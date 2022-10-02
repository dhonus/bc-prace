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
        self.sets = []
        for var in self.variables:
            self.dict[var] = " "
        print(self.dict)

    def __solve(self, node) -> tSet[str]:
        pass

    def solve(self, tree: ExpressionTree) -> tSet[str]:
        pass

    def get_sets(self):
        return self.sets


class Venn2(Venn):
    def __init__(self, variables: List[str]):
        super().__init__(variables)

        self.sets = [set(), set()]
        if len(self.sets) != 2:
            raise Exception('Unknown error while generating sets. Too many found.')
        print(self.variables)
        print(self.sets)

        self.area_combinations = []

        # creates a list of all possible ways the given sets can interact
        for area in itertools.product(self.variables, self.variables):
            if area <= area[::-1]:
                if area[0] == area[1]:
                    self.area_combinations.append(area[0])
                else:
                    self.area_combinations.append(area[0] + area[1])

        # construct the list of sets from the list of variables
        for i, var in enumerate(self.variables):
            for area in self.area_combinations:
                if var in area:
                    self.sets[i].add(area)

    def solve(self, tree: ExpressionTree) -> tSet[str]:
        negation = set()
        for sets in self.sets:
            negation = negation.union(sets)
        negation = negation.difference(self.__solve(tree))
        print("solved", negation)
        return negation

    def __solve(self, node: Node) -> tSet[str]:
        match node:
            case Set() as s:
                return self.sets[self.variables.index(s.value)]
            case Neg() as n:
                left = self.__solve(n.left)
                negation = set()
                for sets in self.sets:
                    negation = negation.union(sets)
                negation = negation.difference(left)
                print(f'Staged negation {negation}')
                return negation
            case Operation() as op:
                left = self.__solve(op.left)
                right = self.__solve(op.right)
                print(f"staged 2 sets {left} and {right}")
                match op.value:
                    case 'or':
                        return left.union(right)
                    case '>':
                        print(f"returning {left.difference(right)}")
                        return left.difference(right)
                    case '&':
                        return left.intersection(right)
                    case '<>':
                        return left.symmetric_difference(right)
            case _:
                raise Exception(f'Unrecognised type ( {type(node).__name__} )encountered. Exiting. ')


class Venn3(Venn):
    def __init__(self, variables: List[str]):
        super().__init__(variables)
        self.sets = {}
        print(" -> vars", self.variables)
        # print(f"final = {self.__solve(tree)}")

        self.area_combinations = []

        # creates a list of all possible ways the given sets can interact
        for area in itertools.product(self.variables, self.variables):
            if area <= area[::-1]:
                if area[0] == area[1]:
                    self.area_combinations.append(area[0])
                else:
                    self.area_combinations.append(area[0] + area[1])

        # add Set1Set2Set3 combination
        self.area_combinations.append(self.variables[0] + self.variables[1] + self.variables[2])
        print(" -> combinations", self.area_combinations)

        # construct the list of sets from the list of variables
        for i, var in enumerate(self.variables):
            self.sets[var] = []
            for area in self.area_combinations:
                if var in area:
                    self.sets[var].append(area)

        for var in self.variables:
            self.explanations[var] = []

    def better_solve(self, tree: ExpressionTree) -> list[str]:
        # print(f"---------\nsets: {self.sets}")
        # print("explanations:", self.explanations)
        sol = self.__better_solve(tree)
        # print(f"solution:: {sol}")
        # print(self.area_combinations)

        return self.__negate(sol)

    def __negate(self, to_negate: List[str]):
        new_values = []
        for key, value in self.sets.items():
            for elem in value:
                if elem not in to_negate:
                    new_values.append(elem)
        return new_values

    def __better_solve(self, node) -> List[str]:
        match node:
            case Set() as s:
                print(" -> set ", self.sets.get(s.value))
                return self.sets.get(s.value)
            case Neg() as n:
                # remove current from all possible and return new set
                left = self.__better_solve(n.left)
                print(" -> neg", left)
                return self.__negate(left)
            case Operation() as op:
                left = self.__better_solve(op.left)
                right = self.__better_solve(op.right)
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


class Venn4(Venn):
    def __init__(self, tree: ExpressionTree, variables: List[str]):
        super().__init__(tree, variables)
        if len(self.sets) != 4:
            raise Exception('Error while generating sets.')

    def __solve(self, node) -> tSet[str]:
        pass
