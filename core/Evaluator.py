import logging

from core.Nodes import ExpressionTree, Node, Set, Operation, Neg
from typing import List, Set as tSet, Dict, Any, Set
from core.Venn import *


class Evaluator:
    def __init__(self):
        self.__existential_count = 0
        self.__objects = []
        self.__variables = []
        self.__sets_count_limit = 5  # how many sets are allowed. Corresponds to final Venn diagram
        self.__sets_dict = {}
        self.__universal_solved = []  # the universal statement result
        self.__universal_solved_counts = {}  # the universal statement result
        self.__existential_solved = {}
        self.__all_solved = {}
        self.__all_solved_by_whom = {}
        self.__bad = {}
        self.__conclusion_solved = {}
        self.__conclusion_variable = None
        self.__conclusion_existential = False
        self.__explanations = {}
        self.__steps = []
        self.__valid_on_all = True  # if it so happens that something goes wrong, the validity is set to false
        self.__contradiction = [False, -1, ""]
        self.__contain = []
        self.__constant_jail = {}
        self.__area_combinations = []
        self.__invalid = False

    def get_invalid_expected(self) -> bool:
        return not self.__valid_on_all

    def get_sets(self):
        return self.__objects

    def get_steps(self):
        return self.__steps

    def get_explanations(self):
        return self.__explanations

    def get_combinations(self):
        # [('A',), ('B',), ('Ω',), ('A', 'B'), ('A', 'Ω'), ('B', 'Ω'), ('A', 'B', 'Ω')]
        sol_universum_accounted = list()
        # remove universe symbol from all but just itself
        # {'AΩ', 'Ω', 'BΩ'} -> {'A', 'Ω', 'B'}
        for item in self.__area_combinations:
            if item[0] == 'Ω' and len(item) == 1:
                sol_universum_accounted.append(item)
                continue
            try:
                idx = item.index('Ω')
                if idx == 0 and len(item) == 1:
                    sol_universum_accounted.append(item)
                    continue
                item = item[:idx] + item[idx + 1:]
            except ValueError:
                pass  # not in tuple
            adding = item
            if adding:
                sol_universum_accounted.append(adding)

        output = []
        for item in sorted(sol_universum_accounted):
            output.append(",".join(sorted(item)))

        return sorted(list(set(output)))

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
            self.__area_combinations = venn.get_combinations()
            return venn.universal(node)
        raise ValueError(f'Neočekávaný počet objektů {len(self.__objects)}. Zkontrolujte vstup.')

    def __existential_solve(self, node: Node):
        """ solves an existential predicate; same alg as universal. Produces list of areas which contain elements """
        if len(self.__objects) <= self.__sets_count_limit:
            logging.info(f"universal {len(self.__objects)}")
            venn = Venn(self.__objects.copy())
            self.__area_combinations = venn.get_combinations()
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
            self.__invalid = True
            print("Invalid: conclusion is existential, but there are no existential predicates.")

        # there is a limit to how many sets we can draw. This checks if we have exceeded said limit.
        if len(self.__objects) > self.__sets_count_limit:  # +1 for quantifier
            raise Exception(f'Je povoleno nejvýše {self.__sets_count_limit} množin.\n'
                            f'Překročeno o {len(self.__objects) - self.__sets_count_limit}. Množiny: {self.__objects}')

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
                """self.__explanations[expr_tree.p_index] = [
                    f"Všeobecná premisa: {expr_tree.print()}. Vyškrtáme prázdné oblasti."]"""
                new_solved = self.__universal_solve(expr_tree)
                self.__universal_solved += new_solved
                self.__explanations[expr_tree.p_index] = [
                    f"Všeobecná premisa: Vyškrtáme prázdné oblasti. Jedná se o {self.__pretty_print(set(new_solved))}."]
                if len(set(new_solved)) == 0:
                    self.__explanations[expr_tree.p_index] = [f"Všeobecná premisa: Neovlivňuje žádnou oblast."]
                print (set(self.__universal_solved), "universal solved NOTE", expr_tree.p_index)
                self.__universal_solved_counts[expr_tree.p_index] = set(self.__universal_solve(expr_tree))
                """for area in list(self.__universal_solved):
                    if set(area) not in self.__universal_solved_counts:
                        self.__universal_solved_counts[area] = set(expr_tree.p_index)
                    else:
                        self.__universal_solved_counts[area].add(expr_tree.p_index)
                print(self.__universal_solved_counts, "universal solved counts")"""

            elif expr_tree.value == '∃':
                self.__existential_count += 1

                print(f"\nsolving {expr_tree.value} {expr_tree.p_index}")

                adding = set(
                    self.__existential_solve(expr_tree)
                )  # we want this to be length 1

                # now, of course we do NOT want the areas that we know are hatched (universal statements)
                orig_adding = adding.copy()
                adding = adding - set(self.__universal_solved)

                if expr_tree.variable not in self.__all_solved:
                    self.__all_solved[expr_tree.variable] = adding
                    for area in adding:
                        if area not in self.__all_solved_by_whom:
                            self.__all_solved_by_whom[area] = [expr_tree.p_index]
                        else:
                            self.__all_solved_by_whom[area].append(expr_tree.p_index)
                else:
                    self.__all_solved[expr_tree.variable] = self.__all_solved[expr_tree.variable].intersection(adding)
                    for area in adding:
                        if area not in self.__all_solved_by_whom:
                            self.__all_solved_by_whom[area] = [expr_tree.p_index]
                        else:
                            self.__all_solved_by_whom[area].append(expr_tree.p_index)

                self.__contain.append([expr_tree.p_index, adding, expr_tree.variable])

                if expr_tree.variable in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
                    # if not in dict
                    if expr_tree.variable not in self.__constant_jail:
                        self.__constant_jail[expr_tree.variable] = adding
                        print (self.__constant_jail, "jail")
                    else:
                        # if adding is not a subset of the previous adding
                        if adding.isdisjoint(self.__constant_jail[expr_tree.variable]):
                            self.__contradiction = [True, expr_tree.p_index, f"Nalezen spor pro '{expr_tree.variable}'."]

                # we WANT this to be 1, because otherwise we don't know where to put the "x" in the diagram!
                if len(adding) == 1:
                    self.__existential_solved[expr_tree.variable] += self.__existential_solve(expr_tree)
                    msg = f"Existuje pouze jedna plocha, na kterou lze umístit křížek. Tato plocha je {self.__pretty_print(adding)}. "
                    if self.__contradiction[0]:
                        msg += f"Nalezen však spor pro '{expr_tree.variable}'."
                    self.__explanations[expr_tree.p_index] = [msg]
                else:
                    # so if we DO NOT know where to put the "x", we will tell the user
                    # self.__valid_on_all = False
                    self.__explanations[expr_tree.p_index] = [
                        f"{expr_tree.p_index}. premisa: Pro '{expr_tree.variable}' nevíme, na kterou z oblastí {self.__pretty_print(adding)} umístit křížek."]
                    # check for contradiction
                    # if adding is empty, that means that we have a contradiction
                    # if orig_adding is not empty, that means that we have a contradiction
                    print(adding, "adding")
                    print(orig_adding, "orig adding")
                    if len(adding) == 0 and len(orig_adding) == 0:
                        self.__explanations[expr_tree.p_index] = [f"Všechny potenciální plochy jsou vyřazeny. Předpoklady jsou ve sporu. Oblast {self.__pretty_print(orig_adding)} je vyřazena."]
                        self.__contradiction = [True, expr_tree.p_index, "Všechny potenciální plochy jsou vyřazeny. Předpoklady jsou ve sporu."]

                    # this means that there is no place to put the "x" in the diagram
                    if len(adding) == 0 and len(orig_adding) != 0:
                        self.__explanations[expr_tree.p_index] = [f"Všechny potenciální plochy jsou vyřazeny. Předpoklady jsou ve sporu. Oblast {self.__pretty_print(orig_adding)} je vyřazena."]
                        self.__valid_on_all = False
                        self.__contradiction = [True, expr_tree.p_index, "Všechny potenciální plochy jsou vyřazeny. Předpoklady jsou ve sporu."]

                    for var in self.__existential_solved.keys():
                        for constant in constants:
                            self.__existential_solved[constant.variable] += self.__existential_solved[constant.variable]

                        # this should be OK, removing the inaccessible areas
                        # if this is the one we care about
                        if var == expr_tree.variable:
                            existential_solved_final[var] = adding.copy()
                        else:
                            # empty
                            existential_solved_final[var] = set()
                        print(existential_solved_final, "existential solved final")
                        found = False
                        for step in self.__steps:
                            if step["Predicate"] == expr_tree.p_index:
                                step["Exists within"] = existential_solved_final.copy()
                                step["Crossed out"] = list(set(self.__universal_solved.copy()))  # deduplicate
                                step["Explanations"] = self.__explanations.copy()
                                step["Bad"] = {expr_tree.variable: adding}
                                step["Counts"] = self.__universal_solved_counts.copy()
                                found = True
                        if not found and var == expr_tree.variable:
                            self.__steps.append(
                                {
                                    "Bad": {expr_tree.variable: adding},
                                    "Predicate": expr_tree.p_index,
                                    "Exists within": existential_solved_final.copy(),
                                    "Crossed out": list(set(self.__universal_solved.copy())),  # deduplicate
                                    "Explanations": self.__explanations.copy(),  # we need the current state
                                    "Counts": self.__universal_solved_counts.copy()
                                }
                            )
                        for constant in constants:
                            self.__existential_solved[constant.variable] += self.__existential_solved[constant.variable]

                        print(self.__steps, "steps!!")

                        # this should be OK, removing the inaccessible areas
                        existential_solved_final[expr_tree.variable] = adding
                        self.__conclusion_variable = conclusion_tree.variable
                        self.__conclusion_solved[conclusion_tree.variable] = set(
                            self.__existential_solve(conclusion_tree))
                        self.__bad[expr_tree.variable] = adding

            else:
                raise ValueError('Interní chyba. Obnovte stránku.')

            # here we just add the existential output of constants to all other variables
            for var in self.__existential_solved.keys():
                for constant in constants:
                    self.__existential_solved[constant.variable] += set(self.__existential_solved[constant.variable])
                # this should be OK, removing the inaccessible areas
                existential_solved_final[var] = set(self.__existential_solved[var]) - set(self.__universal_solved)

            found = False
            for step in self.__steps:
                if step["Predicate"] == expr_tree.p_index:
                    found = True
            if not found:
                self.__steps.append(
                    {
                        "Bad": self.__bad.copy(),
                        "Predicate": expr_tree.p_index,
                        "Exists within": existential_solved_final.copy(),
                        "Crossed out": list(set(self.__universal_solved.copy())),  # deduplicate
                        "Explanations": self.__explanations.copy(),  # we need the current state
                        "Counts": self.__universal_solved_counts.copy()
                    }
                )

            # here we just add the existential output of constants to all other variables
            for var in self.__existential_solved.keys():
                for constant in constants:
                    self.__existential_solved[constant.variable] += self.__existential_solved[constant.variable]

            # this should be OK, removing the inaccessible areas
            existential_solved_final[var] = set(self.__existential_solved[var]) - set(self.__universal_solved)

        self.__conclusion_variable = conclusion_tree.variable
        if conclusion_tree.value == '∃' or conclusion_tree.value == 'E':
            self.__conclusion_existential = True
            self.__conclusion_solved[conclusion_tree.variable] = set(self.__existential_solve(conclusion_tree))
        else:
            self.__conclusion_existential = False
            self.__conclusion_solved[conclusion_tree.variable] = set(self.__universal_solve(conclusion_tree))

        return {
            "Exists within": existential_solved_final,
            "Crossed out": list(set(self.__universal_solved)),  # deduplicate
            "Explanations": self.__explanations,
            "Counts": self.__universal_solved_counts
        }

    def validity(self, solution: dict[str, dict[str, list[str]]]) -> bool:
        """ checks the validity of the entire problem using the parsed existential and universal results """
        variables = list(solution['Exists within'].keys())  # the variable of the conclusion
        print(variables, "solution")
        print(self.__conclusion_variable, "conclusion")
        if not solution.get('Bad'):
            solution['Bad'] = {}

        if self.__contradiction[0]:
            self.__explanations[0] = [self.__contradiction[2]]
            return True

        if not self.__valid_on_all and not self.__invalid:
            return False

        ret = True
        len_sum = 0

        # for variable in variables:
        variable = self.__conclusion_variable

        len_sum += len(solution['Exists within'][variable])
        var_set = set(solution['Exists within'][variable])
        crossed_out = set(solution['Crossed out'])

        print(self.__contain, "contains")
        print(var_set, "var set")

        print("-------\nall the good things:")
        print (self.__all_solved)
        print("-------")

        # if an element in var_set is in crossed_out remove it from var_set
        var_set.difference_update(crossed_out)
        print(var_set, "var set")
        print(self.__conclusion_solved[variable], "conclusion solved")
        print(len(self.__objects)**2)
        print(len(self.__conclusion_solved[variable]))

        all_ = True

        for key in self.__conclusion_solved:
            if self.__conclusion_solved[key] != set():
                all_ = False
        if self.__conclusion_existential:
            if all_ or (2**len(self.__objects) == len(self.__conclusion_solved[variable])): # tautology
                if len(self.__conclusion_solved[variable]) != 0:
                    self.__explanations[0] = [f"Pro '{variable}' bylo nalezeno řešení. Závěr je tautologie."]
                else:
                    if self.__invalid:
                        raise LogicException('Nesprávný úsudek. Ze všeobecných premis nemůže vyplývat existence.')
                    if self.__contradiction[0]:
                        self.__explanations[0] = [self.__contradiction[2]]
                        return True
                    self.__explanations[0] = [f"Sporný závěr pro '{variable}'"]
                    return False
                return True
        else:
            if all_ or (2**len(self.__objects) == len(self.__conclusion_solved[variable])): # tautology
                if len(self.__conclusion_solved[variable]) == 0:
                    self.__explanations[0] = [f"Pro '{variable}' bylo nalezeno řešení. Závěr je tautologie."]
                else:
                    if self.__contradiction[0]:
                        self.__explanations[0] = [self.__contradiction[2]]
                        return True
                    self.__explanations[0] = [f"Sporný závěr pro '{variable}'"]
                    return False
                return True

        if len_sum == 0:
            self.__explanations[0] = [f"Pro {variable} nebylo nalezeno řešení. Nebyl zadán predikát pro {variable}."]

        if self.__conclusion_existential:
            if self.__invalid:
                raise LogicException('Nesprávný úsudek. Ze všeobecných premis nemůže vyplývat existence.')
            major_set = set()
            all_have_in_common = set()
            if len(self.__contain) > 0:
                if variable == self.__contain[0][2] or self.__contain[0][2] in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
                    print(all_have_in_common, "all have in common!!")
            # this is for the case of
            # Ax[A(x) | B(x)]
            # A(a)
            # B(a)
            # ---
            # Ex[B(x) & A(x)]
            for v in self.__all_solved:
                print(v, "v")
                print(self.__all_solved)
                print(self.__all_solved_by_whom, "whom")
                common = set(self.__all_solved[v])
                common_numbers = set()
                print(common)

                for c in common:
                    if len(common_numbers) == 0:
                        common_numbers.update(set(self.__all_solved_by_whom[c]))
                    else:
                        common_numbers.intersection_update(set(self.__all_solved_by_whom[c]))

                if v in ['a', 'b', 'c', 'd', 'e', 'f', 'g'] and variable not in ['a', 'b', 'c', 'd', 'e', 'f', 'g'] and variable != v:
                    print(self.__conclusion_solved)
                    print(self.__all_solved[v], "all solved")
                    if self.__all_solved[v].issubset(set(self.__conclusion_solved[variable])):
                        if len(common_numbers) > 1:
                            self.__explanations[0] = [
                                f"Pro '{variable}' bylo nalezeno řešení. Existenciální predikát pro '{variable}' byl vhodný - nachází se v {self.__pretty_print(self.__all_solved[v])}. Tato oblast je podle premis {self.__pretty_print(common_numbers)} neprázdná."]
                        elif len(common_numbers) == 1:
                            self.__explanations[0] = [
                                f"Pro '{variable}' bylo nalezeno řešení. Existenciální predikát pro '{variable}' byl vhodný - nachází se v {self.__pretty_print(self.__all_solved[v])}. Tato oblast je podle {list(common_numbers)[0]}. premisy neprázdná."]
                        else:
                            self.__explanations[0] = [
                                f"Pro '{variable}' bylo nalezeno řešení. Existenciální predikát pro '{variable}' byl vhodný - nachází se v {self.__pretty_print(self.__all_solved[v])}."]
                        if len(self.__conclusion_solved[variable]) == 1:
                            solution['Exists within'][v].update(self.__conclusion_solved[variable])
                        return True

                if v in ['a', 'b', 'c', 'd', 'e', 'f', 'g'] and variable in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
                    if v == variable:
                        if self.__all_solved[v].issubset(set(self.__conclusion_solved[variable])):
                            self.__explanations[0] = [
                                f"Pro '{variable}' bylo nalezeno řešení. Existenciální predikát pro '{variable}' byl vhodný - nachází se v {self.__pretty_print(self.__all_solved[v])}."]
                            if len(self.__conclusion_solved[variable]) == 1:
                                solution['Exists within'][v].update(self.__conclusion_solved[variable])
                            return True
            if variable not in self.__all_solved and variable in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
                self.__explanations[0] = [
                    f"Pro '{variable}' nebylo nalezeno řešení. Konstanta '{variable}' nebyla nalezena v žádné premise."
                ]
                return False

            for c in self.__contain:
                major_set.update(c[1])
                print(self.__contain, "contains")
                print(self.__existential_solved, "existential solved!")

                print(c[1], "c1")
                print(self.__conclusion_solved[variable], "conclusion solved...")
                if len(set(c[1])) == 0:
                    return False
                if c[1].issubset(self.__conclusion_solved[variable]) and len(self.__conclusion_solved[variable]) > 0:
                    self.__explanations[0] = [
                        f"Pro '{variable}' bylo nalezeno řešení. Oblast {self.__pretty_print(c[1])} je neprázdná ({c[0]}. premisa)"]
                    if len(c[1]) != 1:
                        solution['Exists within'][variable].update(c[1])
                        solution['Bad'][variable] = c[1]
                    return True

            """if len(all_have_in_common) > 0:
                if self.__conclusion_solved[variable].issubset(all_have_in_common):
                    self.__explanations[0] = [
                        f"Pro '{variable}' bylo nalezeno řešení. Existenciální predikát pro '{variable}' byl vhodný - nachází se v {self.__pretty_print(all_have_in_common)}."]
                    solution['Exists within'][variable].update(all_have_in_common)
                    return True
            print(major_set, "major set")
            print(self.__conclusion_solved[variable], "conclusion solved")
            if major_set.issubset(self.__conclusion_solved[variable]) and len(self.__conclusion_solved[variable]) > 0:
                self.__explanations[0] = [
                    f"Pro '{variable}' bylo nalezeno řešení. {self.__pretty_print(self.__conclusion_solved[variable])} je podmnožinou {self.__pretty_print(major_set)}"]
                return True
            if len(var_set) == 0:
                print("conclusion existential", self.__conclusion_solved[variable])
                constants = []
                for v in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
                    if v in solution['Exists within'].keys():
                        if not set(solution['Exists within'][v]).isdisjoint(self.__conclusion_solved[variable]):
                            if v == self.__conclusion_variable or self.__conclusion_variable not in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
                                constants.append(v)
                if len(constants) == 0:
                    self.__explanations[0] = [
                        f"Pro '{variable}' nebylo nalezeno řešení. Žádný existenciální predikát pro '{variable}' nebyl vhodný."]
                    return False
                self.__explanations[0] = [
                    f"Pro '{variable}' bylo nalezeno řešení. Platné konstanty {', '.join(constants)}."]
                return True
"""
            # if any from var_set is in the conclusion, the problem is valid
            print("here", self.__conclusion_solved, variable, var_set)
            if not var_set.isdisjoint(self.__conclusion_solved[variable]):
                if variable in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
                    self.__explanations[0] = [
                        f"Pro '{variable}' platí, že existuje prvek, který spadá do alespoň jedné z {self.__pretty_print(self.__conclusion_solved[variable])}."]
                else:
                    self.__explanations[0] = [
                        f"Pro '{variable}' platí, že existují prvky, které spadají do alespoň jedné z {self.__pretty_print(self.__conclusion_solved[variable])}."]

                return True

            if len(c[1]) > 0:
                # get those in c[1] but not in conclusion
                extras = set(c[1]).difference(self.__conclusion_solved[variable])
                if len(extras) > 0:
                    if len(extras) == 1:
                        self.__explanations[0] = [
                            f"Podle {c[0]}. premisy existuje možnost umístění '{variable}' do oblasti {self.__pretty_print(extras)}, kde budou pravdivé předpoklady, ale nepravdivý závěr."]
                    else:
                        self.__explanations[0] = [
                            f"Podle {c[0]}. premisy existuje možnost umístění '{variable}' do oblastí {self.__pretty_print(extras)}, kde budou pravdivé předpoklady, ale nepravdivý závěr."]
                    return False

            print(self.__all_solved, "all solved")
            # tell the user which are is extra and makes the argument invalid
            self.__explanations[0] = [
                f"Pro '{variable}' neexistují žádné prvky, které by splňovaly závěr."]

            return False

        else:
            # here we solve the case in which only universal statements are provided
            # we determine the validity by checking if the areas that should be crossed out are actually crossed out
            checking = set(crossed_out) - set(self.__conclusion_solved[variable])
            print(set(self.__conclusion_solved[variable]), "conclusion solved")
            print(crossed_out, "crossed out")
            print(checking, "checking")

            if len_sum == 0 or len(checking) == 0:
                if set(self.__conclusion_solved[variable]).issubset(crossed_out):
                    if len(self.__conclusion_solved[variable]) == 1:
                        self.__explanations[0] = [
                            f"Závěr vyžaduje, aby oblast {self.__pretty_print(self.__conclusion_solved[variable])} byla nutně prázdná, což odpovídá výsledku."]
                    else:
                        self.__explanations[0] = [
                            f"Závěr vyžaduje, aby oblasti {self.__pretty_print(self.__conclusion_solved[variable])} byly nutně prázdné, což odpovídá výsledku."]
                    return True

            if not crossed_out.issubset(self.__conclusion_solved[variable]):
                print(crossed_out, "crossed out")
                print(self.__conclusion_solved[variable], "conclusion solved")
                print (self.__conclusion_solved[variable] - crossed_out, "crossed out - conclusion solved")
                if len(self.__conclusion_solved[variable] - crossed_out) > 0:
                    if len(self.__conclusion_solved[variable] - crossed_out) == 1:
                        self.__explanations[0] = [
                            f"Pro '{variable}' není řešení. Nelze zaručit, že oblast {self.__pretty_print(self.__conclusion_solved[variable] - crossed_out)} je prázdná."]
                    else:
                        self.__explanations[0] = [
                            f"Pro '{variable}' není řešení. Nelze zaručit, že oblasti {self.__pretty_print(self.__conclusion_solved[variable] - crossed_out)} jsou prázdné."]
                    return False
                # if not var_set.issubset(set(self.__conclusion_solved[variable])):
                #     self.__explanations[0] = [f"Pro '{variable}' není řešení. Existují prvky mimo výběr. {set(self.__conclusion_solved[variable]) - crossed_out}"]
                #    return False
                self.__explanations[0] = [f"Pro '{variable}' nalezeno řešení. "
                                          f"Platí že {self.__pretty_print(var_set)} není vyškrtáno a splňuje tím podmínku závěru."]
                return True

            self.__explanations[0] = [
                f"Pro '{variable}' není řešení. Aby byl závěr pravdivý, je nutné, aby byly vyšrafovány oblasti {self.__pretty_print(self.__conclusion_solved[variable])}."]
            return False

    def __pretty_print(self, param):
        matches = self.get_combinations()
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
                return "(" + str(matches.index(",".join(sorted(param)))) + ")"
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
