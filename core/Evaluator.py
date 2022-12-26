import logging

from core.Nodes import ExpressionTree, Node, Set, Operation, Neg
from typing import List, Set as tSet, Dict, Any, Set
from core.Venn import *


def deprecated(args):
    print("This is an old function")
    pass


class Evaluator:
    def __init__(self):
        self.__existential_count = 0
        self.__objects = []
        self.__variables = []
        self.__sets_count_limit = 5  # how many sets are allowed. Corresponds to final Venn diagram
        self.__sets_dict = {}
        self.__universal_solved = []  # the universtal statement result
        self.__existential_solved = {}
        self.__conclusion_solved = {}
        self.__explanations = {}
        self.__valid_on_all = True  # if it so happens that something goes wrong, the validity is set to false

    def get_invalid_expected(self) -> bool:
        return not self.__valid_on_all

    def get_sets(self):
        return self.__objects

    def get_explanations(self):
        return self.__explanations

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

    def eval(self, trees: List[ExpressionTree], conclusion_tree: ExpressionTree) -> dict[str, list[str]]:
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
            self.__valid_on_all = False
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
            self.__explanations[expr_tree.p_index] = []
            if expr_tree.value == '∀':
                print(f"\nsolving {expr_tree.value} {expr_tree.p_index}")
                self.__universal_solved += self.__universal_solve(expr_tree)
                print(set(self.__universal_solved), ";)")

                for solved in set(self.__universal_solved):
                    area = list(solved)
                    print(area)
                    # add list to list instead of joining
                    self.__explanations[expr_tree.p_index].append(area)

                self.__existential_solved[expr_tree.variable] = []
            elif expr_tree.value == '∃':
                self.__existential_count += 1
                print(f"\nsolving {expr_tree.value} {expr_tree.p_index}")
                adding = set(self.__existential_solve(expr_tree)) # we want this to be length 1
                print(adding, "ADDING")
                # remove from adding those that are in universal
                adding = adding - set(self.__universal_solved)
                if len(adding) != 1:
                    self.__explanations[expr_tree.p_index] = f"Nevíme na kterou plochu z {self.__universal_solved} umístit {adding}"
                    self.__valid_on_all = False
                else:
                    self.__existential_solved[expr_tree.variable] += self.__existential_solve(expr_tree)
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

        print(f"\nsolving conclusion {conclusion_tree.p_index}")
        self.__conclusion_solved[conclusion_tree.variable] = set(self.__existential_solve(conclusion_tree))
        print(self.__conclusion_solved, "conclusion")
        print(self.__existential_solved, "hi")
        print(self.__universal_solved, "hi2")

        print(f"\n\nExplanations : {self.__explanations}\n\n")

        return {
            "Exists within": existential_solved_final,
            "Crossed out": list(set(self.__universal_solved)),  # deduplicate
            "Explanations": self.__explanations
        }

    def validity(self, solution: dict[str, dict[str, list[str]]]) -> bool:
        """ checks the validity of the entire problem using the parsed existential and universal results """
        variables = list(solution['Exists within'].keys())  # the variable of the conclusion
        print(variables, "solution")

        ret = True
        len_sum = 0
        for variable in variables:
            len_sum += len(solution['Exists within'][variable])
            print(set(solution['Exists within'][variable]), variable)
            print(set(solution['Crossed out']), "crossed out")
            var_set = set(solution['Exists within'][variable])
            crossed_out = set(solution['Crossed out'])
            # if an element in var_set is in crossed_out remove it from var_set
            var_set.difference_update(crossed_out)
            print(var_set, "var_set")
            try:
                print(self.__conclusion_solved[variable], "conclusion")
                # if the conclusion is not a subset of the var_set, the problem is invalid
                if not var_set.issubset(self.__conclusion_solved[variable]):
                    ret = False
                print(set(self.__conclusion_solved[variable]), "conclusion")
            except KeyError:
                print("not the correct variable")

        # if we have 0 crosses and it is not the case that the problem is purely
        # universal, we can say that the problem is invalid
        if len_sum == 0 and self.__existential_count != 0:
            ret = False
        return ret

    """
     solution_candidates = set((solution['Exists within'][variable])).difference(solution['Crossed out'])
            print(len(solution_candidates))
            print(f"{solution_candidates}, {self.__conclusion_solved[variable]}")
            print(solution_candidates.intersection(set(self.__conclusion_solved[variable])))
            if len(solution_candidates.intersection(set(self.__conclusion_solved[variable]))) == 0:
                ret = ret & False
            ret = ret & True"""


"""
    def validity(self, solution: dict[str, list[str]]):
         checks the validity of the entire problem using the parsed existential and universal results 
        variable = str(list(self.__conclusion_solved.keys())[0])  # the variable of the conclusion
        print(variable, "solution")
        solution_candidates = set((solution['Exists within'][variable])).difference(solution['Crossed out'])
        print(len(solution_candidates))
        print(f"{solution_candidates}, {self.__conclusion_solved[variable]}")
        print(solution_candidates.intersection(set(self.__conclusion_solved[variable])))
        if len(solution_candidates.intersection(set(self.__conclusion_solved[variable]))) == 0:
            return False
        return True
 """


class LogicException(Exception):
    pass
