from expressions.Nodes import  Parser, EmptyInputException, InvalidExpressionException

"""
    RECURSIVE DESCENT PARSING
        https://www.youtube.com/watch?v=SToUyjAsaFk
        https://www.codeproject.com/Articles/318667/Mathematical-Expression-Parser-Using-Recursive-Des
    REMOVING LEFT RECURSION FORMULA
        https://www.csd.uwo.ca/~mmorenom/CS447/Lectures/Syntax.html/node8.html
"""

"""
SYMBOLS:        PRECEDENCE
    NOT:    ~   1
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
    E -> EOE | FOF | (E)
    V -> {a..z}
    W -> {Aa..Zz}
    F -> W(V) | ~F | (F)
    O -> > | <> | & | v

THE GRAMMAR WITH LEFT RECURSION REMOVED:
    S -> Q[E]
    Q -> ∀V | ∃V
    E -> GOG | (E)
    G -> FG' | (G) | (GOG) | F
    G'-> OGG' | epsilon
    V -> {a..z}
    W -> {Aa..Zz}
    F -> W(V) | ~F | (F)
    O -> > | <> | & | v
"""


def main() -> None:
    try:
        expr = "∀x[R(y) & S(x) > C(x)]"
        print(f"{expr}:")
        p = Parser(expr)
        re = p.s_rule()
        re.print()
        expr = "∃x[Auto(x) v Clovek(x) & Objekt(x)]"
        print(f"\n{expr}:")
        p = Parser(expr)
        re = p.s_rule()
        re.print()
    except EmptyInputException:
        pass
    except ValueError as e:
        print("Error:", e)
    except InvalidExpressionException as iee:
        print(iee)


if __name__ == '__main__':
    main()
