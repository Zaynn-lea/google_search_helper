
"""
submodule of the graphic_tool package made to handle definitions of matrices classes, matrix manipulation and matrix
opperations

made by Gely Lea

------------------------------------------------------------------------------------------------------------------------

    - Matrix : an abstract class to represent a Matrix

    - Matrix2x2 : a class which inherit from Matrix, represent a 2 by 2 matrix

    - Matrix3x3 : a class which inherit from Matrix, represent a 3 by 3 matrix

    - Matrix4x4 : a class which inherit from Matrix, represent a 4 by 4 matrix

    - null_Matrix_2x2, null_Matrix_3x3 and null_Matrix_4x4 : a special matrix with every coordinate equal to 0

    - unit_Matrix_2x2, unit_Matrix_3x3 and unit_Matrix_4x4 :
            a special matrix with the diagonal set to 1 and the rest to 0
"""

import math
import typing

from graphic_tool import _error_handling as _err


# +------------------+
# |   Matrix class   |
# +------------------+

class Matrix(object):
    def __init__(self, width: int, high: int):
        """
        this is an abstract Matrix class, used to derive Matrix4x4 and enabling polymorphism

        ----------------------------------------------------------------------------------------------------------------

        :param : list or tuple or set of Triangle object
        """
        if width < 1:
            raise ValueError
        if high < 1:
            raise ValueError

        self.width = width
        self.high = high

        self.matrix = None

    def __getitem__(self, y):
        """
        Implement self[y]

        :param y: a positive integer
        :return: a number
        """
        if y < -1 or y >= self.high:
            raise IndexError

        return self.matrix[y]

    def _test_input(self, matrix: [list, tuple]):
        """
        method to test if the matrix is the same size of the current one
        also test for the type of the matrix type (list of list, tuple of tuple, tuple of list, list of tuple)
        and test to see if all components are numbers (int or float)

        :param matrix: list or tuple of lmist or tuple of number
        """
        if len(matrix) < self.high:
            raise _err.LengthError

        i, i_max, test_row_type, test_elt_type, test_length = 0, self.high, True, True, True
        while i < i_max and test_row_type and test_elt_type and test_length:
            test_row_type = test_row_type and type(matrix[i]) in [list, tuple]
            test_length = test_length and len(matrix[i]) >= self.width

            j, j_max = 0, self.width
            while j < j_max and test_row_type and test_elt_type and test_length:
                test_elt_type = test_elt_type and type(matrix[i][j]) in [int, float]
                j += 1

            i += 1

        if not test_length:
            raise _err.LengthError
        if not test_elt_type:
            raise TypeError
        if not test_row_type:
            raise TypeError



