from core.Parser import Parser, EmptyInputException, InvalidExpressionException
from core.Evaluator import Evaluator
import logging
from typing import List


def main(predicates: List[str], conclusion: str) -> None:
    logging.root.setLevel(logging.INFO)

    predicates = [predicate.replace(" ", "") for predicate in predicates]

    p_index = 1
    try:
        trees = []
        for predicate in predicates:
            print(f"{predicate}:")
            parser = Parser(predicate)
            tree = parser.parse()
            trees.append(tree)
            print(tree.print())
            print()

        parser = Parser(conclusion)
        conclusion_tree = parser.parse()

        trees = sorted(trees, key=lambda tr: tr.value)  # sort to have universal statements first

        evaluator = Evaluator()
        evaluator.eval(trees, conclusion_tree)

        """
        for tree in trees:
            evaluator = Evaluator()
            evaluator.eval(tree, conclusion_tree)
        """
        p_index += 1

    except EmptyInputException:
        pass
    except InvalidExpressionException as iee:
        print(iee)
    except Exception as e:
        logging.critical(f"{type(e).__name__}: In predicate {p_index}: {e}")

    print("----------")


if __name__ == '__main__':
    p = [
        "∀x[!(S(x) <> X(x)) & V(x)]",
        "∃x[S(x) | V(x) & X(x) & V(x)]",
        "∀x[(S(x) & (X(x)) > V(x))]",
        "∃x[V(x) & !(V(x) & !S(x))]"
    ]
    c = "∃x[S(x) & V(x)]"
    main(p, c)
