import logging

from core.Nodes import ExpressionTree, Node, Set, Operation, Neg
from typing import List, Set as tSet, Dict, Any, Set
from core.Venn import *


class Evaluator:
    def __init__(self):
        self.__objects = []
        self.__variables = []
        self.__truthtable = []
        self.__sets_count_limit = 5  # how many sets are allowed. Corresponds to final Venn diagram
        self.__sets_dict = {}
        self.__universal_solved = []   # the universtal statement result
        self.__existential_solved = {}
        self.__conclusion_solved = {}

    def __get_sets(self, tree: ExpressionTree | Node):
        match tree:
            case None:
                return
            case Set():
                if tree.value not in self.__objects:
                    self.__objects.append(tree.value)
                if tree.variable not in self.__variables:
                    self.__variables.append(tree.variable)
            case ExpressionTree():
                self.__get_sets(tree.tree)
            case Operation() | Neg():
                self.__get_sets(tree.left)
                self.__get_sets(tree.right)
            case _:
                raise TypeError(f'Unknown type passed to evaluator: {type(tree).__name__}')
        print(self.__objects, " :p ")

    def __generate_truthtable(self, size: int):
        if size < 1:
            return [[]]
        sub = self.__generate_truthtable(size - 1)
        return [row + [v] for row in sub for v in [0, 1]]

    def __universal_solve(self, node: Node) -> list[str]:
        if len(self.__objects) <= self.__sets_count_limit:
            logging.info(f"universal {len(self.__objects)}")
            venn = Venn(self.__objects.copy())
            return venn.universal(node)
        raise ValueError(f'Encountered unexpected variable count {len(self.__objects)}.')

    def __existential_solve(self, node: Node):
        print(self.__objects, " :D ", self.__sets_count_limit)
        if len(self.__objects) <= self.__sets_count_limit:
            logging.info(f"universal {len(self.__objects)}")
            venn = Venn(self.__objects.copy())
            return venn.existential(node)
        raise ValueError(f'Neočekávaný počet objektů {len(self.__objects)}. Zkontrolujte vstup.')

    def eval(self, trees: List[ExpressionTree], conclusion_tree: ExpressionTree) -> dict[str, set[str]]:
        existential_validate = 0
        for tree in trees:
            if tree.value == '∃' or tree.value == 'E':
                existential_validate += 1
            self.__get_sets(tree)
        self.__get_sets(conclusion_tree)
        if existential_validate == 0 and conclusion_tree.value == '∃':
            raise LogicException('Nesprávný úsudek. Všeobecné premisy nemohou implikovat existenci.')

        if len(self.__objects) > self.__sets_count_limit:  # +1 for quantifier
            raise Exception(f'Je povoleno nejvýše {self.__sets_count_limit} objektů.\n'
                             f'Překročeno o {len(self.__objects) - self.__sets_count_limit}. Objekty: {self.__objects}')

        self.__truthtable = self.__generate_truthtable(len(self.__objects))

        print(f"objects for the entire diagram: {self.__objects}")
        for var in self.__variables:
            self.__existential_solved[var] = []

        for expr_tree in trees:
            if expr_tree.value == '∀':
                print(f"\nsolving {expr_tree.value}")
                adding = self.__universal_solve(expr_tree)
                print("adding", adding)
                self.__universal_solved += adding
            elif expr_tree.value == '∃':
                adding = self.__existential_solve(expr_tree)
                print(adding, " :x ")
                self.__existential_solved[expr_tree.variable] = self.__existential_solved[expr_tree.variable] + adding
            else:
                raise ValueError('Interní chyba. Obnovte stránku.')

        esolved = {}
        for var in self.__existential_solved.keys():
            esolved[var] = set(self.__existential_solved[var])

        self.__conclusion_solved[conclusion_tree.variable] = self.__existential_solve(conclusion_tree)
        print()
        print(self.__existential_solved, "hi")
        print(self.__universal_solved, "hi")

        return {"Exists within": esolved, "Crossed out": set(self.__universal_solved), "Universum":"Crossed"}

    def __print_truthtable(self):
        print(self.__objects)
        for i, t in enumerate(self.__truthtable):
            print(f" -> {i + 1}: {t}")

    def validity(self, solution: dict[str, set[str]]):
        variable = str(list(self.__conclusion_solved.keys())[0])  # the variable of the conclusion
        print(solution)
        solution_candidates = set((solution['Exists within'][variable])).difference(solution['Crossed out'])
        print (len(solution_candidates))
        print(f"{solution_candidates}, {self.__conclusion_solved[variable]}")
        print(solution_candidates.intersection(set(self.__conclusion_solved[variable])))
        if len(solution_candidates.intersection(set(self.__conclusion_solved[variable]))) == 0:
            return False
        return True


class LogicException(Exception):
    pass
