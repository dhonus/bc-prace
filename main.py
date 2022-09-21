from expressions.Parser import Parser, EmptyInputException, InvalidExpressionException
import logging

"""
    RECURSIVE DESCENT PARSING
        https://www.youtube.com/watch?v=SToUyjAsaFk
        https://www.codeproject.com/Articles/318667/Mathematical-Expression-Parser-Using-Recursive-Des
    REMOVING LEFT RECURSION FORMULA
        https://www.csd.uwo.ca/~mmorenom/CS447/Lectures/Syntax.html/node8.html
"""

"""
SYMBOLS:        PRECEDENCE
    NOT:    !   1
    AND:    &   2  
    OR:     v   3
    IMPL:   >   4
    BICON:  <>  5
    UNI:    A
    EXI:    E
    ABS:    #

THE GRAMMAR:
    S -> Q[E]
    Q -> ∀V | ∃V
    E -> B | (E)
    B -> I | I <> B
    I -> D | D > I
    D -> C | C "|" D
    C -> N | N & C
    N -> F | !F
    F = W(V)
    V -> {a..z}
    W -> {Aa..Zz}
"""


def main() -> None:
    logging.root.setLevel(logging.INFO)
    try:
        expr = "∀x[!(S(x) > C(x)) & V(x)]"
        print(f"{expr}:")
        p = Parser(expr)
        print(p.s_rule().print())

    except EmptyInputException:
        pass
    except InvalidExpressionException as iee:
        logging.warning(iee)
    except ValueError as e:
        logging.warning("Error:", e)


if __name__ == '__main__':
    main()
