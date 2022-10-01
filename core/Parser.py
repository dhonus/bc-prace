from core.Nodes import ExpressionTree, Set, Neg, Operation, expression_generator
import logging


class Parser:
    """ this class implements a recursive descent algorithm """
    """ each production rule of the grammar is represented by its own method """
    def __init__(self, string: str):
        string = string.replace(" ", "")  # remove whitespace
        if not string:
            raise EmptyInputException
        self.expression = string
        self.expression_generator = expression_generator(string)  # create generator for the parser to iterate over
        self.current = next(self.expression_generator)  # set current char to next in generator
        self.position = 0  # position within the string being parsed.
        self.pedantic = True  # forces usage of stricter syntax

    def __pretty_error(self, predicate: str, p_index: int) -> str:
        pos_indicator = ""
        for i, char in enumerate(predicate):
            if i == p_index - 1:
                pos_indicator += "^"
                continue
            pos_indicator += " "
        return predicate + '\n' + pos_indicator


    def match(self, char: str) -> bool:
        """ check next char in generator """
        if self.current == char:
            self.current = next(self.expression_generator)
            self.advance()
            return True
        return False

    def require(self, req: str) -> bool | ValueError:
        """ mostly used for bracket parity """
        if self.current == req:
            self.current = next(self.expression_generator)
            return True

        if req == ')':
            print(self.__pretty_error(self.expression, self.position))
            raise ValueError(f"Error: '{req}' required, but got '{self.current}' instead."
                  f" Probably a missing closing bracket. Occurred at position: {self.position}"
                             f"\n{self.__pretty_error(self.expression, self.position)}")
        else:
            raise ValueError(f"Error: '{req}' required, but got '{self.current}' instead. Happened at position: {self.position}"
                             f"\n{self.__pretty_error(self.expression, self.position)}")

    def advance(self, amount=1):
        print(f"advanced {self.expression[self.position]}")
        self.position += amount

    def parse(self) -> ExpressionTree:
        parsed = self.s_rule()
        if not parsed:
            raise Exception('Unknown error occurred while parsing expression.')
        return parsed

    # S -> Q[E]
    def s_rule(self) -> ExpressionTree | None:
        expr = self.q_rule()
        if self.match('['):
            tree = self.e_rule()
            if not tree:
                return None
            expr.tree = tree
            self.require(']')
        return expr

    # Q -> ∀V | ∃V
    def q_rule(self) -> ExpressionTree:
        """ each quantifier different rules """
        """ to be implemented """
        elem = self.current
        self.current = next(self.expression_generator)
        match elem:
            case '∃':
                variable = self.current
                if not variable.islower() and self.pedantic:
                    raise ValueError('Pedantic: Lowercase variable expected to follow quantifier.')
                self.current = next(self.expression_generator)
                self.advance(2)
                return ExpressionTree(value='∃', variable=variable, tree=None)
            case '∀':
                variable = self.current
                if not variable.islower() and self.pedantic:
                    raise ValueError('Pedantic: Lowercase variable expected to follow quantifier.')
                self.current = next(self.expression_generator)
                self.advance(2)
                return ExpressionTree(value='∀', variable=variable, tree=None)
            case _:
                raise ValueError('No quantifier found. The input must be a closed formula.')

    # E -> B # this is done because we can only have one expression
    def e_rule(self) -> Operation | None:
        left = self.b_rule()
        if not left:
            return None
        return left

    #  B -> I | I <> B
    def b_rule(self) -> Operation | None:
        left = self.i_rule()
        if not left:
            return None
        if self.match('<'):
            if self.require('>'):
                self.advance()
                right = self.b_rule()
                if right:
                    return Operation(left, right, '<>')
            return None
        return left

    # I -> D | D > I
    def i_rule(self) -> Operation | None:
        left = self.d_rule()
        if not left:
            return None
        if self.match('>'):
            right = self.i_rule()
            if right:
                return Operation(left, right, '>')
        return left

    # D -> C | C '|' D
    def d_rule(self) -> Operation | None:
        left = self.c_rule()
        if not left:
            return None
        if self.match('|'):
            right = self.d_rule()
            if right:
                return Operation(left, right, 'or')
        return left

    # C -> N | N & C
    def c_rule(self) -> Operation | Set | Neg | None:
        left = self.neg_rule()
        if not left:
            return None
        if self.match('&'):
            right = self.c_rule()
            if right:
                return Operation(left, right, '&')
        return left

    # N -> F | !F
    def neg_rule(self) -> Set | Neg | None:
        if self.match('!'):
            left = self.f_rule()
            if not left:
                return None
            return Neg(left)
        self.advance()
        left = self.f_rule()
        return left

    # F = W(V)
    def f_rule(self) -> Set | None:
        if self.match('('):
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
            if elem.islower():
                raise TypeError(f"Lowercase literal. Failed to identify token '{elem}' at position {self.position}."
                                f"\n{self.__pretty_error(self.expression, self.position)}")
            raise TypeError(f"Failed to identify token '{elem}' at position {self.position}. Expected a literal."
                            f"\n{self.__pretty_error(self.expression, self.position)}")
        length = 0
        while not self.match('('):
            if not self.current.islower():
                logging.warning("f_rule violated uppercase")
                raise ValueError(f"Illegal character '{self.current}' within set name. All capital letters required."
                                 f"\n{self.__pretty_error(self.expression, self.position)}")
            elem += self.current
            self.advance()
            self.current = next(self.expression_generator)
            length += 1
            if length == set_name_length_limit:
                raise ValueError(f"The maximum length of a set name is {set_name_length_limit} characters. "
                                 f"Exceeded, or no opening parenthesis found.\n{self.__pretty_error(self.expression, self.position)}")
        if not self.current.islower():
            logging.warning("f_rule violated lowercase")
            if self.pedantic:
                raise ValueError(f"Pedantic: Required lowercase variable in parentheses at position {self.position}, "
                                 f"but got '{self.current}' instead.\n{self.__pretty_error(self.expression, self.position)}")
        variable = self.current.lower()
        self.current = next(self.expression_generator)
        self.require(')')
        logging.debug(f"returning set {elem}({variable})")

        return Set(elem, variable)


class InvalidExpressionException(Exception):
    """ raised when the expression_generator fails to produce a valid expression """
    pass


class EmptyInputException(Exception):
    """ empty input string """
    pass
