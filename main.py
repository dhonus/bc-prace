from expressions.Parser import Parser, EmptyInputException, InvalidExpressionException
import logging

"""
    RECURSIVE DESCENT PARSING
        https://www.youtube.com/watch?v=SToUyjAsaFk
        https://www.codeproject.com/Articles/318667/Mathematical-Expression-Parser-Using-Recursive-Des
        https://en.wikipedia.org/wiki/Recursive_descent_parser
    REMOVING LEFT RECURSION FORMULA
        https://www.csd.uwo.ca/~mmorenom/CS447/Lectures/Syntax.html/node8.html
    LOGIC
        https://en.wikipedia.org/wiki/Logical_biconditional
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
    D -> C | C '|' D
    C -> N | N & C
    N -> F | !F
    F = W(V)
    V -> [a..z]
    V' -> VV' | eps
    W -> [A..Z] V'
"""


def main() -> None:
    logging.root.setLevel(logging.INFO)
    predicates = [
        "∀x[!(S(x) > C(x)) & V(x)]",
        "∀x[(S(x) & B(x)) > V(x)",
        "∃x[S(x) | B(x) & C(x) & V(x)]"
    ]
    predicates = [p.replace(" ", "") for p in predicates]

    try:
        p_index = 1
        for predicate in predicates:
            print(f"{predicate}:")
            p = Parser(predicate)
            print(p.s_rule().print())
            p_index += 1

    except EmptyInputException:
        pass
    except InvalidExpressionException as iee:
        print(iee)
    except ValueError as e:
        logging.critical(f"Error: In predicate {p_index}: {e}")


if __name__ == '__main__':
    main()
