import logging

from core.Nodes import ExpressionTree, Node, Set, Operation, Neg
from typing import List, Set as tSet, Dict, Any, Set
from core.Venn import *


def deprecated(args):
    print("This is an old function")
    pass


class Evaluator:
    def __init__(self):
        self.__objects = []
        self.__variables = []
        self.__sets_count_limit = 5  # how many sets are allowed. Corresponds to final Venn diagram
        self.__sets_dict = {}
        self.__universal_solved = []   # the universtal statement result
        self.__existential_solved = {}
        self.__conclusion_solved = {}

    def __get_variables(self, tree: ExpressionTree | Node):
        """ produces a list of variables in the expression tree """
        match tree:
            case None:
                return
            case Set():
                if tree.value not in self.__objects:
                    self.__objects.append(tree.value)
                if tree.variable not in self.__variables:
                    self.__variables.append(tree.variable)
            case ExpressionTree():
                self.__get_variables(tree.tree)
            case Operation() | Neg():
                self.__get_variables(tree.left)
                self.__get_variables(tree.right)
            case _:
                raise TypeError(f'Unknown type passed to evaluator: {type(tree).__name__}')
        # print(self.__objects, " :p ")

    def __universal_solve(self, node: Node) -> list[str]:
        """ solves a universal predicate and produces list of crossed out areas """
        if len(self.__objects) <= self.__sets_count_limit:
            logging.info(f"universal {len(self.__objects)}")
            venn = Venn(self.__objects.copy())
            return venn.universal(node)
        raise ValueError(f'Neočekávaný počet objektů {len(self.__objects)}. Zkontrolujte vstup.')

    def __existential_solve(self, node: Node):
        """ solves an existential predicate; same alg as universal. Produces list of areas which contain elements """
        print(self.__objects, " :D ", self.__sets_count_limit)
        if len(self.__objects) <= self.__sets_count_limit:
            logging.info(f"universal {len(self.__objects)}")
            venn = Venn(self.__objects.copy())
            return venn.existential(node)
        raise ValueError(f'Neočekávaný počet objektů {len(self.__objects)}. Zkontrolujte vstup.')

    def eval(self, trees: List[ExpressionTree], conclusion_tree: ExpressionTree) -> dict[str, set[str]]:
        """ takes all the predicates and sequentially produces lists of 'areas' of the imaginary venn diagram
            read as: predicate -> 'is this area crossed out or does it contain an X?'. Solves universal first. """
        existential_validate = 0

        # we must count up existential predicates to check for this basic logical error
        for tree in trees:
            if tree.value == '∃' or tree.value == 'E':
                existential_validate += 1
            self.__get_variables(tree)
        self.__get_variables(conclusion_tree)
        if existential_validate == 0 and conclusion_tree.value == '∃':
            raise LogicException('Nesprávný úsudek. Všeobecné premisy nemohou implikovat existenci.')

        # there is a limit to how many objects we can draw. This checks if we have exceeded said limit.
        if len(self.__objects) > self.__sets_count_limit:  # +1 for quantifier
            raise Exception(f'Je povoleno nejvýše {self.__sets_count_limit} objektů.\n'
                             f'Překročeno o {len(self.__objects) - self.__sets_count_limit}. Objekty: {self.__objects}')

        print(f"objects for the entire diagram: {self.__objects}")
        for var in self.__variables:
            self.__existential_solved[var] = []

        # universal predicates have priority
        for expr_tree in trees:
            if expr_tree.value == '∀':
                print(f"\nsolving {expr_tree.value}")
                adding = self.__universal_solve(expr_tree)
                self.__universal_solved += adding
                self.__existential_solved[expr_tree.variable] = []
            elif expr_tree.value == '∃':
                adding = self.__existential_solve(expr_tree)
                self.__existential_solved[expr_tree.variable] = self.__existential_solved[expr_tree.variable] + adding
            else:
                raise ValueError('Interní chyba. Obnovte stránku.')

        constants = []
        for expr_tree in trees:
            if expr_tree.constant:
                constants.append(expr_tree)

        # since we have outputs for multiple different variables, we can store them in a dictionary
        existential_solved_final = {}

        # here we just add the existential output of constants to all other variables
        for var in self.__existential_solved.keys():
            for constant in constants:
                print(self.__existential_solved[constant.variable], "ggg")
                self.__existential_solved[var] += self.__existential_solved[constant.variable]
            existential_solved_final[var] = set(self.__existential_solved[var])

        self.__conclusion_solved[conclusion_tree.variable] = self.__existential_solve(conclusion_tree)
        print()
        print(self.__existential_solved, "hi")
        print(self.__universal_solved, "hi")

        return {"Exists within": existential_solved_final, "Crossed out": set(self.__universal_solved), "Universum":"Crossed"}

    def validity(self, solution: dict[str, set[str]]):
        """ checks the validity of the entire problem using the parsed existential and universal results """
        variable = str(list(self.__conclusion_solved.keys())[0])  # the variable of the conclusion
        #print(solution)
        solution_candidates = set((solution['Exists within'][variable])).difference(solution['Crossed out'])
        print(len(solution_candidates))
        print(f"{solution_candidates}, {self.__conclusion_solved[variable]}")
        print(solution_candidates.intersection(set(self.__conclusion_solved[variable])))
        if len(solution_candidates.intersection(set(self.__conclusion_solved[variable]))) == 0:
            return False
        return True


class LogicException(Exception):
    pass
