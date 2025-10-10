__author__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__date__ = "30/09/2025"

"""
Project: B4B33RPH
Filename: vectors.py
Directory: homeworks/02_DU/
"""

class MyVector:
    def __init__(self, vector: list):
        self.vector = vector

    def get_vector(self):
        return self.vector

    def __mul__(self, other: "MyVector"):
        # alternative: return sum(x*y for x,y in zip(self.vector, other.vector))
        result = 0
        for items in zip(self.vector, other.vector):
            result += items[0] * items[1]
        return result

if __name__ == '__main__':
    assert MyVector([1, 2, 3]) * MyVector([3, 4, 5]) == 26
    assert MyVector([2, 4, 6]) * MyVector([3, 5, 7]) == 68
    # alternative with unittest module

