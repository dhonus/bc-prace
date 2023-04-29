from core.Parser import Parser, EmptyInputException, InvalidExpressionException
from core.Evaluator import Evaluator
import logging
from typing import List

""" this file can serve to test out the API """
def main(predicates: List[str], conclusion: str) -> bool:
    logging.root.setLevel(logging.DEBUG)

    predicates = [predicate.replace(" ", "") for predicate in predicates]

    # we will return the enumerated predicates to the frontend to make sure the order is maintained
    predicates_to_return = {}
    p_index = 1
    evaluator = Evaluator()
    try:
        trees = []
        parser = Parser()
        for predicate in predicates:
            predicates_to_return[p_index] = predicate
            parser.attach(predicate, p_index)
            tree = parser.parse()
            tree.validate()
            trees.append(tree)
            p_index += 1

        predicates_to_return[p_index] = conclusion
        parser.attach(conclusion, p_index)
        conclusion_tree = parser.parse()
        conclusion_tree.validate()

        trees = sorted(
            trees, key=lambda tr: tr.value
        )  # sort to have universal statements first

        solution = evaluator.eval(trees, conclusion_tree)
        print(f"\n\n----------\nsolution: {solution}\n----------")
        print(evaluator.validity(solution))

    except InvalidExpressionException as iee:
        print(iee)
        if evaluator.get_invalid_expected():
            print("Invalid expected")
            return False
    except Exception as e:
        if p_index == len(predicates):
            logging.critical(f"{type(e).__name__}: V závěru: {e}")
        else:
            logging.critical(f"{type(e).__name__}: V predikátu {p_index}: {e}")
        if evaluator.get_invalid_expected():
            print("Invalid expected")
            return False

    return evaluator.validity(solution)

def validate(predicate: str):
    predicate = predicate.replace(" ", "")
    try:
        parser = Parser()
        parser.attach(predicate, 0)
        tree = parser.parse()
        tree.validate()
        return [True, ""]
    except ValueError as iee:
        err = str(iee)
        return [False, err]

if __name__ == "__main__":
    p = [
        "Ax[P(x) > !S(x)]",
        "Ex[P(x) & B(x)]",
    ]
    c = "Ex[B(x) & !S(x)]"

    main(p, c)
