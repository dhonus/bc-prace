import unittest

from main import main

class MyTestCase(unittest.TestCase):
    def test_something(self):
        p = [
            "Ax[A(x) > !B(x)]",
            "Ex[A(x) &!B(x)]",
            "Ey[A(y) &!B(y)]"
        ]
        c = "Ex[!B(x)]"
        val = main(p, c)
        self.assertEqual(True, val)  # add assertion here

    def test_zero(self):
        p = [
            "Ex[V(x) & K(x)]",
            "Ax[H(x) > !K(x)]",
        ]
        c = "Ex[V(x) & !H(x)]"
        self.assertEqual(True, main(p, c))  # add assertion here

    def test_one(self):
        p = [
            "Ax[A(x) > D(x)]",
            "Ax[A(x) > V(x)]",
            "Ex[A(x)]"
        ]
        c = "Ex[D(x) & V(x)]"
        self.assertEqual(True, main(p, c))  # add assertion here

    def test_two(self):
        p = [
            "Ax[S(x) > P(x)]",
            "Ex[S(x) & I(x)]",
            "Ex[P(x) & !S(x)]",
        ]
        c1 = "Ex[P(x) & !I(x)]"
        c2 = "Ex[P(x) & I(x)]"
        self.assertEqual(False, main(p, c1))
        self.assertEqual(True, main(p, c2))

    def test_three(self):
        p = [
            "Ax[P(x) > Q(x)]",
            "Ax[Q(x) > R(x)]",
            "Ex[P(x)]",
        ]
        c = "Ex[P(x) & R(x)]"
        self.assertEqual(True, main(p, c))

    def test_four(self):
        p = [
            "Ax[S(x) > M(x)]",
            "Ax[M(x) > K(x)]",
        ]
        c = "Ax[S(x) > K(x)]"
        self.assertEqual(True, main(p, c))

    def test_five(self):
        p = [
            "Ax[P(x) > Q(x)]",
            "Ax[Q(x) > R(x)]",
            "Ex[P(x)]",
        ]
        c = "Ex[P(x) & R(x)]"
        self.assertEqual(True, main(p, c))

    def test_six(self):
        p = [
            "Ax[P(x) > !S(x)]",
            "Ex[P(x) & B(x)]",
        ]
        c = "Ex[B(x) & !S(x)]"
        self.assertEqual(True, main(p, c))

    def test_seven(self):
        p = [
            "Ex[V(x) & K(x)]",
            "Ax[H(x) > !K(x)]",
        ]
        c = "Ex[V(x) & !H(x)]"
        self.assertEqual(True, main(p, c))

    def test_eight(self):
        p = [
            "Ex[V(x) & K(x)]",
            "Ax[H(x) > !K(x)]",
        ]
        c = "Ex[V(x) & !H(x)]"
        self.assertEqual(True, main(p, c))

    def test_nine(self):
        p = [
            "Ax[J(x) > S(x)]",
            "Ex[S(x) & N(x)]",
        ]
        c = "Ex[J(x) & N(x)]"
        self.assertEqual(False, main(p, c))

    def test_ten(self):
        p = [
            "Ex[Pl(x) & M(x)]",
            "Ax[M(x) > !Ps(x)]",
        ]
        c = "Ex[Pl(x) & !Ps(x)]"
        self.assertEqual(True, main(p, c))

    def test_eleven(self):
        p = [
            "Ax[A(x) > D(x)]",
            "Ax[A(x) > V(x)]",
        ]
        c = "Ex[D(x) & V(x)]"
        self.assertEqual(False, main(p, c))

    def test_twelve(self):
        p = [
            "Ax[A(x) > !B(x)]",
            "Ex[A(x) & !B(x)]",
        ]
        c = "Ex[!B(x)]"
        self.assertEqual(True, main(p, c))

    def test_thirteen(self):
        p = [
            "A(a)",
            "Ex[A(x) & !B(x)]",
        ]
        c = "Ex[!B(x)]"
        self.assertEqual(True, main(p, c))

    def test_fourteen(self):
        p = [
            "∀x[P(x) ⊃ R(x)]",
            "∀x[R(x) ⊃ E(x)]",
        ]
        c = "∀x[P(x) ⊃ E(x)]"
        self.assertEqual(True, main(p, c))

    def test_fifteen(self):
        p = [
            "∀x[P(x) ⊃ S(x)]",
            "∀x[P(x) ⊃ R(x)]",
        ]
        c = "∃x[S(x) ∧ R(x)]"
        self.assertEqual(False, main(p, c))

    def test_sixteen(self):
        p = [
            "∃x[P(x) ∧ O(x)]",
            "∀x[R(x) ⊃ P(x)]"
        ]
        c = "∃x[R(x) ∧ O(x)]"
        self.assertEqual(False, main(p, c))

    def test_seventeen(self):
        p = [
            "∀x[(S(x) & C(x)) > L(x)]",
            "∃x[S(x) & !C(x)]",
        ]
        c = "∃x[S(x) & !L(x)]"
        self.assertEqual(False, main(p, c))

    def test_eighteen(self):
        p = [
            "∀x[(S(x) & C(x)) > L(x)]",
            "S(a) & C(a)",
        ]
        c = "L(a)"
        self.assertEqual(True, main(p, c))

    def test_nineteen(self):
        p = [
            "∀x[(S(x) ∧ ¬Z(x)) ⊃ T (x)]",
            "S(a) ∧ Z(a)",
        ]
        c = "!T(a)"
        self.assertEqual(False, main(p, c))

    def test_twenty(self):
        p = [
            "∀x[(S(x) ∧ C(x)) ⊃ L(x)]",
            "S(a) ∧ ¬C(a)",
        ]
        c = "¬L(a)"
        self.assertEqual(False, main(p, c))

    def test_twenty_one(self):
        p = [
            "∀x[S(x) ⊃ I(x)]",
            "∀x[R(x) ⊃ ¬I(x)]",
            "∃x[R(x) ∧ S(x)]"
        ]
        c = "∃x[S(x) ∧ ¬R(x)]"
        self.assertEqual(True, main(p, c))
    def test_twenty_two(self):
        p = [
            "∀x[S(x) ⊃ ¬L(x)]",
            "∃x[L(x) ∧ P(x)]",
        ]
        c = "∃x[P(x) ∧ ¬S(x)]"
        self.assertEqual(True, main(p, c))
    def test_twenty_three(self):
        p = [
            "∀x[(C(x) ∨ D(x)) ⊃ S(x)]",
            "∃x[D(x) ∧ C(x)]",
        ]
        c = " ∃x[S(x) ∧ D(x)]"
        self.assertEqual(True, main(p, c))
    def test_twenty_four(self):
        p = [
            "∀x[(N(x) ∧ V(x)) ⊃ ¬C(x)]",
            "∃x[V(x) ∧ C(x)]",
        ]
        c = "∃x[V(x) ∧ ¬N(x)]"
        self.assertEqual(True, main(p, c))
    def test_twenty_five(self):
        p = [
            "∀x[P(x) ⊃ (¬N(x) ∧ ¬V(x))]",
            "∃x[V(x) ∧ N(x)]",
        ]
        c = "∃x[N(x) ∧ ¬P(x)]"
        self.assertEqual(True, main(p, c))
    def test_twenty_six(self):
        p = [
            "∀x[S(x) ⊃ (P(x) ∨ L(x))]",
            "∀x[L(x) ⊃ P(x)]",
        ]
        c = "∀x[L(x) ⊃ ¬S(x)]"
        self.assertEqual(False, main(p, c))
    def test_twenty_seven(self):
        p = [
            "∀x[P(x) ⊃ (S(x) ∧ ¬L(x))]",
            "∃x[S(x) ∧ ¬P(x)]",
        ]
        c = "∃x[S(x) ∧ L(x)]"
        self.assertEqual(False, main(p, c))
    def test_twenty_eight(self):
        p = [
            "∀x[C(x) ⊃ ¬P(x)]",
            "∀x[V(x) ⊃ C(x)]",
        ]
        c = "∀x[V(x) ⊃ ¬P(x)]"
        self.assertEqual(True, main(p, c))
    def test_twenty_nine(self):
        p = [
            "∃x[F(x) ∧ ¬I(x)]",
            "∀x[F(x) ⊃ S(x)]",
        ]
        c = "∃x[S(x) ∧ ¬I(x)]"
        self.assertEqual(True, main(p, c))
    def test_thirty(self):
        p = [
            "∀x[P(x) ⊃ K(x)]",
            "¬P(a)",
        ]
        c = "¬K(a)"
        self.assertEqual(False, main(p, c))
    def test_thirty_one(self):
        p = [
            "∀x[T (x) ∨ C(x)]",
            "∀x[C(x) ⊃ ¬T (x)]",
            "∃x[S(x) ∧ ¬C(x)]",
        ]
        c = "∃x[S(x) ∧ T (x)]"
        self.assertEqual(True, main(p, c))

    def test_thirty_two(self):
        p = [
            "∀x[F(x) ⊃ ¬M(x)]",
            "∃x[F(x) ∧ P(x)]",
        ]
        c = "∃x[P(x) ∧ ¬M(x)]"
        self.assertEqual(True, main(p, c))

    def test_thirty_three(self):
        p = [
            "∃x[A(x) ∧ ¬R(x)]",
            "A(a)",
        ]
        c = "∀x[R(x) ⊃ ¬A(x)]"
        self.assertEqual(False, main(p, c))

    def test_thirty_four(self):
        p = [
            "Ax[A(x) | B(x)]",
            "Ex[A(x)]",
        ]
        c = "Ex[A(x)]"
        self.assertEqual(True, main(p, c))
        c = "Ex[B(x)]"
        self.assertEqual(False, main(p, c))

    def test_thirty_five(self):
        p = [
            "Ax[A(x) | B(x)]",
            "Ex[A(x) & C(x)]",
        ]
        c = "Ex[A(x)]"
        self.assertEqual(True, main(p, c))
        c = "Ex[B(x)]"
        self.assertEqual(False, main(p, c))

    # not sure actually
    """def test_thirty_six(self):
        p = [
            "P(a) > Q(a)",
            "P(a)",
        ]
        c = "!P(a)" # tautology
        self.assertEqual(True, main(p, c))"""

    def test_thirty_seven(self):
        p = [
            "Ax[A(x) | B(x)]",
            "A(a)",
            "B(a)"
        ]
        c = "A(a) & B(a)"
        self.assertEqual(True, main(p, c))

    def test_thirty_eight(self):
        p = [
            "Ax[A(x)]",
            "Ex[A(x)]",
        ]
        c = "A(b)"
        self.assertEqual(False, main(p, c))

    def test_thirty_nine(self):
        p = [
            "P(a)  & Q(a)",
            "Ax[P(x) & Q(x)  > R(x)]",
        ]
        c = "R(a)"
        self.assertEqual(True, main(p, c))
        c = "R(b)"
        self.assertEqual(False, main(p, c))

if __name__ == '__main__':
    unittest.main()
