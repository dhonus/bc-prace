import itertools
import logging

from core.Nodes import *
from typing import List
from typing import Set as tSet


class Venn:
    def __init__(self, variables: List[str]):
        self.dict = {}
        self.variables = variables
        for var in self.variables:
            self.dict[var] = " "
        print(self.dict)

        self.sets = [set(), set(), set()]
        area_combinations = []

        # creates a list of all possible ways the given sets can interact
        for area in itertools.product(self.variables, self.variables):
            if area <= area[::-1]:
                if area[0] == area[1]:
                    area_combinations.append(area[0])
                else:
                    area_combinations.append(area[0] + area[1])

        # add Set1Set2Set3 combination
        area_combinations.append(self.variables[0] + self.variables[1] + self.variables[2])
        print(":", area_combinations)

        # construct the list of sets from the list of variables
        for i, var in enumerate(self.variables):
            for area in area_combinations:
                if var in area:
                    self.sets[i].add(area)

    def __solve(self, node) -> tSet[str]:
        pass

    def solve(self, tree: ExpressionTree) -> tSet[str]:
        pass


class Venn2(Venn):
    def __init__(self, variables: List[str]):
        super().__init__(variables)
        if len(self.sets) != 2:
            raise Exception('Error while generating sets.')

    def __solve(self, node) -> tSet[str]:
        pass


class Venn3(Venn):
    def __init__(self, variables: List[str]):
        super().__init__(variables)
        if len(self.sets) != 3:
            raise Exception('Unknown error while generating sets. Too many found.')
        print(self.variables)
        print(self.sets)

    def solve(self, tree: ExpressionTree) -> tSet[str]:
        return self.__solve(tree)

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


class Venn4(Venn):
    def __init__(self, tree: ExpressionTree, variables: List[str]):
        super().__init__(tree, variables)
        if len(self.sets) != 4:
            raise Exception('Error while generating sets.')

    def __solve(self, node) -> tSet[str]:
        pass
