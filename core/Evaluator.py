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
        self.__conclusion_variable = None
        self.__explanations = {}
        self.__steps = []
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

        # since we have outputs for multiple different variables, we can store them in a dictionary
        existential_solved_final = {}

        constants = []
        for expr_tree in trees:
            if expr_tree.constant:
                constants.append(expr_tree)

        # universal predicates have priority
        for expr_tree in trees:
            self.__explanations[expr_tree.p_index] = ["hi"]  # TBA
            if expr_tree.value == '∀':
                print(f"\nsolving {expr_tree.value} {expr_tree.p_index}")
                self.__universal_solved += self.__universal_solve(expr_tree)
                print(set(self.__universal_solved), ";)")

                for solved in set(self.__universal_solved):
                    area = list(solved)
                    print(area)
                    # add list to list instead of joining

                self.__existential_solved[expr_tree.variable] = []
            elif expr_tree.value == '∃':
                self.__existential_count += 1
                print(f"\nsolving {expr_tree.value} {expr_tree.p_index}")
                adding = set(self.__existential_solve(expr_tree)) # we want this to be length 1
                print(adding, "ADDING")
                # remove from adding those that are in universal
                adding = adding - set(self.__universal_solved)

                if len(adding) != 1:
                    self.__explanations[expr_tree.p_index] = [f"Nevíme na kterou plochu umístit {adding}"]
                    if len(adding) == 0:
                        self.__explanations[expr_tree.p_index] = [f"Všechny plochy jsou vyřazeny"]
                    self.__valid_on_all = False

                    for var in self.__existential_solved.keys():
                        for constant in constants:
                            self.__existential_solved[var] += self.__existential_solved[constant.variable]
                        # this should be OK, removing the inaccessible areas
                        existential_solved_final[var] = adding
                        self.__steps.append(
                            {
                                "Exists within": adding,
                                "Crossed out": list(set(self.__universal_solved)),  # deduplicate
                                "Explanations": self.__explanations.copy()
                            }
                        )
                        for constant in constants:
                            self.__existential_solved[var] += self.__existential_solved[constant.variable]
                        # this should be OK, removing the inaccessible areas
                        existential_solved_final[expr_tree.variable] = adding
                        self.__conclusion_variable = conclusion_tree.variable
                        if conclusion_tree.value == '∃' or conclusion_tree.value == 'E':
                            self.__conclusion_solved[conclusion_tree.variable] = set(
                                self.__existential_solve(conclusion_tree))
                        else:
                            self.__conclusion_solved[conclusion_tree.variable] = set(
                                self.__universal_solve(conclusion_tree))

                        print()
                        print("STEPS")
                        for step in self.__steps:
                            print(step)
                        print()

                        return {
                            "Exists within": existential_solved_final,
                            "Crossed out": list(set(self.__universal_solved)),  # deduplicate
                            "Explanations": self.__explanations
                        }

                else:
                    self.__existential_solved[expr_tree.variable] += self.__existential_solve(expr_tree)
            else:
                raise ValueError('Interní chyba. Obnovte stránku.')

            # here we just add the existential output of constants to all other variables
            for var in self.__existential_solved.keys():
                for constant in constants:
                    self.__existential_solved[var] += self.__existential_solved[constant.variable]
                # this should be OK, removing the inaccessible areas
                existential_solved_final[var] = set(self.__existential_solved[var]) - set(self.__universal_solved)

            self.__steps.append(
                {
                    "Exists within": existential_solved_final,
                    "Crossed out": list(set(self.__universal_solved)),  # deduplicate
                    "Explanations": self.__explanations.copy()  # we need the current state
                }
            )

        # here we just add the existential output of constants to all other variables
        for var in self.__existential_solved.keys():
            for constant in constants:
                self.__existential_solved[var] += self.__existential_solved[constant.variable]
            # this should be OK, removing the inaccessible areas
            existential_solved_final[var] = set(self.__existential_solved[var]) - set(self.__universal_solved)

        print(f"\nsolving conclusion {conclusion_tree.p_index}")
        self.__conclusion_variable = conclusion_tree.variable
        if conclusion_tree.value == '∃' or conclusion_tree.value == 'E':
            self.__conclusion_solved[conclusion_tree.variable] = set(self.__existential_solve(conclusion_tree))
        else:
            self.__conclusion_solved[conclusion_tree.variable] = set(self.__universal_solve(conclusion_tree))

        print(f"\n\nExplanations : {self.__explanations}\n\n")

        print()
        print("STEPS")
        for step in self.__steps:
            print(step)
        print()

        return {
            "Exists within": existential_solved_final,
            "Crossed out": list(set(self.__universal_solved)),  # deduplicate
            "Explanations": self.__explanations
        }

    def validity(self, solution: dict[str, dict[str, list[str]]]) -> bool:
        """ checks the validity of the entire problem using the parsed existential and universal results """
        variables = list(solution['Exists within'].keys())  # the variable of the conclusion
        print(variables, "solution")
        print(self.__conclusion_variable, "conclusion")

        if not self.__valid_on_all:
            return False

        ret = True
        len_sum = 0
        # for variable in variables:

        variable = self.__conclusion_variable

        len_sum += len(solution['Exists within'][variable])
        print(set(solution['Exists within'][variable]), variable)
        print(set(solution['Crossed out']), "crossed out")
        var_set = set(solution['Exists within'][variable])
        crossed_out = set(solution['Crossed out'])
        # if an element in var_set is in crossed_out remove it from var_set
        var_set.difference_update(crossed_out)
        print(var_set, "var_set")

        print (len_sum, "len_sum")
        if len_sum == 0:
            self.__explanations[0] = [f"Pro {variable} nebylo nalezeno řešení. Nebyl zadán predikát pro {variable}."]
        try:
            print(self.__conclusion_solved[variable], "conclusion")
            # if the conclusion is not a subset of the var_set, the problem is invalid
            if not var_set.issubset(self.__conclusion_solved[variable]):
                ret = False
            print(set(self.__conclusion_solved[variable]), "conclusion")
        except KeyError:
            print("not the correct variable")

        # here we solve the case in which only universal statements are provided
        # we determine the validity by checking if the areas that should be crossed out are actually crossed out
        if len_sum == 0:
            checking = set(crossed_out) - set(self.__conclusion_solved[variable])
            if set(self.__conclusion_solved[variable]).issubset(crossed_out):
                self.__explanations[0] = [f"Platí, že vyškrtání {checking} vystihuje aktuální řešení."]
                return True
            else:
                self.__explanations[0] = [f"Toto nelze tvrdit. Všechny z {self.__conclusion_solved[variable]} musí být vyškrtány."]
                return False

        # if we have 0 crosses, and it is not the case that the problem is purely
        # universal, we can say that the problem is invalid
        if len_sum == 0 and self.__existential_count != 0:
            self.__explanations[0] = [f"Pro {variable} nebylo nalezeno řešení. Žádná existenciální tvrzení."]
            ret = False

        if len_sum == 1:
            if len(crossed_out) == 0:
                self.__explanations[0] = [f"Pro {variable} nalezeno řešení. "
                                          f"Můžeme umístit {var_set} a jedná se o jediné řešení."]
            else:
                self.__explanations[0] = [f"Pro {variable} nalezeno řešení. "
                                  f"Můžeme umístit {var_set}, protože {crossed_out} jsou vyškrtány."]
            ret = True
        else:
            self.__explanations[0] = [f"Pro {variable} není řešení. "
                                  f"Nevíme kam umístit {var_set}"]
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
