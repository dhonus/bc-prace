import itertools
import logging

from core.Nodes import *
from typing import List
from typing import Set as tSet


class Venn:
    def __init__(self, variables: List[str]):
        self.dict = {}
        self.explanations = {}
        self.variables = variables
        self.variables.append('μ')
        self.sets = []
        for var in self.variables:
            self.dict[var] = " "
        print(self.dict)

        self.sets = {}
        print(" -> vars", self.variables)

        self.area_combinations = []

        for i, the_set in enumerate(self.variables):
            for elem in itertools.combinations(self.variables, i+1):
                self.area_combinations.append("".join(elem))

        print(self.area_combinations, "aaa")

        for i, var in enumerate(self.variables):
            self.sets[var] = []
            for area in self.area_combinations:
                if var in area:
                    self.sets[var].append(area)

        for var in self.variables:
            self.explanations[var] = []

    def better_solve(self, tree: ExpressionTree) -> list[str]:
        print(f"---------\nsets: {self.sets}")
        print("explanations:", self.explanations)
        sol = self.__solver(tree)
        print(f"solution:: {sol}")
        print(self.area_combinations)
        sol = self.__negate(sol)
        sol_universum_accounted = list()
        # remove universe symbol from all but just itself
        # {'Aμ', 'μ', 'Bμ'} -> {'A', 'μ', 'B'}
        for item in sol:
            if item == 'μ':
                sol_universum_accounted.append(item)
                continue
            adding = item.replace("μ", "")
            if adding:
                sol_universum_accounted.append(adding)
        return sol_universum_accounted

    def existential(self, tree: Node) -> list[str]:
        print(f"---------\nexistential sets: {self.sets}")
        print("explanations:", self.explanations)
        sol = self.__solver(tree)
        print(f"solution:: {sol}")
        print(self.area_combinations)
        sol_universum_accounted = list()
        # remove universe symbol from all but just itself
        # {'Aμ', 'μ', 'Bμ'} -> {'A', 'μ', 'B'}
        for item in sol:
            if item == 'μ':
                sol_universum_accounted.append(item)
                continue
            adding = item.replace("μ", "")
            if adding:
                sol_universum_accounted.append(adding)
        return sol_universum_accounted

    def __negate(self, to_negate: List[str]):
        new_values = []
        for key, value in self.sets.items():
            for elem in value:
                if elem not in to_negate:
                    new_values.append(elem)
        print(f"negated to {new_values}")
        return new_values

    def __solver(self, node) -> List[str]:
        match node:
            case Set() as s:
                print(" -> set ", self.sets.get(s.value))
                return self.sets.get(s.value)
            case Neg() as n:
                # remove current from all possible and return new set
                left = self.__solver(n.left)
                print(" -> neg", left)
                return self.__negate(left)
            case Operation() as op:
                left = self.__solver(op.left)
                right = self.__solver(op.right)
                print(f" -> staged 2 sets {left} and {right}")
                match op.value:
                    case 'or':
                        return list(set(left + right))
                    case '>':
                        return list(set(self.__negate(left) + right))
                    case '&':
                        return [elem for elem in left and right if elem in left and right]
                    case '<>':
                        l = list(set(self.__negate(left) + right))
                        r = list(set(self.__negate(right) + left))
                        return [elem for elem in l and r if elem in l and r]
            case _:
                raise Exception(f'Unrecognised type ( {type(node).__name__} )encountered. Exiting. ')

    def get_sets(self):
        return self.sets