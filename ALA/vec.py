
import sys
from typing import Self


"""
A custom vector class implementation for educational purposes.
"""
#this class represents a vector of numbers (int or float). It supports basic vector operations such as addition, scalar multiplication, and more.

class Vec:
    #constructor for the Vec class that Initializes a vector with the given source elements or an empty vector if no source is provided.
    def __init__(self, src=None) -> Self:
        if src is None:
            self.elements = ()
        else:
            self.elements = tuple(src)
            """
            for x in elements:
                if not isinstance(x, (int, float)):
                    raise TypeError(f"Scalar must be a number: {type(x)}")
            self.elements = elements
            """

    def scalar_mul(self,alpha):
        ele = list(self.elements)
        # for each 'val' in 'ele' perform alpha+val and store it in 'ele'
        # for i in range(len(ele)):
        #     ele[i] = round(alpha * ele[i], 5)
        result = Vec(x*alpha for x in self.elements)
        return result
    
    def __repr__(self):
        return repr(self.elements)


'''
    def __add__(self, t: Self) -> Self:
        if not isinstance(t, Vec):
            raise TypeError(f"Expected Vec: {type(t)}")
        if len(self.elements) != len(t):
            raise TypeError(f"Type error - vectors must be of same dimensions")

        return Vec([round(x + y, 5) for x, y in zip(self.elements, t.elements)])


    def __rmul__(self, scalar: int | float) -> Self:
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"Vector multiplication with invalid type: {type(scalar)}")
        #
        return Vec([round(x * scalar, 5) for x in self.elements])

    def __imul__(self, scalar: int | float) -> Self:
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"Vector multiplication with invalid type: {type(scalar)}")

        for i, val in enumerate(self.elements):
            self.elements[i] = round(val * scalar, 5)
        #
        return self

    def __repr__(self) -> str:
        return repr(self.elements)

    def __len__(self) -> int:
        return len(self.elements)

    def __sub__(self, t: Self) -> Self:
        raise RuntimeError("vec subtraction unimplemented")

    def __neg__(self) -> Self:
        raise RuntimeError("vec negation unimplemented")

    def __radd__(self, other):
        raise RuntimeError("vec _radd_ unimplemented")

    def __iadd__(self, other):
        raise RuntimeError("vec _iadd_ unimplemented")

    # return a vector of @n zeroes. precondition: @n > 0
    @staticmethod
    def zeros(n: int) -> Self:
        raise RuntimeError("zeros unimpleented")

    # return a vector of @n. precondition: @n > 0
    @staticmethod
    def ones(n: int) -> Self:
        raise RuntimeError("ones unimpleented")

    # return a vector of @n uniformly distributed numbers in [0, 1]. precondition: @n > 0
    @staticmethod
    def uniform(n: int) -> Self:
        raise RuntimeError("random unimpleented")

    # Calculates the Euclidean norm (L2 norm) of the vector.
    # sqrt(e[0]^2 + e[1]^2 + e[2]^2 + ... + e[n-1]^2)
    def norm(self) -> float:
        raise RuntimeError("norm unimpleented")
'''

"""
(1) Understand the basic design of the vector abstraction. Review the implementation.
(2) Document each function.
(3) Implement all unimplemented methods.
(4) Create appropriate tests for this implementation, increasing the confidence about its correctness.
(5) Test this implementation by importing the class in a sepatate python script.

(6) Measure the performance of each of these functions on vectors of varying lengths.
    Try 2k to 64k dimension vectors and time the results.
    How would you do the measurements?
(7) Measure the performance on your machine. Check it on colab.

(8) use numpy and compare the performance.
"""


if sys.version_info < (3, 8):
    sys.exit("Error: This script requires Python 3.8 or higher.")

if __name__ == "__main__":
    #z1 = Vec.zeros(10)
    v1 = Vec((10, 20, 1.03))
    print(v1)
    v2 = v1.scalar_mul(2.2)
    print(v2)
    # v3 = 2.2 * v1
    # v3 *= 5
    # # v3 = 1 + v3
    # print(v3)
    # v2 = v1 + v3
    # print(v1 + v3)
    # #print(-(v1 + v3))
