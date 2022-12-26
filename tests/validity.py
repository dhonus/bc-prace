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


if __name__ == '__main__':
    unittest.main()
