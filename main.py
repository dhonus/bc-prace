from expressions.Nodes import Node, Impl

"""
    RECURSIVE DESCENT PARSING
        https://www.youtube.com/watch?v=SToUyjAsaFk
        https://www.codeproject.com/Articles/318667/Mathematical-Expression-Parser-Using-Recursive-Des
    REMOVING LEFT RECURSION FORMULA
        https://www.csd.uwo.ca/~mmorenom/CS447/Lectures/Syntax.html/node8.html
"""

"""
SYMBOLS:
    IMPL:   >
    BICON:  <>
    AND:    &
    OR:     v
    NOT:    ~
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
    O -> > | <> | & | v | *

THE GRAMMAR WITH LEFT RECURSION REMOVED:
    S -> Q[E]
    Q -> ∀V | ∃V
    E -> FOF | GOG | (E)
    G -> FG' | (G) | (GOG) | F
    G'-> OGG' | epsilon
    V -> {a..z}
    W -> {Aa..Zz}
    F -> W(V) | ~F | (F)
    O -> > | <> | & | v | *
"""


def recursive_descent_parse():
    pass


def parse(input_string: str) -> Node:
    """ parse the input and break up into tokens """
    input_string = input_string.replace(' ', '')
    if not input_string:
        return Node()
    match input_string[0]:
        case '∃':
            pass
        case '∀':
            pass
        case _:
            pass

    n = Node
    return n


def del_f():
    node = Node()
    print(node.get_value())

    p1 = "∀x[R(x) ⊃ S(x)]"
    parse(p1)


if __name__ == '__main__':
    del_f()
