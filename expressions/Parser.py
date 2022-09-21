from expressions.Nodes import Node, Quantifier, Set, Neg, Operation, lexer
import logging


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

    def require(self, req: str) -> bool:
        """ mostly used for bracket parity """
        if self.current == req:
            self.current = next(self.expression_generator)
            return True
        if req == ')':
            print(f"Error: '{req}' required, but got '{self.current}' instead."
                  f" Probably a missing closing bracket. Happened at position: {self.position}")
        else:
            print(f"Error: '{req}' required, but got '{self.current}' instead. Happened at position: {self.position}")
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
        expr = self.quantifier()
        if self.accept('['):
            self.advance()
            tree = self.e_rule()
            if not tree:
                return None
            expr.tree = tree
            self.require(']')
        return expr

    # E -> B | (E)
    def e_rule(self) -> Operation | None:
        left = self.b_rule()
        self.advance()
        if not left:
            return None
        return left

    #  B -> I | I <> B
    def b_rule(self) -> Operation | None:
        left = self.i_rule()
        if not left:
            return None
        if self.accept('<'):
            self.advance()
            if self.require('>'):
                self.advance()
                right = self.b_rule()
                if right is not None:
                    return Operation(left, right, '<>')
            return None
        return left

    # I -> D | D > I
    def i_rule(self) -> Operation | None:
        left = self.d_rule()
        if not left:
            return None
        if self.accept('>'):
            self.advance()
            right = self.i_rule()
            if right is not None:
                return Operation(left, right, '>')
        return left

    # D -> C | C "|" D
    def d_rule(self) -> Operation | None:
        left = self.c_rule()
        if not left:
            return None
        if self.accept('|'):
            self.advance()
            right = self.d_rule()
            if right is not None:
                return Operation(left, right, 'or')
        return left

    # C -> N | N & C
    def c_rule(self) -> Operation | None:
        left = self.neg_rule()
        if not left:
            return None
        if self.accept('&'):
            self.advance()
            right = self.c_rule()
            if right is not None:
                return Operation(left, right, '&')
        return left

    # N -> F | !F
    def neg_rule(self) -> Set | Neg | None:
        if self.accept('!'):
            self.advance()
            left = self.f_rule()
            if not left:
                return None
            return Neg(left)
        left = self.f_rule()
        return left

    # F = W(V)
    def f_rule(self) -> Set | None:
        if self.accept('('):
            self.advance()
            right = self.b_rule()
            if self.require(')'):
                self.advance()
                return right
            return None

        self.advance()

        set_name_length_limit = 15
        elem = self.current
        self.current = next(self.expression_generator)
        if not elem.isupper():
            return None
        length = 0
        while not self.accept('(') :
            if not self.current.islower():
                logging.warning("f_rule bracket")
                raise ValueError(f"Illegal character ({self.current}) within set name.")
            elem += self.current
            self.advance()
            self.current = next(self.expression_generator)
            length += 1
            if length == set_name_length_limit:
                raise ValueError(f"The maximum length of a set name is {set_name_length_limit} characters. "
                                 f"Exceeded, or no opening parenthesis found.")
        if not self.current.islower():
            raise ValueError(f"required lowercase variable in parentheses at position {self.position}, but got '{self.current}' instead.")
        variable = self.current
        self.current = next(self.expression_generator)
        self.require(')')
        logging.debug(f"returning set {elem}({variable})")
        return Set(None, None, elem, variable)


class InvalidExpressionException(Exception):
    """ raised when the lexer fails to produce a valid expression """
    pass


class EmptyInputException(Exception):
    """ empty input string """
    pass
