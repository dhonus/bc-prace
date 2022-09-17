from typing import Generator


class Node:
    def __init__(self, left, right, value: str):
        self.value = value
        self.left = left
        self.right = right

    def print(self):
        return f"({self.left.value})"


class Quantifier(Node):
    """ main node which holds the quantifier of a premise and the full subtree """
    def __init__(self, value: str, variable: str, tree: Node):
        self.value = value
        self.variable = variable
        self.tree = tree

    def print(self):
        match self.value:
            case '∃':
                print(f"Exists {self.variable} for which {self.tree.print()} is true")
            case '∀':
                print(f"For all {self.variable} applies {self.tree.print()}")


class Set(Node):
    """ a single set. X(y) """
    def __init__(self, left, right, value: str, variable: str):
        self.value = value
        self.variable = variable
        self.left = left
        self.right = right

    def print(self):
        return f"({self.value}({self.variable}))"


class Operation(Node):
    """ an operation node """
    def __init__(self, left: Node, right: Node, operation: str):
        self.operation = operation
        self.left = left
        self.right = right

    def print(self):
        return f"({self.left.print()} {self.operation} {self.right.print()})"


def lexer(string: str) -> Generator[str, None, None]:
    """ python generator for us to iterate over an expression """
    for char in string:
        yield char
    while True:
        yield '\0'


class Parser:
    """ this class implements a recursive descent algorithm """
    """ each production rule of the grammar is represented by its own method """
    def __init__(self, string: str):
        string = string.replace(" ", "")  # remove whitespace
        if not string:
            raise EmptyInputException
            return None
        self.expression_generator = lexer(string)  # create python generator for the parser to iterate over
        self.current = next(self.expression_generator)  # set current char to next in generator

    def accept(self, char: str) -> bool:
        """ check next char in generator """
        if self.current == char:
            self.current = next(self.expression_generator)
            return True
        return False

    def expect(self, char: str) -> bool:
        """ mostly used for bracket parity """
        if self.current == char:
            self.current = next(self.expression_generator)
            return True
        print(f"Error, expected {char}")
        return False

    def quantifier(self) -> Quantifier:
        """ each quantifier different rules """
        """ to be implemented """
        elem = self.current
        self.current = next(self.expression_generator)
        match elem:
            case '∃':
                variable = self.current
                self.current = next(self.expression_generator)
                return Quantifier(value='∃', variable=variable, tree=None)
            case '∀':
                variable = self.current
                self.current = next(self.expression_generator)
                return Quantifier(value='∀', variable=variable, tree=None)
            case _:
                return None

    # S -> Q[E]
    def s(self) -> Quantifier:
        expr = self.quantifier()
        if self.accept('['):
            tree = self.e()
            if not tree:
                return None
            expr.tree = tree
        return expr

    # E -> GOG | (E)
    def e(self) -> Operation:
        g = self.g()
        if not g:
            return None
        op = self.o(g)
        if not op:
            return g
        right = g
        if not right:
            return None
        op.right = right
        return op

    # G -> FG' | (G) | (GOG) | F
    def g(self) -> Node:
        # print("calling g")
        left = self.f()
        if not left:
            return None
        # print(left.value)
        if self.accept(']'):
            # print("found final expression")
            return left

        gg = self.gg(left)
        if not gg:
            return left
        # print("returning gg")
        return gg

    # G'-> OGG' | epsilon
    def gg(self, left):
        # print("calling gg")
        op = self.o(left)
        if not op:
            return None
        g = self.g()
        if not g:
            return None
        op.right = g
        next_operation = self.o(op)
        if not next_operation:
            return op
        right = self.g()
        if not right:
            return None
        next_operation.right = right
        return next_operation

    # F -> W(V) | ~F | (F)
    def f(self):
        elem = self.current
        self.current = next(self.expression_generator)
        if not elem.isupper():
            return None
        # print("returning node")
        self.expect('(')
        variable = self.current
        self.current = next(self.expression_generator)
        self.expect(')')
        return Set(None, None, elem, variable)

    # O -> > | <> | & | v
    def o(self, left):
        operation = self.current
        self.current = next(self.expression_generator)
        match operation:
            case '>':
                return Operation(left, None, 'implies')
            case '<':
                if self.accept('>'):
                    return Operation(left, None, 'is biconditional with')
                return None
            case '&':
                return Operation(left, None, 'and')
            case 'v':
                return Operation(left, None, 'or')
            case _:
                if self.current not in {'(', ')', '∀', '∃'}:
                    return None
                raise InvalidExpressionException


class InvalidExpressionException(Exception):
    """ raised when the lexer fails to produce a valid expression """
    pass


class EmptyInputException(Exception):
    """ empty input string """
    pass
