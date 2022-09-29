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


if __name__ == '__main__':
    # final = {'AB', 'ABC', 'AC'}
    # final = {'A', 'B', 'C', 'BC'}

    p = [
        "∀x[!A(x) & (B(x) | C(x))]",
        "∀x[A(x) | (B(x) & C(x))]",
    ]
    # "∃x[s(x) | v(x) & x(x) & v(x)]",
    #         "∀x[(s(x) & (x(x)) > v(x))]",
    #         "∃x[v(x) & !(v(x) & !s(x))]"
    c = "∃x[A(x) & (B(x) | C(x))]"
    main(p, c)

    print("\n-- testing sets --")

    #  (a(x) & b(x)) > b(x)
    a = {
        "a",
        "ab",
        "ac",
        "abc"
    }
    b = {
        "b",
        "ab",
        "bc",
        "abc"
    }
    c = {
        "c",
        "ac",
        "bc",
        "abc"
    }
    states = {
        "a": "crossed",
    }

    tmp = b.union(c)
    print(tmp)
    tmp = a.intersection(tmp)
    print(tmp)

    print(b.union(c)) # disjunction
    print(b.intersection(b)) # conjunction
    print(a.difference(b)) # implication
    print(a.symmetric_difference(b)) # biconditional
    print(states)
