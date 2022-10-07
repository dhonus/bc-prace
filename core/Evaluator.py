import logging

from core.Nodes import ExpressionTree, Node, Set, Operation, Neg
from typing import List, Set as tSet, Dict, Any, Set
from core.Venn import *


class Evaluator:
    def __init__(self):
        self.__variables = []
        self.__truthtable = []
        self.__sets_count_limit = 5  # how many sets are allowed. Corresponds to final Venn diagram excluding the universe
        self.__sets_dict = {}
        self.__universal_solved = []  # the universtal statement result
        self.__existential_solved = []

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

    def __universal_solve(self, node: Node) -> list[str]:
        if len(self.__variables) <= self.__sets_count_limit:
            logging.info(f"universal {len(self.__variables)}")
            venn = Venn(self.__variables)
            return venn.better_solve(node)
        raise ValueError(f'Encountered unexpected variable count {len(self.__variables)}.')

    def __existential_solve(self, node: Node):
        if len(self.__variables) <= self.__sets_count_limit:
            logging.info(f"universal {len(self.__variables)}")
            venn = Venn(self.__variables)
            return venn.existential(node)
        raise ValueError(f'Encountered unexpected variable count {len(self.__variables)}.')

    def eval(self, trees: List[ExpressionTree], conclusion_tree: ExpressionTree) -> dict[str, set[str]]:
        existential_validate = 0
        for tree in trees:
            if tree.value == '∃':
                existential_validate += 1
            self.__get_sets(tree)
        self.__get_sets(conclusion_tree)

        if existential_validate == 0 and conclusion_tree.value == '∃' and False:
            raise LogicException('Nesprávný úsudek. Příklad Bertranda Russella. Všeobecné premisy nemohou implikovat existenci.')

        if len(self.__variables) > self.__sets_count_limit:  # +1 for quantifier
            raise Exception(f'The maximum amount of sets in Venn is {self.__sets_count_limit}.\n'
                             f'Exceeded by {len(self.__variables) - self.__sets_count_limit}. Sets: {self.__variables}')

        self.__truthtable = self.__generate_truthtable(len(self.__variables))

        print(f"variables for the entire diagram: {self.__variables}")

        for expr_tree in trees:
            if expr_tree.value == '∀':
                print(f"\nsolving {expr_tree.value}")
                adding = self.__universal_solve(expr_tree.tree)
                print("adding", adding)
                self.__universal_solved += adding
            elif expr_tree.value == '∃':
                adding = self.__existential_solve(expr_tree.tree)
                self.__existential_solved += adding
            else:
                raise ValueError('Internal error. Refresh the page.')

        print(self.__existential_solved, "hi")
        return {"Exists within": set(self.__existential_solved), "Crossed out": set(self.__universal_solved), "Universum":"Crossed"}

    def __print_truthtable(self):
        print(self.__variables)
        for i, t in enumerate(self.__truthtable):
            print(f" -> {i + 1}: {t}")


class LogicException(Exception):
    pass
