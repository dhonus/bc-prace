from typing import Generator

"""
TBA:
    operator precedence -> add rules to grammar to reflect valid logic
    bracket support and parity check
    bracket negation
    expression parsing unit tests
"""

class Node:
    def __init__(self, left, right, value: str):
        self.value = value
        self.left = left
        self.right = right

    def print(self):
        return f"({self.left.value})"


class Quantifier(Node):
    """ main node which holds the quantifier of a premise and the full subtree """
    def __init__(self, value: str, variable: str, tree: Node | None):
        super().__init__(None, None, value)
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
        super().__init__(left, right, value)
        self.variable = variable

    def print(self):
        return f"({self.value}({self.variable}))"


class Neg(Node):
    def __init__(self, left, right, value: str):
        super().__init__(left, right, value)

    def print(self):
        return f"( not ({self.left.print()}))"


class Operation(Node):
    """ an operation node """
    def __init__(self, left: Node | None, right: Node | None, operation: str):
        super().__init__(left, right, operation)

    def print(self):
        return f"'{self.left.print()}' {self.value} .{self.right.print()}."


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
        self.expression_generator = lexer(string)  # create python generator for the parser to iterate over
        self.current = next(self.expression_generator)  # set current char to next in generator
        self.position = 0  # position within the string being parsed.

    def accept(self, char: str) -> bool:
        """ check next char in generator """
        if self.current == char:
            self.current = next(self.expression_generator)
            self.advance()
            return True
        return False

    def expect(self, char: str) -> bool:
        """ mostly used for bracket parity """
        if self.current == char:
            self.current = next(self.expression_generator)
            return True
        print(f"Error: expected '{char}', but got '{self.current}' instead. Happened at position: {self.position}")
        return False

    def advance(self, amount=1):
        self.position += amount

    def quantifier(self) -> Quantifier:
        """ each quantifier different rules """
        """ to be implemented """
        elem = self.current
        self.current = next(self.expression_generator)
        match elem:
            case '∃':
                variable = self.current
                self.current = next(self.expression_generator)
                self.advance(2)
                return Quantifier(value='∃', variable=variable, tree=None)
            case '∀':
                variable = self.current
                self.current = next(self.expression_generator)
                self.advance(2)
                return Quantifier(value='∀', variable=variable, tree=None)
            case _:
                raise ValueError('No quantifier found. The input must be a closed formula.')

    # S -> Q[E]
    def s_rule(self) -> Quantifier | None:
        print("S:")
        expr = self.quantifier()
        if self.accept('['):
            self.advance()
            tree = self.e_rule()
            if not tree:
                return None
            expr.tree = tree
        return expr

    # E -> GOG | (E)
    def e_rule(self) -> Operation | None:
        print("E:")
        left = self.g_rule()
        if not left:
            return None
        op = self.o_rule(left)
        if not op:
            return left
        op.right = self.g_rule()
        return op

    # G -> !G | FG' | (G) | (GOG)  | F
    def g_rule(self) -> Node | None:
        print("G:")
        # print("calling g")
        left = self.f_rule()
        if not left:
            return None
        # print(left.value)
        if self.accept(']'):
            # print("found final expression")
            return left

        op = self.gg_rule(left)
        if not op:
            raise ValueError(f"Malformed input: Missing ending ']' parenthesis at position {self.position}")
        print("returning op ", type(op.left), op.value, type(op.right))
        return op

    # G'-> OGG' | epsilon
    def gg_rule(self, left: Node) -> Node | None:
        print("G':")
        op = self.o_rule(left)
        if not op:
            return left
        g = self.g_rule()
        if not g:
            return None
        op.right = g
        next_it = self.gg_rule(op)
        if not next_it:
            return op
        """
        next_operation = self.o_rule(op)
        if not next_operation:
            return op
        right = self.g_rule()
        if not right:
            return None
        next_operation.right = right
        return next_operation
        """
        return next_it

    # F -> W(V) | !F | (F)
    def f_rule(self) -> Set | Neg | None:
        print("F:")
        if self.accept('!'):
            left = self.f_rule()
            if not left:
                return None
            return Neg(left, None, "not")
        set_name_length_limit = 15
        elem = self.current
        self.current = next(self.expression_generator)
        if not elem.isupper():
            return None
        len = 0
        while not self.accept('(') :
            if not self.current.islower():
                raise ValueError(f"Illegal character ({self.current}) within set name.")
            elem += self.current
            self.advance()
            self.current = next(self.expression_generator)
            len += 1
            if len == set_name_length_limit:
                raise ValueError(f"The maximum length of a set name is {set_name_length_limit} characters. "
                                 f"Exceeded, or no opening parenthesis found.")
        if not self.current.islower():
            raise ValueError(f"Expected lowercase variable in parentheses at position {self.position}, but got '{self.current}' instead.")
        variable = self.current
        self.current = next(self.expression_generator)
        self.expect(')')
        print(elem)
        return Set(None, None, elem, variable)

    # O -> > | <> | & | v
    def o_rule(self, left: Node) -> Operation | None:
        print("O:")
        operation = self.current
        self.current = next(self.expression_generator)
        print(operation)
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
