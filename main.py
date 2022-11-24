from core.Parser import Parser, EmptyInputException, InvalidExpressionException
from core.Evaluator import Evaluator
import logging
from typing import List


def main(predicates: List[str], conclusion: str) -> None:
    logging.root.setLevel(logging.DEBUG)

    predicates = [predicate.replace(" ", "") for predicate in predicates]

    # we will return the enumerated predicates to the frontend to make sure the order is maintained
    predicates_to_return = {}
    p_index = 1
    try:
        trees = []
        parser = Parser()
        for predicate in predicates:
            predicates_to_return[p_index] = predicate
            parser.attach(predicate, p_index)
            tree = parser.parse()
            tree.validate()
            trees.append(tree)
            print(tree.print())
            print()
            p_index += 1

        predicates_to_return[p_index] = conclusion
        parser.attach(conclusion, p_index)
        conclusion_tree = parser.parse()
        conclusion_tree.validate()

        trees = sorted(
            trees, key=lambda tr: tr.value
        )  # sort to have universal statements first

        evaluator = Evaluator()
        solution = evaluator.eval(trees, conclusion_tree)
        print(f" -- {evaluator.get_sets()} -- ")
        print(f"\n\n----------\nsolution: {solution}\n----------")
        print(predicates_to_return)
        print(evaluator.validity(solution))

    except InvalidExpressionException as iee:
        print(iee)
    except Exception as e:
        logging.critical(f"{type(e).__name__}: V predikátu {p_index}: {e}")


if __name__ == "__main__":

    """p = ["∀x[A(x) > B(x)]",
         "∀y[B(y) > A(y) | C(y)]",
         "∃y[B(y) | A(y)]",
         "B(x) & C(x)"]"""
    p = [
        "Ax[P(x) > Q(x)]",
        "Ax[Q(x) > R(x)]",
        "Ex[P(x)]",
    ]

    # c = "∃y[B(y) | C(y)]"
    c = "Ex[P(x) & R(x)]"
    main(p, c)
