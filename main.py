from expressions.Parser import Parser, EmptyInputException, InvalidExpressionException
import logging

"""

"""


def main() -> None:
    logging.root.setLevel(logging.INFO)
    predicates = [
        "∀x[!(S(x) > C(x)) & V(x)]",
        "∀x[(S(x) & B(x)) > V(x)]",
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