class Matrix2x2(Matrix):
    def __init__(self, initial=None):
        """
        class to represent a 2 by 2 matrix

        ----------------------------------------------------------------------------------------------------------------

        Methods :

            .copy() -> Matrix3x3

            .get_row(index) -> list

            .get_column(index) -> list

            .get_matrix() -> list

            .get_row(new_row, index) -> None
                method to change the specified row

            .get_column(new_column, index) -> None
                method to change the specified column

            .get_matrix(new_matrix) -> None
                method to change the whole matrix

            .get_transpose() -> Matrix4x4

            .transpose() -> None
                method that transpose the matrix

        ----------------------------------------------------------------------------------------------------------------

        supported operations:

            + ; += : add each component

            - ; -= : sub each component
                     if put right before the object, multiply by -1 each component

            * ; *= : multiply by a scalar

            / ; // : divide by a scalar != 0

            == : test if each of the components are equal

            [y] : return the y-th line

        ----------------------------------------------------------------------------------------------------------------

        :param initial: list or tuple of lmist or tuple of number, optional, defaulted to None
        """
        super().__init__(2, 2)

        if initial is not None:
            self._test_input(initial)

            self.matrix = initial
        else:
            self.matrix = [
                [0, 0],
                [0, 0],
            ]

    def __add__(self, other):
        """
        Implement self + other

        :param other: a Matrix2x2 object or a list or tuple of list or tuple
        :return: a Matrix2x2 object
        """
        if isinstance(other, Matrix2x2):
            return Matrix2x2(initial=[
                [self[0][0] + other[0][0], self[0][1] + other[0][1]],
                [self[1][0] + other[1][0], self[1][1] + other[1][1]],
            ])
        elif type(other) in (list, tuple):
            self._test_input(other)

            return Matrix2x2(initial=[
                [self[0][0] + other[0][0], self[0][1] + other[0][1]],
                [self[1][0] + other[1][0], self[1][1] + other[1][1]],
            ])
        else:
            raise TypeError

    def __sub__(self, other):
        """
        Implement self - other

        :param other: a Matrix2x2 object or a list or tuple of list or tuple
        :return: a Matrix2x2 object
        """
        if isinstance(other, Matrix2x2):
            return Matrix2x2(initial=[
                [self[0][0] - other[0][0], self[0][1] - other[0][1]],
                [self[1][0] - other[1][0], self[1][1] - other[1][1]],
            ])
        elif type(other) in (list, tuple, Matrix2x2):
            self._test_input(other)

            return Matrix2x2(initial=[
                [self[0][0] - other[0][0], self[0][1] - other[0][1]],
                [self[1][0] - other[1][0], self[1][1] - other[1][1]],
            ])
        else:
            raise TypeError

    def __mul__(self, other):
        """
        Implement self * other

        :param other: a number or a Matrix2x2 object or a list or tuple of list or tuple
        :return: a Matrix2x2 object
        """
        if type(other) in [int, float]:
            return Matrix2x2(initial=[
                [self[0][0] * other, self[0][1] * other],
                [self[1][0] * other, self[1][1] * other],
            ])
        elif isinstance(other, Matrix2x2):
            return Matrix2x2(initial=[
                [self[0][0] * other[0][0] + self[0][1] * other[1][0],
                 self[0][0] * other[0][1] + self[0][1] * other[1][1]],

                [self[1][0] * other[0][0] + self[1][1] * other[1][0],
                 self[1][0] * other[0][1] + self[1][1] * other[1][1]],
            ])
        elif type(other) in [tuple, list]:
            self._test_input(other)

            return Matrix2x2(initial=[
                [self[0][0] * other[0][0] + self[0][1] * other[1][0],
                 self[0][0] * other[0][1] + self[0][1] * other[1][1]],

                [self[1][0] * other[0][0] + self[1][1] * other[1][0],
                 self[1][0] * other[0][1] + self[1][1] * other[1][1]],
            ])
        else:
            raise TypeError

    def __truediv__(self, other: [float, int]):
        """
        Implement self / other

        :param other: a number
        :return: a Matrix2x2 object
        """
        if other != 0:
            raise ZeroDivisionError
        return Matrix2x2(initial=[
            [self.matrix[0][0] / other, self.matrix[0][1] / other],
            [self.matrix[1][0] / other, self.matrix[1][1] / other],
        ])

    def __radd__(self, other):
        """
        Implement self + other

        :param other: a Matrix2x2 object or a list or tuple of list or tuple
        :return: a Matrix2x2 object
        """
        if isinstance(other, Matrix2x2):
            return Matrix2x2(initial=[
                [other.matrix[0][0] + self.matrix[0][0], other.matrix[0][1] + self.matrix[0][1]],
                [other.matrix[1][0] + self.matrix[1][0], other.matrix[1][1] + self.matrix[1][1]],
            ])
        elif type(other) in (list, tuple):
            self._test_input(other)

            return Matrix2x2(initial=[
                [other[0][0] + self.matrix[0][0], other[0][1] + self.matrix[0][1]],
                [other[1][0] + self.matrix[1][0], other[1][1] + self.matrix[1][1]],
            ])
        else:
            raise TypeError

    def __rsub__(self, other):
        """
        Implement other - self

        :param other: a Matrix2x2 object or a list or tuple of list or tuple
        :return: a Matrix2x2 object
        """
        if isinstance(other, Matrix2x2):
            return Matrix2x2(initial=[
                [other.matrix[0][0] - self.matrix[0][0], other.matrix[0][1] - self.matrix[0][1]],
                [other.matrix[1][0] - self.matrix[1][0], other.matrix[1][1] - self.matrix[1][1]],
            ])
        elif type(other) in (list, tuple):
            self._test_input(other)

            return Matrix2x2(initial=[
                [other[0][0] - self.matrix[0][0], other[0][1] - self.matrix[0][1]],
                [other[1][0] - self.matrix[1][0], other[1][1] - self.matrix[1][1]],
            ])
        else:
            raise TypeError

    def __rmul__(self, other):
        """
        Implement other * self

        :param other: a number or a Matrix2x2 object or a list or tuple of list or tuple
        :return: a Matrix2x2 object
        """
        if type(other) in [int, float]:
            return Matrix2x2(initial=[
                [other * self[0][0], other * self[0][1]],
                [other * self[1][0], other * self[1][1]],
            ])
        elif isinstance(other, Matrix2x2):
            return Matrix2x2(initial=[
                [other[0][0] * self[0][0] + other[0][1] * self[1][0],
                 other[0][0] * self[0][1] + other[0][1] * self[1][1]],

                [other[1][0] * self[0][0] + other[1][1] * self[1][0],
                 other[1][0] * self[0][1] + other[1][1] * self[1][1]],
            ])
        elif type(other) in [tuple, list]:
            self._test_input(other)

            return Matrix2x2(initial=[
                [other[0][0] * self[0][0] + other[0][1] * self[1][0],
                 other[0][0] * self[0][1] + other[0][1] * self[1][1]],

                [other[1][0] * self[0][0] + other[1][1] * self[1][0],
                 other[1][0] * self[0][1] + other[1][1] * self[1][1]],
            ])
        else:
            raise TypeError

    def __iadd__(self, other):
        """
        Implement self += other

        :param other: a Matrix2x2 object or a list or tuple of list or tuple
        """
        if isinstance(other, Matrix2x2):
            self.matrix[0][0] += other.matrix[0][0]
            self.matrix[0][1] += other.matrix[0][1]
            self.matrix[1][0] += other.matrix[1][0]
            self.matrix[1][1] += other.matrix[1][1]
            return self
        elif type(other) in (list, tuple):
            self._test_input(other)

            self.matrix[0][0] += other[0][0]
            self.matrix[0][1] += other[0][1]
            self.matrix[1][0] += other[1][0]
            self.matrix[1][1] += other[1][1]
            return self
        else:
            raise TypeError

    def __isub__(self, other):
        """
        Implement self -= other

        :param other: a Matrix2x2 object or a list or tuple of list or tuple
        """
        if isinstance(other, Matrix2x2):
            self.matrix[0][0] -= other.matrix[0][0]
            self.matrix[0][1] -= other.matrix[0][1]
            self.matrix[1][0] -= other.matrix[1][0]
            self.matrix[1][1] -= other.matrix[1][1]
            return self
        elif type(other) in (list, tuple):
            self._test_input(other)

            self.matrix[0][0] -= other[0][0]
            self.matrix[0][1] -= other[0][1]
            self.matrix[1][0] -= other[1][0]
            self.matrix[1][1] -= other[1][1]
            return self
        else:
            raise TypeError

    def __imul__(self, other: [float, int]):
        """
        Implement self *= other

        :param other: a number or a Matrix2x2 object or a list or tuple of list or tuple
        :return: a Matrix2x2 object
        """
        if type(other) in [int, float]:
            self.matrix[0][0] *= other
            self.matrix[0][1] *= other
            self.matrix[1][0] *= other
            self.matrix[1][1] *= other

        elif isinstance(other, Matrix2x2):
            self[0][0] = self[0][0] * other[0][0] + self[0][1] * other[1][0]
            self[0][1] = self[0][0] * other[0][1] + self[0][1] * other[1][1]

            self[1][0] = self[1][0] * other[0][0] + self[1][1] * other[1][0]
            self[1][1] = self[1][0] * other[0][1] + self[1][1] * other[1][1]

        elif type(other) in [tuple, list]:
            self._test_input(other)

            self[0][0] = self[0][0] * other[0][0] + self[0][1] * other[1][0]
            self[0][1] = self[0][0] * other[0][1] + self[0][1] * other[1][1]

            self[1][0] = self[1][0] * other[0][0] + self[1][1] * other[1][0]
            self[1][1] = self[1][0] * other[0][1] + self[1][1] * other[1][1]

        else:
            raise TypeError

        return self

    def __itruediv__(self, other: [float, int]):
        """
        Implement self /= other

        :param other: a number
        """
        if other == 0:
            raise ZeroDivisionError

        self.matrix[0][0] /= other
        self.matrix[0][1] /= other
        self.matrix[1][0] /= other
        self.matrix[1][1] /= other
        return self

    def __neg__(self):
        """
        Implement -self
        """
        self.matrix[0][0] = -self.matrix[0][0]
        self.matrix[0][1] = -self.matrix[0][1]
        self.matrix[1][0] = -self.matrix[1][0]
        self.matrix[1][1] = -self.matrix[1][1]
        return self

    def __eq__(self, other) -> bool:
        """
        Implement self == other

        :param other: a Matrix2x2 object, a list or a tuple of list or tuple
        :return: bool
        """
        if isinstance(other, Matrix2x2):
            test = self.matrix[0][0] == other.matrix[0][0] \
                   and self.matrix[0][1] == other.matrix[0][1] \
                   and self.matrix[1][0] == other.matrix[1][0] \
                   and self.matrix[1][1] == other.matrix[1][1]

        elif type(other) in (tuple, list):
            if len(other) < 2:
                raise _err.LengthError

            i, i_max, test = 0, 2, True
            while i < i_max and test:
                test = test and type(other[i]) in [list, tuple] and len(other[i]) >= 2

                j, j_max = 0, 2
                while j < j_max and test:
                    test = test and type(other[i][j]) in [int, float]
                    j += 1

                i += 1

            test = self.matrix[0][0] == other[0][0]\
                   and self.matrix[0][1] == other[0][1]\
                   and self.matrix[1][0] == other[1][0]\
                   and self.matrix[1][1] == other[1][1]

        else:
            test = False

        return test

    def copy(self):
        """
        method to get a copy of the matrix

        :return: a Matrix2x2 object
        """
        return Matrix2x2(initial=self.matrix)

    def get_row(self, index: int) -> list:
        """
        method which return the row corresponding to the index (between 0 and 2, -1 allow to get last one)

        :param index: an integer
        :return: a list of number
        """
        if index < -1 or index > 2:
            raise IndexError
        return self.matrix[index]

    def get_column(self, index: int) -> list:
        """
        method which return the column corresponding to the index (between 0 and 2, -1 allow to get last one)

        :param index: an integer
        :return: a list of number
        """
        if index < -1 or index > 2:
            raise IndexError
        return [self.matrix[i][index] for i in range(2)]

    def get_matrix(self) -> list:
        """
        method which return the whole 2 by 2 matrix

        :return: a list of list of number
        """
        return self.matrix

    def set_row(self, new_row: [tuple, list], index: int):
        """
        method which change the row corresponding to the index for new_row
        index must be between 0 and 2 or -1 to get the last one

        :param new_row: a list of number
        :param index: an integer
        """
        if len(new_row) < 2:
            raise _err.LengthError

        if type(new_row[0]) not in (int, float):
            raise TypeError
        if type(new_row[1]) not in (int, float):
            raise TypeError

        if index < -1 or index > 3:
            raise IndexError

        self.matrix[index] = new_row

    def set_column(self, new_column: [tuple, list], index: int):
        """
        method which change the column corresponding to the index for new_column
        index must be between 0 and 2 or -1 to get the last one

        :param new_column: a list of number
        :param index: an integer
        """
        if len(new_column) < 2:
            raise _err.LengthError

        if type(new_column[0]) not in (int, float):
            raise TypeError
        if type(new_column[1]) not in (int, float):
            raise TypeError

        if index < -1 or index > 3:
            raise IndexError

        self.matrix[index][0] = new_column[0]
        self.matrix[index][1] = new_column[1]

    def set_matrix(self, new_matrix: [tuple, list]):
        """
        method which change the whole matrix for new_matrix

        :param new_matrix: a list of list of number
        """
        self._test_input(new_matrix)

        self.matrix = new_matrix

    def get_transpose(self):
        """
        method to get a copy of the matrix which is its transpose

        :return: a Matrix4x4 object
        """
        return Matrix4x4(initial=[
            [self.matrix[0][0], self.matrix[1][0]],
            [self.matrix[0][1], self.matrix[1][1]],
        ])

    def transpose(self):
        """
        method to transpose the matrix
        """
        self.matrix[0][1] = self.matrix[1][0]
        self.matrix[1][0] = self.matrix[0][1]


