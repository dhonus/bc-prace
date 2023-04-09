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
        self.__universal_solved = []  # the universal statement result
        self.__existential_solved = {}
        self.__conclusion_solved = {}
        self.__conclusion_variable = None
        self.__conclusion_existential = False
        self.__explanations = {}
        self.__steps = []
        self.__valid_on_all = True  # if it so happens that something goes wrong, the validity is set to false

    def get_invalid_expected(self) -> bool:
        return not self.__valid_on_all

    def get_sets(self):
        return self.__objects

    def get_steps(self):
        return self.__steps

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
            if expr_tree.value == '∀':
                self.__explanations[expr_tree.p_index] = [f"Všeobecná premisa: {expr_tree.print()}. Vyškrtáme oblasti, které vyhovují."]
                self.__universal_solved += self.__universal_solve(expr_tree)

                for solved in set(self.__universal_solved):
                    area = list(solved)
                    # add list to list instead of joining

            elif expr_tree.value == '∃':
                self.__existential_count += 1

                print(f"\nsolving {expr_tree.value} {expr_tree.p_index}")

                adding = set(
                    self.__existential_solve(expr_tree)
                )  # we want this to be length 1
                print(adding, "ADDING")

                # now, of course we do NOT want the areas that we know are hatched (universal statements)
                adding = adding - set(self.__universal_solved)

                print(adding, "ADDING")
                print(set(self.__universal_solved), "uni")

                # we WANT this to be 1, because otherwise we don't know where to put the "x" in the diagram!
                if len(adding) != 1:
                    # so if we DO NOT know where to put the "x", we will tell the user
                    # self.__valid_on_all = False
                    self.__explanations[expr_tree.p_index] = [f"Predikát {expr_tree.p_index}: Pro '{expr_tree.variable}' nevíme, na kterou z ploch {self.__pretty_print(adding)} umístit křížek."]

                    # this means that there is no place to put the "x" in the diagram
                    if len(adding) == 0:
                        self.__explanations[expr_tree.p_index] = [f"Všechny potenciální plochy jsou vyřazeny."]
                        self.__valid_on_all = False  # NOT SURE HERE

                    print("adding is not 1", self.__existential_solved)
                    for var in self.__existential_solved.keys():
                        for constant in constants:
                            self.__existential_solved[constant.variable] += self.__existential_solved[constant.variable]

                        # this should be OK, removing the inaccessible areas
                        existential_solved_final[var] = adding
                        found = False
                        for step in self.__steps:
                            if step["Predicate"] == expr_tree.p_index:
                                step["Exists within"] = existential_solved_final.copy()
                                step["Crossed out"] = list(set(self.__universal_solved.copy()))  # deduplicate
                                step["Explanations"] = self.__explanations.copy()
                                found = True
                        if not found and var == expr_tree.variable:
                            self.__steps.append(
                                {
                                    "Bad": {expr_tree.variable: adding},
                                    "Predicate": expr_tree.p_index,
                                    "Exists within": existential_solved_final.copy(),
                                    "Crossed out": list(set(self.__universal_solved.copy())),  # deduplicate
                                    "Explanations": self.__explanations.copy()  # we need the current state
                                }
                            )
                        for constant in constants:
                            self.__existential_solved[constant.variable] += self.__existential_solved[constant.variable]

                        # this should be OK, removing the inaccessible areas
                        existential_solved_final[expr_tree.variable] = adding
                        self.__conclusion_variable = conclusion_tree.variable
                        self.__conclusion_solved[conclusion_tree.variable] = set(
                            self.__existential_solve(conclusion_tree))

                else:
                    self.__existential_solved[expr_tree.variable] += self.__existential_solve(expr_tree)
                    self.__explanations[expr_tree.p_index] = [f"Existuje pouze jedna plocha, na kterou lze umístit křížek. Tato plocha je {self.__pretty_print(adding)}."]

            else:
                raise ValueError('Interní chyba. Obnovte stránku.')

            # here we just add the existential output of constants to all other variables
            for var in self.__existential_solved.keys():
                print(f"var: {var}")
                for constant in constants:
                    self.__existential_solved[constant.variable] += self.__existential_solved[constant.variable]
                # this should be OK, removing the inaccessible areas
                existential_solved_final[var] = set(self.__existential_solved[var]) - set(self.__universal_solved)
                print(f"existential solved final: {self.__existential_solved[var]}")

            found = False
            for step in self.__steps:
                if step["Predicate"] == expr_tree.p_index:
                    found = True
            if not found:
                self.__steps.append(
                    {
                        "Bad": {},
                        "Predicate": expr_tree.p_index,
                        "Exists within": existential_solved_final.copy(),
                        "Crossed out": list(set(self.__universal_solved.copy())),  # deduplicate
                        "Explanations": self.__explanations.copy()  # we need the current state
                    }
                )

            # here we just add the existential output of constants to all other variables
            for var in self.__existential_solved.keys():
                for constant in constants:
                    self.__existential_solved[constant.variable] += self.__existential_solved[constant.variable]

            # this should be OK, removing the inaccessible areas
            existential_solved_final[var] = set(self.__existential_solved[var]) - set(self.__universal_solved)

        print(f"\nsolving conclusion {conclusion_tree.p_index}")
        self.__conclusion_variable = conclusion_tree.variable
        if conclusion_tree.value == '∃' or conclusion_tree.value == 'E':
            self.__conclusion_existential = True
            self.__conclusion_solved[conclusion_tree.variable] = set(self.__existential_solve(conclusion_tree))
        else:
            self.__conclusion_existential = False
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
        # print(set(solution['Exists within'][variable]), variable)
        # print(set(solution['Crossed out']), "crossed out")
        var_set = set(solution['Exists within'][variable])
        crossed_out = set(solution['Crossed out'])
        # if an element in var_set is in crossed_out remove it from var_set
        var_set.difference_update(crossed_out)
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

        if self.__conclusion_existential:
            if len(var_set) == 0:
                print("conclusion existential", self.__conclusion_solved[variable])
                constants = []
                for v in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
                    if v in solution['Exists within'].keys():
                        print(v, solution['Exists within'][v], "HAA")
                        if not set(solution['Exists within'][v]).isdisjoint(self.__conclusion_solved[variable]):
                            print("Hell yess", v)
                            constants.append(v)
                if len(constants) == 0:
                    self.__explanations[0] = [f"Pro '{variable}' nebylo nalezeno řešení. Žádný existenciální predikát pro '{variable}' nebyl vhodný."]
                    return False
                self.__explanations[0] = [f"Pro '{variable}' bylo nalezeno řešení. Platné konstanty {', '.join(constants)}."]
                return True

            # if any from var_set is in the conclusion, the problem is valid
            if not var_set.isdisjoint(self.__conclusion_solved[variable]):
                if variable in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
                    self.__explanations[0] = [
                        f"Pro '{variable}' platí, že existuje prvek, který spadá do alespoň jednoho z {self.__pretty_print(self.__conclusion_solved[variable])}."]
                else:
                    self.__explanations[0] = [f"Pro '{variable}' platí, že existují prvky, které spadají do alespoň jednoho z {self.__pretty_print(self.__conclusion_solved[variable])}."]

                return True

            self.__explanations[0] = [f"Pro '{variable}' neexistují žádné prvky, které by splňovaly závěr. Existují pouze na {self.__pretty_print(solution['Exists within'][variable])}."]

            return False

        else:
            # here we solve the case in which only universal statements are provided
            # we determine the validity by checking if the areas that should be crossed out are actually crossed out
            if len_sum == 0:
                checking = set(crossed_out) - set(self.__conclusion_solved[variable])
                if set(self.__conclusion_solved[variable]).issubset(crossed_out):
                    self.__explanations[0] = [f"Závěr říká, že mají být vyškrtány {self.__pretty_print(self.__conclusion_solved[variable])}, což odpovídá výsledku."]
                    return True

            if not var_set.issubset(self.__conclusion_solved[variable]):
                # if not var_set.issubset(set(self.__conclusion_solved[variable])):
                #     self.__explanations[0] = [f"Pro '{variable}' není řešení. Existují prvky mimo výběr. {set(self.__conclusion_solved[variable]) - crossed_out}"]
                #    return False
                self.__explanations[0] = [f"Pro '{variable}' nalezeno řešení. "
                                          f"Platí že {self.__pretty_print(var_set)} není vyškrtáno a splňuje tím podmínku závěru."]
                return True

            self.__explanations[0] = [f"Pro '{variable}' není řešení. Je žádané, aby byly vyškrtány {self.__pretty_print(self.__conclusion_solved[variable])}."]
            return False


    def __pretty_print(self, param):
        match param:
            case set():
                ret = ""
                for what, i in enumerate(param):
                    if what == len(param) - 2:
                        ret += self.__pretty_print(i) + " a "
                    else:
                        ret += self.__pretty_print(i)
                        if what != len(param) - 1:
                            ret += ", "
                return ret
            case tuple():
                ret = "("
                if len(param) == 1:
                    return ret + self.__pretty_print(param[0]) + ")"
                for i, what in enumerate(param):
                    ret += self.__pretty_print(what)
                    if i != len(param) - 1:
                        ret += " ∩ "
                return ret + ")"
            case _:
                return str(param)

class LogicException(Exception):
    pass
