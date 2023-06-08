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
        self.variables.append('Ω')
        self.sets = []
        for var in self.variables:
            self.dict[var] = " "

        self.sets = {}
        self.area_combinations = []

        for i, the_set in enumerate(self.variables):
            for elem in itertools.combinations(self.variables, i+1):
                self.area_combinations.append(elem)

        for i, var in enumerate(self.variables):
            self.sets[var] = []
            for area in self.area_combinations:
                if var in area:
                    self.sets[var].append(area)

        for var in self.variables:
            self.explanations[var] = []

    def universal(self, tree: ExpressionTree) -> list[str]:
        sol = self.__solver(tree.tree)
        sol = self.__negate(sol)

        sol_universum_accounted = list()
        # remove universe symbol from all but just itself
        # {'AΩ', 'Ω', 'BΩ'} -> {'A', 'Ω', 'B'}
        for item in sol:
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
                pass # not in tuple
            adding = item
            if adding:
                sol_universum_accounted.append(adding)
        print(set(sol_universum_accounted), ";))")
        return sol_universum_accounted

    def existential(self, tree: ExpressionTree) -> list[str]:
        # print(f"---------\nexistential sets: {self.sets}")
        # print("explanations:", self.explanations)

        # deal with the tree
        solution = self.__solver(tree.tree)

        sol_universum_accounted = list()

        # remove universe symbol from all but just itself
        # {'AΩ', 'Ω', 'BΩ'} -> {'A', 'Ω', 'B'}
        print ("solution", solution)
        for item in solution:
            try:
                idx = item.index('Ω')
                if idx == 0 and len(item) == 1:
                    sol_universum_accounted.append(item)
                    continue
                item = item[:idx] + item[idx + 1:]
            except ValueError:
                pass # not in tuple
            adding = item
            if adding:
                sol_universum_accounted.append(adding)

        print ("sol_universum_accounted", sol_universum_accounted)
        return sol_universum_accounted

    def __negate(self, to_negate: List[str]):
        new_values = []
        for key, value in self.sets.items():
            for elem in value:
                if elem not in to_negate:
                    new_values.append(elem)
        # print(f"negated to {new_values}")
        return new_values

    def __solver(self, node) -> List[str]:
        """ solver common for both existential and universal """
        match node:
            case Set() as s:
                print(" -> set ", self.sets.get(s.value))
                return self.sets.get(s.value)
            case Neg() as n:
                # remove current from all possible and return new set
                left = self.__solver(n.left)
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