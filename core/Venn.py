import itertools

from core.Nodes import *
from typing import List


class Venn:
    def __init__(self, tree: ExpressionTree, variables: List[str]):
        self.dict = {}
        self.variables = variables
        for var in self.variables:
            self.dict[var] = " "
        print(self.dict)
        self.tree = tree

        self.sets = [set(), set(), set()]
        area_combinations = []
        # creates a list of all possible ways the given sets can interact
        for area in itertools.product(self.variables, self.variables):
            if area <= area[::-1]:
                if area[0] == area[1]:
                    area_combinations.append(area[0])
                else:
                    area_combinations.append(area[0] + area[1])

        for i, var in enumerate(self.variables):
            for area in area_combinations:
                if var in area:
                    self.sets[i].add(area)


    def solve(self, node):
        pass


class Venn2(Venn):
    def __init__(self, tree: ExpressionTree, variables: List[str]):
        super().__init__(tree, variables)
        if len(self.sets) != 2:
            raise Exception('Error while generating sets.')

    def solve(self, node):
        pass


class Venn3(Venn):
    def __init__(self, tree: ExpressionTree, variables: List[str]):
        super().__init__(tree, variables)
        if len(self.sets) != 3:
            raise Exception('Error while generating sets.')
        print(self.variables)
        print(self.sets)
        self.solve(tree)

    def solve(self, node) -> Node | None:
        match node:
            case None:
                return None
            case Operation() as op:
                self.solve(node.left)
                match op.value:
                    case '|':
                        print("or")
                        self.sets[self.variables.index(op.left.value)].union(self.sets[self.variables.index(op.right.value)])
                    case '>':
                        print("impl")
                        print(op.right.value)


class Venn4(Venn):
    def __init__(self, tree: ExpressionTree, variables: List[str]):
        super().__init__(tree, variables)
        if len(self.sets) != 4:
            raise Exception('Error while generating sets.')

    def solve(self, node):
        pass