class Matrix3x3(Matrix):
    def __init__(self, initial=None):
        """
        class to represent a 3 by 3 matrix

        ----------------------------------------------------------------------------------------------------------------

        Methods :

            .copy() -> Matrix3x3

            .get_row(index) -> list

            .get_column(index) -> list

            .get_matrix() -> list

            .get_row(new_row, index) -> None
                method to change the specified row

            .get_column(new_column, index) -> None
                method to change the specified column

            .get_matrix(new_matrix) -> None
                method to change the whole matrix

            .get_transpose() -> Matrix3x3

            .transpose() -> None
                method that transpose the matrix

        ----------------------------------------------------------------------------------------------------------------

        supported operations:

            + ; += : add each component

            - ; -= : sub each component
                     if put right before the object, multiply by -1 each component

            * ; *= : multiply by a scalar

            / ; // : divide by a scalar != 0

            == : test if each of the components are equal

            [y] : return the y-th line

        ----------------------------------------------------------------------------------------------------------------

        :param initial: list or tuple of list or tuple of number, optional, defaulted to None
        """
        super().__init__(3, 3)

        if initial is not None:
            self._test_input(initial)

            self.matrix = initial
        else:
            self.matrix = [
                [0 for _ in range(3)] for _ in range(3)
            ]

    def __add__(self, other):
        """
        Implement self + other

        :param other: a Matrix3x3 object or a list or tuple of list or tuple
        :return: a Matrix3x3 object
        """
        if isinstance(other, Matrix3x3):
            return Matrix3x3(initial=[[self.matrix[i][j] + other.matrix[i][j] for j in range(3)] for i in range(3)])
        elif type(other) in (list, tuple):
            self._test_input(other)

            return Matrix3x3(initial=[[self.matrix[i][j] + other[i][j] for j in range(3)] for i in range(3)])
        else:
            raise TypeError

    def __sub__(self, other):
        """
        Implement self - other

        :param other: a Matrix3x3 object or a list or tuple of list or tuple
        :return: a Matrix3x3 object
        """
        if isinstance(other, Matrix3x3):
            return Matrix3x3(initial=[[self.matrix[i][j] - other.matrix[i][j] for j in range(3)] for i in range(3)])
        elif type(other) in (list, tuple):
            self._test_input(other)

            return Matrix3x3(initial=[[self.matrix[i][j] - other[i][j] for j in range(3)] for i in range(3)])
        else:
            raise TypeError

    def __mul__(self, other):
        """
        Implement self * other

        :param other: a number or a Matrix3x3 object or a list or tuple of list or tuple
        :return: a Matrix3x3 object
        """
        if type(other) in [int, float]:
            return Matrix3x3(initial=[[self.matrix[i][j] * other for j in range(3)] for i in range(3)])

        elif isinstance(other, Matrix3x3):
            ret_mat = Matrix3x3()

            for i_self in range(3):
                for i_other in range(3):
                    s = 0
                    for j in range(3):
                        s += self[i_self][j] * other[j][i_other]
                    ret_mat[i_self][i_other] = s

            return ret_mat

        elif type(other) in [tuple, list]:
            self._test_input(other)

            ret_mat = Matrix3x3()

            for i_self in range(3):
                for i_other in range(3):
                    s = 0
                    for j in range(3):
                        s += self[i_self][j] * other[j][i_other]
                    ret_mat[i_self][i_other] = s

            return ret_mat

        else:
            raise TypeError

    def __truediv__(self, other: [float, int]):
        """
        Implement self / other

        :param other: a number
        :return: a Matrix3x3 object
        """
        if other != 0:
            raise ZeroDivisionError
        return Matrix3x3(initial=[[self.matrix[i][j] / other for j in range(3)] for i in range(3)])

    def __radd__(self, other):
        """
        Implement other + self

        :param other: a Matrix3x3 object or a list or tuple of list or tuple
        :return: a Matrix3x3 object
        """
        if isinstance(other, Matrix3x3):
            return Matrix3x3(initial=[[other.matrix[i][j] + self.matrix[i][j] for j in range(3)] for i in range(3)])
        elif type(other) in (list, tuple):
            self._test_input(other)

            return Matrix3x3(initial=[[other[i][j] + self.matrix[i][j] for j in range(3)] for i in range(3)])
        else:
            raise TypeError

    def __rsub__(self, other):
        """
        Implement other - self

        :param other: a Matrix3x3 object or a list or tuple of list or tuple
        :return: a Matrix3x3 object
        """
        if isinstance(other, Matrix3x3):
            return Matrix3x3(initial=[[other.matrix[i][j] - self.matrix[i][j] for j in range(3)] for i in range(3)])
        elif type(other) in (list, tuple):
            self._test_input(other)

            return Matrix3x3(initial=[[other[i][j] - self.matrix[i][j] for j in range(3)] for i in range(3)])
        else:
            raise TypeError

    def __rmul__(self, other):
        """
        Implement other * self

        :param other: a number or a Matrix3x3 object or a list or tuple of list or tuple
        :return: a Matrix3x3 object
        """
        if type(other) in [int, float]:
            return Matrix3x3(initial=[[other * self.matrix[i][j] for j in range(3)] for i in range(3)])

        elif isinstance(other, Matrix3x3):
            ret_mat = Matrix3x3()

            for i_self in range(3):
                for i_other in range(3):
                    s = 0
                    for j in range(3):
                        s += other[i_self][j] * self[j][i_other]
                    ret_mat[i_self][i_other] = s

            return ret_mat

        elif type(other) in [tuple, list]:
            self._test_input(other)

            ret_mat = Matrix3x3()

            for i_self in range(3):
                for i_other in range(3):
                    s = 0
                    for j in range(3):
                        s += other[i_self][j] * self[j][i_other]
                    ret_mat[i_self][i_other] = s

            return ret_mat

        else:
            raise TypeError

    def __iadd__(self, other):
        """
        Implement self += other

        :param other: a Matrix3x3 object or a list or tuple of list or tuple
        """
        if isinstance(other, Matrix3x3):
            for i in range(3):
                for j in range(3):
                    self.matrix[i][j] += other.matrix[i][j]
            return self
        elif type(other) in (list, tuple):
            self._test_input(other)

            for i in range(3):
                for j in range(3):
                    self.matrix[i][j] += other[i][j]
            return self
        else:
            raise TypeError

    def __isub__(self, other):
        """
        Implement self -= other

        :param other: a Matrix3x3 object or a list or tuple of list or tuple
        """
        if isinstance(other, Matrix3x3):
            for i in range(3):
                for j in range(3):
                    self.matrix[i][j] -= other.matrix[i][j]
            return self
        elif type(other) in (list, tuple):
            self._test_input(other)

            for i in range(3):
                for j in range(3):
                    self.matrix[i][j] -= other[i][j]
            return self
        else:
            raise TypeError

    def __imul__(self, other):
        """
        Implement self *= other

        :param other: a number or a Matrix3x3 object or a list or tuple of list or tuple
        :return: a Matrix3x3 object
        """
        if type(other) in [int, float]:
            for i in range(3):
                for j in range(3):
                    self.matrix[i][j] *= other

        elif isinstance(other, Matrix3x3):
            for i_self in range(3):
                for i_other in range(3):
                    s = 0
                    for j in range(3):
                        s += self[i_self][j] * other[j][i_other]
                    self[i_self][i_other] = s

        elif type(other) in [tuple, list]:
            self._test_input(other)

            for i_self in range(3):
                for i_other in range(3):
                    s = 0
                    for j in range(3):
                        s += self[i_self][j] * other[j][i_other]
                    self[i_self][i_other] = s

        else:
            raise TypeError

        return self

    def __itruediv__(self, other: [float, int]):
        """
        Implement self /= other

        :param other: a number
        """
        if other == 0:
            raise ZeroDivisionError
        for i in range(3):
            for j in range(3):
                self.matrix[i][j] /= other
        return self

    def __neg__(self):
        """
        Implement -self
        """
        for i in range(3):
            for j in range(3):
                self.matrix[i][j] = -self.matrix[i][j]
        return self

    def __eq__(self, other) -> bool:
        """
        Implement self == other

        :param other: a Matrix3x3 object, a list or a tuple of list or tuple
        :return: bool
        """
        if isinstance(other, Matrix3x3):

            i, i_max, test = 0, 3, True
            while i < i_max and test:

                j, j_max = 0, 3
                while j < j_max and test:
                    test = test and self.matrix[i][j] == other.matrix[i][j]
                    j += 1

                i += 1

        elif type(other) in (tuple, list):

            i, i_max, test = 0, 3, True
            while i < i_max and test:
                test = test and type(other[i]) in [list, tuple]

                j, j_max = 0, 3
                while j < j_max and test:
                    test = test and self.matrix[i][j] == other[i][j]
                    j += 1

                i += 1

        else:
            test = False

        return test

    def copy(self):
        """
        method to get a copy of the matrix

        :return: a Matrix3x3 object
        """
        return Matrix3x3(initial=self.matrix)

    def get_row(self, index: int) -> list:
        """
        method which return the row corresponding to the index (between 0 and 2, -1 allow to get last one)

        :param index: an integer
        :return: a list of number
        """
        if index < -1 or index > 3:
            raise IndexError
        return self.matrix[index]

    def get_column(self, index: int) -> list:
        """
        method which return the column corresponding to the index (between 0 and 2, -1 allow to get last one)

        :param index: an integer
        :return: a list of number
        """
        if index < -1 or index > 3:
            raise IndexError
        return [self.matrix[i][index] for i in range(3)]

    def get_matrix(self) -> list:
        """
        method which return the whole 3 by 3 matrix

        :return: a list of list of number
        """
        return self.matrix

    def set_row(self, new_row: [tuple, list], index: int):
        """
        method which change the row corresponding to the index for new_row
        index must be between 0 and 2 or -1 to get the last one

        :param new_row: a list of number
        :param index: an integer
        """
        if len(new_row) < 3:
            raise _err.LengthError

        i, i_max, test_type, test_length = 0, 3, True, True
        while i < i_max and test_type and test_length:
            test_type = test_type and type(new_row[i]) in [list, tuple]
            test_length = test_length and len(new_row[i]) >= 3
            i += 1

        if not test_length:
            raise _err.LengthError
        if not test_type:
            raise TypeError

        if index < -1 or index > 3:
            raise IndexError
        self.matrix[index] = new_row

    def set_column(self, new_column: [tuple, list], index: int):
        """
        method which change the column corresponding to the index for new_column
        index must be between 0 and 2 or -1 to get the last one

        :param new_column: a list of number
        :param index: an integer
        """
        if len(new_column) < 3:
            raise _err.LengthError

        i, i_max, test_type, test_length = 0, 3, True, True
        while i < i_max and test_type and test_length:
            test_type = test_type and type(new_column[i]) in [list, tuple]
            test_length = test_length and len(new_column[i]) >= 3
            i += 1

        if not test_length:
            raise _err.LengthError
        if not test_type:
            raise TypeError

        if index < -1 or index > 3:
            raise IndexError
        self.matrix[index][i] = new_column[i]

    def set_matrix(self, new_matrix: [tuple, list]):
        """
        method which change the whole matrix for new_matrix

        :param new_matrix: a list of list of number
        """
        self._test_input(new_matrix)

        self.matrix = new_matrix

    def get_transpose(self):
        """
        method to get a copy of the matrix which is its transpose

        :return: a Matrix3x3 object
        """
        new_matrix = list()

        for i in range(3):
            line = list()

            for j in range(3):
                line.append(self.matrix[j][i])

            new_matrix.append(line)

        return Matrix3x3(initial=new_matrix)

    def transpose(self):
        """
        method to transpose the matrix
        """
        for i in range(3):
            for j in range(3):
                self.matrix[i][j] = self.matrix[j][i]


