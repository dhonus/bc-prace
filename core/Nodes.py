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

    def validate(self, variable: str):
        self.left.validate(variable)
        self.right.validate(variable)


class ExpressionTree(Node):
    """ main node which holds the quantifier of a premise and the full subtree """
    def __init__(self, value: str, variable: str | None, tree: Node | None):
        super().__init__(None, None, value)
        self.variable = variable
        self.tree = tree
        self.constant = False
        self.p_index = -1

    def print(self):
        match self.value:
            case '∃':
                return f"Existuje {self.variable}, pro které platí že {self.tree.print()}"
            case '∀':
                return f"Pro všechna {self.variable} platí, že {self.tree.print()}"

    def validate(self):
        self.tree.validate(self.variable)


class Set(Node):
    """ a single set. e.g. X(y) """
    def __init__(self, value: str, variable: str):
        super().__init__(None, None, value)
        self.variable = variable

    def print(self):
        return f"({self.value} vázané na {self.variable}))"

    def validate(self, variable: str):
        if self.variable != variable:
            raise Exception(f'Neshodují se proměnné/konstanty {self.variable} a {variable}')


class Neg(Node):
    """ a negation node """
    def __init__(self, left: Node):
        super().__init__(left, None, "not")

    def print(self):
        return f" nejsou " + '{' + f"{self.left.print()}" + '}'

    def validate(self, variable: str):
        pass


class Operation(Node):
    """ an operation node """
    def __init__(self, left: Node | None, right: Node | None, operation: str):
        super().__init__(left, right, operation)
        self.text_value = self.value
        match self.value:
            case '>':
                self.text_value = 'implikuje'
            case '<>':
                self.text_value = 'je ekvivalentní'
            case '&':
                self.text_value = 'a'
            case '|':
                self.text_value = 'nebo'

    def print(self):
        return f"[ {self.left.print()} {self.text_value} {self.right.print()} ]"


def expression_generator(string: str) -> Generator[str, None, None]:
    """ python generator for us to iterate over an expression """
    for char in string:
        yield char
    while True:
        yield None
