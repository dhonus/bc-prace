from core.Nodes import ExpressionTree, Set, Neg, Operation, expression_generator
import logging


class Parser:
    """ this class implements a recursive descent algorithm """
    """ each production rule of the grammar is represented by its own method """
    def __init__(self):
        self.d = {
            ' ': '',
            '⊃': '>',
            '≡': '<>',
            '¬': '!',
            '∧': '&',
            '∨': '|'
        }
        self.__expression = ""
        self.__variable = ""
        self.__expression_generator = None
        self.__current = None
        self.__position = 0
        self.__pedantic = True
        self.__parsed_count = 0
        self.__p_index = -1

    def attach(self, string: str, p_index: int):
        """ this is the method supplying the parser with a string to parse """
        for key, value in self.d.items():
            string = string.replace(key, value)
        if not string:
            raise EmptyInputException
        if string.find('Ω') != -1:
            raise Exception("Nelze použít znak Ω, je rezervován pro výpis.")
        self.__expression = string
        self.__variable = ""
        self.__expression_generator = self.__make_expression_generator()  # create generator for the parser to iterate over
        self.__current = next(self.__expression_generator)  # set current char to next in generator
        self.__p_index = p_index

    def __make_expression_generator(self):
        self.__position = 0  # position within the string being parsed.
        return expression_generator(self.__expression)

    @staticmethod
    def __pretty_error(predicate: str, p_index: int) -> str:
        """ print error including an ^ to indicate the position at which it had occurred """
        """ problematic to pass with api. To be replaced with a client-side solution """
        ret = ""
        for i, char in enumerate(predicate):
            if i == p_index:
                ret += f"Problém okolo {p_index}. pozice: '{char}'"

        return ret

    def __match(self, char: str) -> bool:
        """ check next char in generator """
        if self.__current == char:
            self.__current = next(self.__expression_generator)
            self.__advance()
            return True
        return False

    def __require(self, required: str) -> bool | ValueError:
        """ mostly used for bracket parity """
        if self.__current == required:
            self.__current = next(self.__expression_generator)
            return True

        if required == ')' or required == ']':
            if not self.__current:
                raise ValueError(f"Chybějící závorka '{required}' na {self.__position}. pozici.")
            print(self.__pretty_error(self.__expression, self.__position))
            raise ValueError(f"Očekáváno '{required}', na vstupu je ale '{self.__current}'"
                  f" Pravděpodobně chybějící závorka na {self.__position}. pozici."
                             f"\n{self.__pretty_error(self.__expression, self.__position)}")
        else:
            raise ValueError(f"Očekáváno '{required}', na vstupu je ale '{self.__current}'. Na pozici: {self.__position}"
                             f"\n{self.__pretty_error(self.__expression, self.__position)}")

    def __advance(self, amount=1):
        """ move the position pointer """
        self.__position += amount
        return

    def parse(self) -> ExpressionTree:
        """ this is the main method to get called on the expression to produce an expression tree """
        parsed = self.__s_rule()
        self.__parsed_count += 1
        if not parsed:
            raise Exception('Při parsování vstupu nastala neznámá chyba.')
        parsed.p_index = self.__p_index
        return parsed

    # S -> Q[E]
    def __s_rule(self) -> ExpressionTree | None:
        expr = self.__q_rule()
        if expr.variable is None:
            # we assume that this is a constant
            # form like B(a) instead of Ex[B(x)]
            # constants behave differently to regular expressions
            # a variable of a constant is shared among other constants with any variable
            expr.constant = True
            # we now have to backtrack because we have eaten up the first 2 chars
            self.__expression_generator = self.__make_expression_generator()
            self.__current = next(self.__expression_generator)
            expr.tree = self.__e_rule(expr.constant)
            expr.variable = self.__variable
            if expr.variable not in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
                raise Exception(f"Pro konstanty jsou vyhrazenny proměnné [a..g], '{expr.variable}' nespadá do tohoto intervalu.")

            if self.__current:
                raise Exception(f"Chybějící kvantifikátor, nejedná se o konstantu.")
            return expr
        elif expr.variable in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
            raise Exception(f"Proměnná '{expr.variable}' je rezervována pro konstanty.")
        if self.__match('['):
            tree = self.__e_rule(False)
            if not tree:
                return None
            expr.tree = tree
            self.__require(']')
            if self.__current:
                prev = self.__current
                self.__current = next(self.__expression_generator)
                if self.__current == "∃" or self.__current == "∀":
                    raise ValueError("Byla ukončena, ale byl nalezen kvantifikátor. Pouze jeden predikát na řádek.")
                raise ValueError(f"Byla ukončena, ale nalezen znak '{prev}'. Pouze jeden predikát na řádek.")

        else:
            raise Exception(f"Není uzavřena hranatými závorkami.")
        return expr

    def __set_variable(self, var: str):
        if var == self.__variable:
            return
        if not self.__variable:
            self.__variable = var
            return
        raise Exception(f"Nalezeny 2 různé proměnné ve výrazu -> '{self.__variable}' a '{var}'")

    # refer to grammar in the thesis text
    # Q -> ∀V | ∃V
    def __q_rule(self) -> ExpressionTree | None:
        """ each quantifier different rules """
        elem = self.__current
        match elem:
            case '∃' | 'E':
                self.__current = next(self.__expression_generator)
                if self.__current == '(':
                    return ExpressionTree(value='∃', variable=None, tree=None)
                variable = self.__current
                if not variable:
                    raise ValueError('Chybí proměnná.')

                if not variable.islower() and self.__pedantic:
                    raise ValueError('Proměnná by měla být malým písmem. Možná jste zapomněli na závorku?')
                self.__current = next(self.__expression_generator)
                self.__advance(2)
                return ExpressionTree(value='∃', variable=variable, tree=None)
            case '∀' | 'A':
                self.__current = next(self.__expression_generator)
                if self.__current == '(':
                    return ExpressionTree(value='∃', variable=None, tree=None)
                variable = self.__current
                if not variable:
                    raise ValueError('Chybí proměnná.')

                if not variable.islower() and self.__pedantic:
                    raise ValueError('Proměnná by měla být malým písmem. Možná jste zapomněli na závorku?')
                self.__current = next(self.__expression_generator)
                self.__advance(2)
                return ExpressionTree(value='∀', variable=variable, tree=None)
            case _:
                return ExpressionTree(value='∃', variable=None, tree=None)

    # E -> B # this is done because we can only have one expression
    def __e_rule(self, constant: bool) -> Operation | None:
        left = self.__b_rule()
        if not left:
            return None
        return left

    #  B -> I | I <> B
    def __b_rule(self) -> Operation | None:
        left = self.__i_rule()
        if not left:
            return None
        if self.__match('<'):
            if self.__require('>'):
                self.__advance()
                right = self.__b_rule()
                if right:
                    return Operation(left, right, '<>')
            return None
        return left

    # I -> D | D > I
    def __i_rule(self) -> Operation | None:
        left = self.__d_rule()
        if not left:
            return None
        if self.__match('>'):
            right = self.__i_rule()
            if right:
                return Operation(left, right, '>')
        return left

    # D -> C | C '|' D
    def __d_rule(self) -> Operation | None:
        left = self.__c_rule()
        if not left:
            return None
        if self.__match('|'):
            right = self.__d_rule()
            if right:
                return Operation(left, right, 'or')
        return left

    # C -> N | N & C
    def __c_rule(self) -> Operation | Set | Neg | None:
        left = self.__neg_rule()
        if not left:
            return None
        if self.__match('&'):
            right = self.__c_rule()
            if right:
                return Operation(left, right, '&')
        return left

    # N -> F | !F
    def __neg_rule(self) -> Set | Neg | None:
        if self.__match('!'):
            left = self.__f_rule()
            if not left:
                return None
            return Neg(left)
        self.__advance()
        left = self.__f_rule()
        return left

    # F = W(V) | W[V]
    def __f_rule(self) -> Set | None:
        if self.__match('['):
            right = self.__b_rule()
            if self.__require(']'):
                self.__advance()
                return right
            return None
        if self.__match('('):
            right = self.__b_rule()
            if self.__require(')'):
                self.__advance()
                return right
            return None

        self.__advance()

        set_name_length_limit = 15
        elem = self.__current
        self.__current = next(self.__expression_generator)
        if not elem.isupper():
            if elem.islower():
                raise TypeError(f"Jméno objektu musí začínat velkým písmenem. Neznámý znak '{elem}' na pozici {self.__position}."
                                f"\n{self.__pretty_error(self.__expression, self.__position)}")
            raise TypeError(f"Nelze identifikovat znak '{elem}' na {self.__position}. pozici. Očekáván literál."
                            f"\n{self.__pretty_error(self.__expression, self.__position)}")
        length = 0
        while not self.__match('('):
            if not self.__current.islower():
                logging.warning("f_rule violated uppercase")
                if self.__expression[0] not in ["A", "E", "∀", "∃"]:
                    raise ValueError(
                        f"Zakázaný znak '{self.__current}' uvnitř jména objektu. Očekáváno velké písmeno následováno pouze malými."
                        f"\n{self.__pretty_error(self.__expression, self.__position)}. Je možné, že jste uvedli špatný kvalifikátor?")
                raise ValueError(f"Zakázaný znak '{self.__current}' uvnitř jména objektu. Očekáváno velké písmeno následováno pouze malými."
                                 f"\n{self.__pretty_error(self.__expression, self.__position)}")
            elem += self.__current
            self.__advance()
            self.__current = next(self.__expression_generator)
            length += 1
            if length == set_name_length_limit:
                raise ValueError(f"Maximální přípustná délka názvu objektu je {set_name_length_limit} znaků. "
                                 f"Překročeno, nebo chybějící závorka.\n{self.__pretty_error(self.__expression, self.__position)}")
        if not self.__current.islower():
            logging.warning("f_rule violated lowercase")
            if self.__pedantic:
                raise ValueError(f"Proměnná na pozici {self.__position} by měla být malým písmem, "
                                 f"ale bylo nalezeno '{self.__current}'.\n{self.__pretty_error(self.__expression, self.__position)}")
        variable = self.__current.lower()
        self.__set_variable(variable)
        self.__current = next(self.__expression_generator)
        try:
            self.__require(')')
        except ValueError:
            raise ValueError(f"Nalezen znak '{self.__current}'. Zde by měla být ukončovací závorka, jelikož proměnné "
                             f"musí být ve tvaru jednoho písmene.")
        logging.debug(f"returning set {elem}({variable})")

        return Set(elem, variable)


class InvalidExpressionException(Exception):
    """ raised when the expression_generator fails to produce a valid expression """
    pass


class EmptyInputException(Exception):
    """ empty input string """
    pass
