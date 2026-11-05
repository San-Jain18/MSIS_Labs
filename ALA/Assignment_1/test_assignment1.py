import unittest
from assignment_1 import Vec


class TestVector(unittest.TestCase):

    def test_mean(self):
        v = Vec((10, 20, 30, 40))

        result = v.mean()

        self.assertEqual(result, 25)

    def test_mean_with_float_values(self):
        v = Vec((1.5, 2.5, 3.5))

        result = v.mean()

        self.assertEqual(result, 2.5)

    def test_mean_single_element(self):
        v = Vec((10,))

        result = v.mean()

        self.assertEqual(result, 10)

    def test_mean_empty_vector(self):
        v = Vec()

        with self.assertRaises(ValueError):
            v.mean()

    def test_demean(self):
        v = Vec((10, 20, 30))

        result = v.demean()

        expected = Vec((-10, 0, 10))

        self.assertEqual(result.elements, expected.elements)

    def test_demean_mean_is_zero(self):
        v = Vec((10, 20, 30, 40))

        result = v.demean()

        self.assertAlmostEqual(result.mean(), 0.0)

    def test_demean_does_not_change_original(self):
        v = Vec((10, 20, 30))

        v.demean()

        self.assertEqual(v.elements, (10, 20, 30))

    def test_std(self):
        v = Vec((1, 2, 3, 4, 5))

        result = v.std()

        expected = (2 ** 0.5)

        self.assertAlmostEqual(result, expected)

    def test_std_constant_vector(self):
        v = Vec((5, 5, 5, 5))

        result = v.std()

        self.assertEqual(result, 0)

    def test_std_single_element(self):
        v = Vec((10,))

        result = v.std()

        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()