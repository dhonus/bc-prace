import unittest
from core.Parser import Parser, EmptyInputException, InvalidExpressionException


class MyTestCase(unittest.TestCase):
    def test_universal(self):
        expr = "∀x[!(S(x) > C(x)) & V(x)]"
        expected = "For all x applies [  not {[ (S(x)) > (C(x)) ]} & (V(x)) ]"
        p = Parser(expr)
        self.assertEqual(expected, p.s_rule().print())

    def test_existential(self):
        expr = "∃x[Auto(x) | N(x) & Clovek(x) & Objekt(x)]"
        p = Parser(expr)
        expected = "Exists x for which [ (Auto(x)) or [ (N(x)) & [ (Clovek(x)) & (Objekt(x)) ] ] ]"
        self.assertEqual(expected, p.s_rule().print())


if __name__ == '__main__':
    unittest.main()