class Matrix4x4(Matrix):
    def __init__(self, initial=None):
        """
        class to represent a 4 by 4 matrix

        ----------------------------------------------------------------------------------------------------------------

        Methods :

            .copy() -> Matrix4x4

            .get_row(index) -> list

            .get_column(index) -> list

            .get_matrix() -> list

            .get_row(new_row, index) -> None
                method to change the specified row

            .get_column(new_column, index) -> None
                method to change the specified column

            .get_matrix(new_matrix) -> None
                method to change the whole matrix

            .get_transpose() -> Matrix4x4

            .transpose() -> None
                method that transpose the matrix

        ----------------------------------------------------------------------------------------------------------------

        supported operations:

            + ; += : add each component

            - ; -= : sub each component
                     if put right before the object, multiply by -1 each component

            * ; *= : multiply by a scalar

            / ; // ; /= : divide by a scalar != 0

            == : test if each of the components are equal

            [y] : return the y-th line

        ----------------------------------------------------------------------------------------------------------------

        :param initial: list or tuple of list or tuple of number, optional, defaulted to None
        """
        super().__init__(4, 4)

        if initial is not None:
            self._test_input(initial)

            self.matrix = initial
        else:
            self.matrix = [
                [0 for _ in range(4)] for _ in range(4)
            ]

    def __add__(self, other):
        """
        Implement self + other

        :param other: a Matrix4x4 object or a list or tuple of list or tuple
        :return: a Matrix4x4 object
        """
        if isinstance(other, Matrix4x4):
            return Matrix4x4(initial=[[self.matrix[i][j] + other.matrix[i][j] for j in range(4)] for i in range(4)])
        elif type(other) in (list, tuple):
            self._test_input(other)

            return Matrix4x4(initial=[[self.matrix[i][j] + other[i][j] for j in range(4)] for i in range(4)])
        else:
            raise TypeError

    def __sub__(self, other):
        """
        Implement self - other

        :param other: a Matrix4x4 object or a list or tuple of list or tuple
        :return: a Matrix4x4 object
        """
        if isinstance(other, Matrix4x4):
            return Matrix4x4(initial=[[self.matrix[i][j] - other.matrix[i][j] for j in range(4)] for i in range(4)])
        elif type(other) in (list, tuple):
            self._test_input(other)

            return Matrix4x4(initial=[[self.matrix[i][j] - other[i][j] for j in range(4)] for i in range(4)])
        else:
            raise TypeError

    def __mul__(self, other):
        """
        Implement self * other

        :param other: a number or a Matrix4x4 object or a list or tuple of list or tuple
        :return: a Matrix4x4 object
        """
        if type(other) in [int, float]:
            return Matrix4x4(initial=[[self.matrix[i][j] * other for j in range(4)] for i in range(4)])

        elif isinstance(other, Matrix4x4):
            ret_mat = Matrix4x4()

            for i_self in range(4):
                for i_other in range(4):
                    s = 0
                    for j in range(4):
                        s += self[i_self][j] * other[j][i_other]
                    ret_mat[i_self][i_other] = s

            return ret_mat

        elif type(other) in [tuple, list]:
            self._test_input(other)

            ret_mat = Matrix4x4()

            for i_self in range(4):
                for i_other in range(4):
                    s = 0
                    for j in range(4):
                        s += self[i_self][j] * other[j][i_other]
                    ret_mat[i_self][i_other] = s

            return ret_mat

        else:
            raise TypeError

    def __truediv__(self, other: [float, int]):
        """
        Implement self / other

        :param other: a number
        :return: a Matrix4x4 object
        """
        if other != 0:
            raise ZeroDivisionError
        return Matrix4x4(initial=[[self.matrix[i][j] / other for j in range(4)] for i in range(4)])

    def __radd__(self, other):
        """
        Implement other + self

        :param other: a Matrix4x4 object or a list or tuple of list or tuple
        :return: a Matrix4x4 object
        """
        if isinstance(other, Matrix4x4):
            return Matrix4x4(initial=[[other.matrix[i][j] + self.matrix[i][j] for j in range(4)] for i in range(4)])
        elif type(other) in (list, tuple):
            self._test_input(other)

            return Matrix4x4(initial=[[other[i][j] + self.matrix[i][j] for j in range(4)] for i in range(4)])
        else:
            raise TypeError

    def __rsub__(self, other):
        """
        Implement other - self

        :param other: a Matrix4x4 object or a list or tuple of list or tuple
        :return: a Matrix4x4 object
        """
        if isinstance(other, Matrix4x4):
            return Matrix4x4(initial=[[other.matrix[i][j] - self.matrix[i][j] for j in range(4)] for i in range(4)])
        elif type(other) in (list, tuple):
            self._test_input(other)

            return Matrix4x4(initial=[[other[i][j] - self.matrix[i][j] for j in range(4)] for i in range(4)])
        else:
            raise TypeError

    def __rmul__(self, other):
        """
        Implement other * self

        :param other: a number or a Matrix4x4 object or a list or tuple of list or tuple
        :return: a Matrix4x4 object
        """
        if type(other) in [int, float]:
            return Matrix4x4(initial=[[other * self.matrix[i][j] for j in range(4)] for i in range(4)])

        elif isinstance(other, Matrix4x4):
            ret_mat = Matrix4x4()

            for i_self in range(4):
                for i_other in range(4):
                    s = 0
                    for j in range(4):
                        s += other[i_self][j] * self[j][i_other]
                    ret_mat[i_self][i_other] = s

            return ret_mat

        elif type(other) in [tuple, list]:
            self._test_input(other)

            ret_mat = Matrix4x4()

            for i_self in range(4):
                for i_other in range(4):
                    s = 0
                    for j in range(4):
                        s += other[i_self][j] * self[j][i_other]
                    ret_mat[i_self][i_other] = s

            return ret_mat

        else:
            raise TypeError

    def __iadd__(self, other):
        """
        Implement self += other

        :param other: a Matrix4x4 object or a list or tuple of list or tuple
        """
        if isinstance(other, Matrix4x4):
            for i in range(4):
                for j in range(4):
                    self.matrix[i][j] += other.matrix[i][j]
            return self
        elif type(other) in (list, tuple):
            self._test_input(other)

            for i in range(4):
                for j in range(4):
                    self.matrix[i][j] += other[i][j]
            return self
        else:
            raise TypeError

    def __isub__(self, other):
        """
        Implement self -= other

        :param other: a Matrix4x4 object or a list or tuple of list or tuple
        """
        if isinstance(other, Matrix4x4):
            for i in range(4):
                for j in range(4):
                    self.matrix[i][j] -= other.matrix[i][j]
            return self
        elif type(other) in (list, tuple):
            self._test_input(other)

            for i in range(4):
                for j in range(4):
                    self.matrix[i][j] -= other[i][j]
            return self
        else:
            raise TypeError

    def __imul__(self, other):
        """
        Implement self *= other

        :param other: a number or a Matrix4x4 object or a list or tuple of list or tuple
        :return: a Matrix4x4 object
        """
        if type(other) in [int, float]:
            for i in range(4):
                for j in range(4):
                    self.matrix[i][j] *= other

        elif isinstance(other, Matrix4x4):
            for i_self in range(4):
                for i_other in range(4):
                    s = 0
                    for j in range(4):
                        s += self[i_self][j] * other[j][i_other]
                    self[i_self][i_other] = s

        elif type(other) in [tuple, list]:
            self._test_input(other)

            for i_self in range(4):
                for i_other in range(4):
                    s = 0
                    for j in range(4):
                        s += self[i_self][j] * other[j][i_other]
                    self[i_self][i_other] = s

        else:
            raise TypeError

        return self

    def __itruediv__(self, other: [float, int]):
        """
        Implement self /= other

        :param other: a number
        """
        assert other != 0
        for i in range(4):
            for j in range(4):
                self.matrix[i][j] /= other
        return self

    def __neg__(self):
        """
        Implement -self
        """
        for i in range(4):
            for j in range(4):
                self.matrix[i][j] = -self.matrix[i][j]
        return self

    def __eq__(self, other) -> bool:
        """
        Implement self == other

        :param other: a Matrix4x4 object, a list or a tuple of list or tuple
        :return: bool
        """
        if isinstance(other, Matrix4x4):

            i, i_max, test = 0, 4, True
            while i < i_max and test:

                j, j_max = 0, 4
                while j < j_max and test:
                    test = test and self.matrix[i][j] == other.matrix[i][j]
                    j += 1

                i += 1

        elif type(other) in (tuple, list):

            i, i_max, test = 0, 4, True
            while i < i_max and test:
                test = test and type(other[i]) in [list, tuple]

                j, j_max = 0, 4
                while j < j_max and test:
                    test = test and self.matrix[i][j] == other[i][j]
                    j += 1

                i += 1

        else:
            test = False
        return test

    def copy(self):
        """
        method to get a copy of the matrix

        :return: a Matrix4x4 object
        """
        return Matrix4x4(initial=self.matrix)

    def get_row(self, index: int) -> list:
        """
        method which return the row corresponding to the index (between 0 and 3, -1 allow to get last one)

        :param index: an integer
        :return: a list of number
        """
        if index < -1 or index > 4:
            raise IndexError
        return self.matrix[index]

    def get_column(self, index: int) -> list:
        """
        method which return the column corresponding to the index (between 0 and 3, -1 allow to get last one)

        :param index: an integer
        :return: a list of number
        """
        if index < -1 or index > 4:
            raise IndexError
        return [self.matrix[i][index] for i in range(4)]

    def get_matrix(self) -> list:
        """
        method which return the whole 4 by 4 matrix

        :return: a list of list of number
        """
        return self.matrix

    def set_row(self, new_row: [tuple, list], index: int):
        """
        method which change the row corresponding to the index for new_row
        index must be between 0 and 3 or -1 to get the last one

        :param new_row: a list of number
        :param index: an integer
        """
        if len(new_row) < 4:
            raise _err.LengthError

        i, i_max, test_type, test_length = 0, 4, True, True
        while i < i_max and test_type and test_length:
            test_type = test_type and type(new_row[i]) in [list, tuple]
            test_length = test_length and len(new_row[i]) >= 4
            i += 1

        if not test_length:
            raise _err.LengthError
        if not test_type:
            raise TypeError

        if index < -1 or index > 4:
            raise IndexError

        self.matrix[index] = new_row

    def set_column(self, new_column: [tuple, list], index: int):
        """
        method which change the column corresponding to the index for new_column
        index must be between 0 and 3 or -1 to get the last one

        :param new_column: a list of number
        :param index: an integer
        """
        if len(new_column) < 4:
            raise _err.LengthError

        i, i_max, test_type, test_length = 0, 4, True, True
        while i < i_max and test_type and test_length:
            test_type = test_type and type(new_column[i]) in [list, tuple]
            test_length = test_length and len(new_column[i]) >= 4
            i += 1

        if not test_length:
            raise _err.LengthError
        if not test_type:
            raise TypeError

        if index < -1 or index > 4:
            raise IndexError
        for i in range(4):

            self.matrix[index][i] = new_column[i]

    def set_matrix(self, new_matrix: [tuple, list]):
        """
        method which change the whole matrix for new_matrix

        :param new_matrix: a list of list of number
        """
        self._test_input(new_matrix)

        self.matrix = new_matrix

    def get_transpose(self):
        """
        method to get a copy of the matrix which is its transpose

        :return: a Matrix4x4 object
        """
        new_matrix = list()

        for i in range(4):
            line = list()

            for j in range(4):
                line.append(self.matrix[j][i])

            new_matrix.append(line)

        return Matrix4x4(initial=new_matrix)

    def transpose(self):
        """
        method to transpose the matrix
        """
        for i in range(4):
            for j in range(4):
                self.matrix[i][j] = self.matrix[j][i]


# specials Matrices :
# Matrices 2 by 2
null_Matrix_2x2 = Matrix2x2()
unit_Matrix_2x2 = Matrix2x2([
    [1, 0],
    [0, 1],
])

# Matrices 3 by 3
null_Matrix_3x3 = Matrix3x3()
unit_Matrix_3x3 = Matrix3x3([[1 if i == j else 0 for j in range(3)] for i in range(3)])

# Matrices 4 by 4
null_Matrix_4x4 = Matrix4x4()
unit_Matrix_4x4 = Matrix4x4([[1 if i == j else 0 for j in range(4)] for i in range(4)])
