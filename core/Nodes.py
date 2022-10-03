# remove when this becomes default in python (python 3.11)
# used for type annotations in constructor
from __future__ import annotations
from typing import Generator


class Node:
    def __init__(self, left: Node | None, right: Node | None, value: str):
        self.value = value
        self.left = left
        self.right = right

    def print(self):
        return f"({self.left.value})"


class ExpressionTree(Node):
    """ main node which holds the quantifier of a premise and the full subtree """
    def __init__(self, value: str, variable: str, tree: Node | None):
        super().__init__(None, None, value)
        self.variable = variable
        self.tree = tree

    def print(self):
        match self.value:
            case '∃':
                return f"Exists {self.variable} for which {self.tree.print()}"
            case '∀':
                return f"For all {self.variable} applies {self.tree.print()}"


class Set(Node):
    """ a single set. X(y) """
    def __init__(self, value: str, variable: str):
        super().__init__(None, None, value)
        self.variable = variable

    def print(self):
        return f"({self.value}({self.variable}))"


class Neg(Node):
    """ a negation node """
    def __init__(self, left: Node):
        super().__init__(left, None, "not")

    def print(self):
        return f" not " + '{' + f"{self.left.print()}" + '}'


class Operation(Node):
    """ an operation node """
    def __init__(self, left: Node | None, right: Node | None, operation: str):
        super().__init__(left, right, operation)

    def print(self):
        return f"[ {self.left.print()} {self.value} {self.right.print()} ]"


def expression_generator(string: str) -> Generator[str, None, None]:
    """ python generator for us to iterate over an expression """
    for char in string:
        yield char
    while True:
        yield '\0'


