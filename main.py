from core.Parser import Parser, EmptyInputException, InvalidExpressionException
from core.Evaluator import Evaluator
import logging
from typing import List


def main(predicates: List[str], conclusion: str) -> None:
    logging.root.setLevel(logging.DEBUG)

    predicates = [predicate.replace(" ", "") for predicate in predicates]

    p_index = 1
    try:
        trees = []
        parser = Parser()
        for predicate in predicates:
            parser.attach(predicate)
            tree = parser.parse()
            tree.validate()
            trees.append(tree)
            print(tree.print())
            print()

        parser.attach(conclusion)
        conclusion_tree = parser.parse()
        conclusion_tree.validate()

        trees = sorted(
            trees, key=lambda tr: tr.value
        )  # sort to have universal statements first

        evaluator = Evaluator()
        solution = evaluator.eval(trees, conclusion_tree)
        print(f"\n\n----------\nsolution: {solution}\n----------")
        print(evaluator.validity(solution))

        p_index += 1

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
        "∀x[P(x) > Q(x)]",
        "∀x[Q(x) > R(x)]",
        "Ex[P(x)]"
    ]

    # c = "∃y[B(y) | C(y)]"
    c = "Ex[P(x) & R(x)]"
    main(p, c)
