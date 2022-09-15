from expressions.Nodes import Node, Impl

"""
    RDP https://www.youtube.com/watch?v=SToUyjAsaFk
        https://www.codeproject.com/Articles/318667/Mathematical-Expression-Parser-Using-Recursive-Des
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
    E -> EOE | (E) | F
    V -> {a..z}
    W -> {A..Z}
    F -> W(V)
    O -> > | <> | & | ~ | v | *
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
