import logging

from core.Nodes import ExpressionTree, Node, Set, Operation, Neg
from typing import List


class Evaluator:
    def __init__(self):
        self.__variables = []
        self.__truthtable = []
        self.__sets = 4  # how many sets are allowed. Corresponds to final Venn diagram excluding the universe
        self.__sets_dict = {}

    def __get_sets(self, tree: ExpressionTree | Node):
        match tree:
            case None:
                return
            case Set():
                if tree.value not in self.__variables:
                    self.__variables.append(tree.value)
            case ExpressionTree():
                self.__get_sets(tree.tree)
            case Operation() | Neg():
                self.__get_sets(tree.left)
                self.__get_sets(tree.right)
            case _:
                raise TypeError(f'Unknown type passed to evaluator: {type(tree).__name__}')

    def __generate_truthtable(self, size: int):
        if size < 1:
            return [[]]
        sub = self.__generate_truthtable(size - 1)
        return [row + [v] for row in sub for v in [0, 1]]

    def __universal_solve(self, node):
        logging.info("universal")

        # ∀x[!(S(x) <> X(x)) & V(x)]:
        match node:
            case None:
                logging.info("none")
                return
            case Set():
                print("set ", node.value)
                self.__sets_dict[node.value] = "_"
                return node.value
            case Neg():
                print("no", node.left.value)
                left = self.__universal_solve(node.left)
                self.__variables.append('!' + left)
                return '!' + left
            case Operation():
                print("oper", node.value)
                left = self.__universal_solve(node.left)
                right = self.__universal_solve(node.right)
                print(f"{left}{node.value}{right}")
                self.__variables.append(f"{left}{node.value}{right}")
                self.__print_truthtable()

                for row in self.__truthtable:
                    row.append(0)

                return f"{left}{node.value}{right}"

    def __existential_solve(self, expr_tree: ExpressionTree):
        pass

    def eval(self, trees: List[ExpressionTree], conclusion_tree: ExpressionTree) -> List[str]:
        existential_validate = 0
        for tree in trees:
            if tree.value == '∃':
                existential_validate += 1
            self.__get_sets(tree)
        self.__get_sets(conclusion_tree)

        if existential_validate == 0 and conclusion_tree.value == '∃':
            raise LogicException('Nesprávný úsudek. Příklad Bertranda Russella. Všeobecné premisy nemohou implikovat existenci.')

        if len(self.__variables) > self.__sets:  # +1 for quantifier
            raise Exception(f'The maximum amount of sets in Venn is {self.__sets}.\n'
                             f'Exceeded by {len(self.__variables) - self.__sets}. Sets: {self.__variables[1:]}')

        self.__truthtable = self.__generate_truthtable(len(self.__variables))

        print(self.__variables)

        self.__print_truthtable()

        for expr_tree in trees:
            self.__sets_dict = {}
            if expr_tree.value == '∀':
                print(f"solving {expr_tree.value}")
                self.__universal_solve(expr_tree.tree)
            elif expr_tree.value == '∃':
                self.__existential_solve(expr_tree.tree)
            else:
                raise ValueError('Internal error. Refresh the page.')

            print(self.__sets_dict)

        return self.__variables

    def __print_truthtable(self):
        print(self.__variables)
        for i, t in enumerate(self.__truthtable):
            print(f" -> {i + 1}: {t}")


class LogicException(Exception):
    pass
