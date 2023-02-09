
"""
submodule of the graphic_tool package made to handle definitions of vectors classes, vector manipulation and vector
opperrations

@author: Zaynn-Lea

see on gitHub :
    * author :
        - Zaynn-Lea : https://github.com/Zaynn-lea

------------------------------------------------------------------------------------------------------------------------

    - Vector : an abstract class to represent a vector

    - Vector2D : a class which inherit from Vector, represent a vector on the 2D plane

    - Vector3D : a class which inherit from Vector, represent a vector in 3D space

    - Vector4D : a class which inherit from Vector, represent a vector in 4D space
                (or just to have a 4th component in a 3D space for utility)

    - dot_product : a function to compute the dot product between two vectors of same dimension

    - cross_product : a function to compute the cross product between two vectors of same dimension

    - null_vector_2D, null_vector_3D and null_vector_4D : two specials vectors with every coordinate equal to 0
"""

import dataclasses
import math

from . import _error_handling as _err
from .matrix import matrix


# +-------------------+
# |   Vectors class   |
# +-------------------+
@dataclasses.dataclass(kw_only=True)
class Vector(object):
    def __init__(self, dimension: int):
        """
        This is an abstract vector class, used to derive Vector2D and Vector3D and enabling polymorphism
        """
        if dimension < 0:
            raise ValueError

        self.dimension = dimension

        self.x: [int, float] = None
        self.y: [int, float] = None
        self.z: [int, float] = None
        self.t: [int, float] = None

        self.__coord = [self.x, self.y, self.z, self.t]

    def __getitem__(self, y):
        """
        Implement self[y]

        :param y: a positive integer
        :return: a number
        """
        if y < -1 or y >= self.dimension:
            raise IndexError

        match y:
            case 0:
                return self.x
            case 1 if self.dimension > 1:
                return self.y
            case 2 if self.dimension > 2:
                return self.z
            case 3 if self.dimension > 3:
                return self.t

            case -1:
                match self.dimension:
                    case 1:
                        return self.x
                    case 2:
                        return self.y
                    case 3:
                        return self.z
                    case 4:
                        return self.t

    def get_tuple(self) -> tuple:
        """
        method that return the coord in a tuple

        form of the tuple :
            (x, y, ...)

        :return: tuple of int or float
        """
        return tuple(self.__coord.copy())


class Vector2D(Vector):
    def __init__(self, x: [int, float], y: [int, float]):
        """
        class to represent a 2D vector of component x, y

        this class inherit from Vector

        ----------------------------------------------------------------------------------------------------------------

        methods :

            .update_length() -> None:
                update self.length

            .copy() -> Vector2D

            .get_tuple() -> (x, y)

            .set_tuple((x, y)) -> None
                change the coord

            . get_normalise() -> Vector2D:

            .normalise() -> None:
                normalise the length

        ----------------------------------------------------------------------------------------------------------------

        supported operations:

            + ; += : add each component

            - ; -= : sub each component
                     if put right before the object, multiply by -1 each component

            * ; *= : multiply by a scalar or a matrix of same size place to the left

            / ; // : divide by a scalar != 0

            == : test if each of the components are equal

            [y] : return the y-th coordinate

        ----------------------------------------------------------------------------------------------------------------

        :param x: int or float
        :param y: int or float
        """
        super().__init__(2)

        self.x = x
        self.y = y

        self.length = 0
        self.update_length()

    def __add__(self, other):
        """
        Implement self + other

        :param other: a Vector2D object or a tuple or a list
        :return: a Vector2D object
        """
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        elif type(other) in (list, tuple):
            if len(other) < 2:
                raise _err.LengthError
            return Vector2D(self.x + other[0], self.y + other[1])
        else:
            raise TypeError

    def __sub__(self, other):
        """
        Implement self - other

        :param other: a Vector2D object or a tuple or a list
        :return: a Vector2D object
        """
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        elif type(other) in (list, tuple):
            if len(other) < 2:
                raise _err.LengthError
            return Vector2D(self.x - other[0], self.y - other[1])
        else:
            raise TypeError

    def __mul__(self, other: [int, float]):
        """
        Implement self * other

        :param other: a number
        :return: a Vector2D object
        """
        if type(other) in (int, float):
            return Vector2D(other * self.x, other * self.y)
        elif isinstance(other, matrix.Matrix2x2):
            return Vector2D(
                other.matrix[0][0] * self.x + other.matrix[0][1] * self.y,
                other.matrix[1][0] * self.x + other.matrix[1][1] * self.y,
            )
        elif type(other) in (tuple, list):
            if len(other) < 2:
                raise _err.LengthError

            if type(other[0]) not in [list, tuple]:
                raise TypeError
            if type(other[1]) not in [list, tuple]:
                raise TypeError

            if len(other[0]) < 2:
                raise _err.LengthError
            if len(other[1]) < 2:
                raise _err.LengthError

            return Vector2D(
                other[0][0] * self.x + other[0][1] * self.y,
                other[1][0] * self.x + other[1][1] * self.y,
            )
        else:
            raise TypeError

    def __truediv__(self, other: [int, float]):
        """
        Implement self / other

        :param other: a number
        :return: a Vector2D object
        """
        if other == 0:
            raise ZeroDivisionError
        return Vector2D(self.x / other, self.y / other)

    def __radd__(self, other):
        """
        Implement other + self

        :param other: a Vector2D object or a tuple or a list
        :return: a Vector2D object
        """
        if isinstance(other, Vector2D):
            return Vector2D(other.x + self.x, other.y + self.y)
        elif type(other) in (list, tuple):
            if len(other) < 2:
                raise _err.LengthError
            return Vector2D(other[0] + self.x, other[1] + self.y)
        else:
            raise TypeError

    def __rsub__(self, other):
        """
        Implement other - self

        :param other: a Vector2D object or a tuple or a list
        :return: a Vector2D object
        """
        if isinstance(other, Vector2D):
            return Vector2D(other.x - self.x, other.y - self.y)
        elif type(other) in (list, tuple):
            if len(other) < 2:
                raise _err.LengthError
            return Vector2D(other[0] - self.x, other[1] - self.y)
        else:
            raise TypeError

    def __rmul__(self, other):
        """
        Implement other * self

        :param other: a number or a Matrix2x2 object or a list or tuple of list or tuple
        :return: a Vector2D object
        """
        if type(other) in (int, float):
            return Vector2D(other * self.x, other * self.y)
        else:
            raise TypeError

    def __iadd__(self, other):
        """
        Implement self += other

        :param other: a Vector2D object or a tuple or a list
        """
        if isinstance(other, Vector2D):
            self.x += other.x
            self.y += other.y
            return self
        elif type(other) in (list, tuple):
            if len(other) < 2:
                raise _err.LengthError

            self.x += other[0]
            self.y += other[1]
            return self
        else:
            raise TypeError

    def __isub__(self, other):
        """
        Implement self -= other

        :param other: a Vector2D object or a tuple or a list
        """
        if isinstance(other, Vector2D):
            self.x -= other.x
            self.y -= other.y
            return self
        elif type(other) in (list, tuple):
            if len(other) < 2:
                raise _err.LengthError
            self.x -= other[0]
            self.y -= other[1]
            return self
        else:
            raise TypeError

    def __imul__(self, other: [int, float]):
        """
        Implement self *= other

        :param other: a number
        """
        self.x *= other
        self.y *= other
        return self

    def __itruediv__(self, other: [int, float]):
        """
        Implement self /= other

        :param other: a number
        """
        if other == 0:
            raise ZeroDivisionError
        self.x /= other
        self.y /= other
        return self

    def __neg__(self):
        """
        Implement -self
        """
        self.x, self.y = -self.x, -self.y
        return self

    def __eq__(self, other) -> bool:
        """
        Implement self == other

        :param other: a Vector2D object, a list or a tuple
        :return: bool
        """
        if isinstance(other, Vector2D):
            test = self.x == other.x and self.y == other.y
        elif type(other) in (tuple, list):
            test = len(other) >= 2 and self.x == other[0] and self.y == other[1]
        else:
            test = False
        return test

    def update_length(self):
        """
        method that update self.length
        """
        self.length = math.sqrt(self.x * self.x + self.y * self.y)

    def copy(self):
        """
        method that return a copy of the vector

        :return: a Vector2D object
        """
        return Vector2D(self.x, self.y)

    def get_tuple(self) -> tuple:
        """
        method that return the coord in a tuple

        form of the tuple :
            (x, y)

        :return: tuple of int or float
        """
        return self.x, self.y

    def set_tuple(self, new_coord: [tuple, list]):
        """
        method that change the coord for new_coord

        form of the tuple or list :
            (x, y)
            [x, y]

        :param new_coord: tuple or list of int or float
        """
        if len(new_coord) < 2:
            raise _err.LengthError
        if type(new_coord[0]) not in (int, float):
            raise TypeError
        if type(new_coord[1]) not in (int, float):
            raise TypeError

        self.x, self.y = new_coord
        self.update_length()

    def get_normalise(self):
        """
        method that return a new vector with normalised length

        :return: a Vector2D object
        """
        if self.length != 0 and self.length != 1:
            return Vector2D(self.x / self.length, self.y / self.length)
        return Vector2D(self.x, self.y)

    def normalise(self):
        """
        method that normalize the length of the vector
        """
        if self.length != 0 and self.length != 1:
            self.x /= self.length
            self.y /= self.length


class Vector3D(Vector):
    def __init__(self, x: [int, float], y: [int, float], z: [int, float]):
        """
        class to represent a 3D vector of component x, y, z

        this class inherit from Vector

        ----------------------------------------------------------------------------------------------------------------

        methods :

            .update_length() -> None:
                update self.length

            .copy() -> vector3D

            .get_tuple() -> (x, y, z)

            .set_tuple((x, y, z)) -> None
                change the coord

            . get_normalise() -> Vector3D:

            .normalise() -> None:
                normalise the length

        ----------------------------------------------------------------------------------------------------------------

        supported operations:

            + ; += : add each component

            - ; -= : sub each component
                     if put right before the object, multiply by -1 each component

            * ; *= : multiply by a scalar or a matrix of same size

            / ; // : divide by a scalar != 0

            == : test if each of the components are equal

            [y] : return the y-th coordinate

        ----------------------------------------------------------------------------------------------------------------

        :param x: int or float
        :param y: int or float
        :param z: int or float
        """
        super().__init__(3)

        self.x = x
        self.y = y
        self.z = z

        self.length = 0
        self.update_length()

    def __add__(self, other):
        """
        Implement self + other

        :param other: a Vector3D object or a tuple or a list
        :return: a Vector3D object
        """
        if isinstance(other, Vector3D):
            return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
        elif type(other) in (list, tuple):
            if len(other) < 3:
                raise _err.LengthError
            return Vector3D(self.x + other[0], self.y + other[1], self.z + other[2])
        else:
            raise TypeError

    def __sub__(self, other):
        """
        Implement self - other

        :param other: a Vector3D object or a tuple or a list
        :return: a Vector3D object
        """
        if isinstance(other, Vector3D):
            return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
        elif type(other) in (list, tuple):
            if len(other) < 3:
                raise _err.LengthError
            return Vector3D(self.x - other[0], self.y - other[1], self.z - other[2])
        else:
            raise TypeError

    def __mul__(self, other: [int, float]):
        """
        Implement self * other

        :param other: a number
        :return: a Vector3D object
        """
        if type(other) in (int, float):
            return Vector3D(other * self.x, other * self.y, other * self.z)
        elif isinstance(other, matrix.Matrix3x3):
            return Vector3D(
                other.matrix[0][0] * self.x + other.matrix[0][1] * self.y + other.matrix[0][2] * self.z,
                other.matrix[1][0] * self.x + other.matrix[1][1] * self.y + other.matrix[1][2] * self.z,
                other.matrix[2][0] * self.x + other.matrix[2][1] * self.y + other.matrix[2][2] * self.z,
            )
        elif type(other) in (tuple, list):
            if len(other) < 3:
                raise _err.LengthError

            i, i_max, test_size, test_type = 0, 3, True, True
            while i < i_max and test_size and test_type:
                test_type = test_type and type(other[i]) in [list, tuple]
                test_size = test_size and len(other) >= 3
                i += 1
            if not test_size:
                raise _err.LengthError
            if not test_type:
                raise TypeError

            return Vector3D(
                other[0][0] * self.x + other[0][1] * self.y + other[0][2] * self.z,
                other[1][0] * self.x + other[1][1] * self.y + other[1][2] * self.z,
                other[2][0] * self.x + other[2][1] * self.y + other[2][2] * self.z,
            )
        else:
            raise TypeError

    def __truediv__(self, other: [int, float]):
        """
        Implement self / other

        :param other: a number
        :return: a Vector3D object
        """
        if other == 0:
            raise ZeroDivisionError
        return Vector3D(self.x / other, self.y / other, self.z / other)

    def __radd__(self, other):
        """
        Implement other + self

        :param other: a Vector3D object or a tuple or a list
        :return: a Vector3D object
        """
        if isinstance(other, Vector3D):
            return Vector3D(other.x + self.x, other.y + self.y, other.z + self.z)
        elif type(other) in (list, tuple):
            if len(other) < 3:
                raise _err.LengthError
            return Vector3D(other[0] + self.x, other[1] + self.y, other[2] + self.z)
        else:
            raise TypeError

    def __rsub__(self, other):
        """
        Implement other - self

        :param other: a Vector3D object or a tuple or a list
        :return: a Vector3D object
        """
        if isinstance(other, Vector3D):
            return Vector3D(other.x - self.x, other.y - self.y, other.z - self.z)
        elif type(other) in (list, tuple):
            if len(other) < 3:
                raise _err.LengthError
            return Vector3D(other[0] - self.x, other[1] - self.y, other[2] - self.z)
        else:
            raise TypeError

    def __rmul__(self, other: [int, float]):
        """
        Implement other * self

        :param other: a number or a Matrix3x3 object or a list or tuple of list or tuple
        :return: a Vector3D object
        """
        if type(other) in (int, float):
            return Vector3D(other * self.x, other * self.y, other * self.z)
        else:
            raise TypeError

    def __iadd__(self, other):
        """
        Implement self += other

        :param other: a Vector3D object or a tuple or a list
        """
        if isinstance(other, Vector3D):
            self.x += other.x
            self.y += other.y
            self.z += other.z
            return self
        elif type(other) in (list, tuple):
            if len(other) < 3:
                raise _err.LengthError
            self.x += other[0]
            self.y += other[1]
            self.z += other[2]
            return self
        else:
            raise TypeError

    def __isub__(self, other):
        """
        Implement self -= other

        :param other: a Vector3D object or a tuple or a list
        """
        if isinstance(other, Vector3D):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
            return self
        elif type(other) in (list, tuple):
            if len(other) < 3:
                raise _err.LengthError
            self.x -= other[0]
            self.y -= other[1]
            self.z -= other[2]
            return self
        else:
            raise TypeError

    def __imul__(self, other: [int, float]):
        """
        Implement self *= other

        :param other: a number
        """
        self.x *= other
        self.y *= other
        self.z *= other
        return self

    def __itruediv__(self, other: [int, float]):
        """
        Implement self /= other

        :param other: a number
        """
        if other == 0:
            raise ZeroDivisionError
        self.x /= other
        self.y /= other
        self.z /= other
        return self

    def __neg__(self):
        """
        Implement -self
        """
        self.x, self.y, self.z = -self.x, -self.y, -self.z
        return self

    def __eq__(self, other) -> bool:
        """
        Implement self == other

        :param other: a Vector3D object, a list or a tuple
        :return: bool
        """
        if isinstance(other, Vector3D):
            test = self.x == other.x and self.y == other.y and self.z == other.z
        elif type(other) in (tuple, list):
            test = len(other) >= 3 and self.x == other[0] and self.y == other[1] and self.z == other[2]
        else:
            test = False
        return test

    def update_length(self):
        """
        method that update self.length
        """
        self.length = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def copy(self):
        """
        method that return a copy of the vector

        :return: a Vector3D object
        """
        return Vector3D(self.x, self.y, self.z)

    def get_tuple(self) -> tuple:
        """
        method that return the coord in a tuple

        form of the tuple :
            (x, y, z)

        :return: tuple of int or float
        """
        return self.x, self.y, self.z

    def set_tuple(self, new_coord: [tuple, list]):
        """
        method that change the coord for new_coord

        form of the tuple or list :
            (x, y, z)
            [x, y, z]

        :param new_coord: list or tuple of int or float
        """
        if len(new_coord) < 3:
            raise _err.LengthError
        if type(new_coord[0]) not in (int, float):
            raise TypeError
        if type(new_coord[1]) not in (int, float):
            raise TypeError
        if type(new_coord[2]) not in (int, float):
            raise TypeError

        self.x, self.y, self.z = new_coord
        self.update_length()

    def get_normalise(self):
        """
        method that return a new vector with normalised length

        :return: a Vector2D object
        """
        if self.length != 0 and self.length != 1:
            return Vector3D(self.x / self.length, self.y / self.length, self.z / self.length)
        return Vector3D(self.x, self.y, self.z)

    def normalise(self):
        """
        method that normalize the length of the vector
        """
        if self.length != 0 and self.length != 1:
            self.x /= self.length
            self.y /= self.length
            self.z /= self.length


class Vector4D(Vector):
    def __init__(self, x: [int, float], y: [int, float], z: [int, float], t: [int, float]):
        """
        class to represent a 4D vector of component x, y, z, t
        can be use as a 3D vector with an extra utility component

        this class inherit from Vector

        ----------------------------------------------------------------------------------------------------------------

        methods :

            .update_length() -> None:
                update self.length

            .copy() -> Vector4D

            .get_tuple() -> (x, y, z, t)

            .set_tuple((x, y, z, t)) -> None
                change the coord

            . get_normalise() -> Vector4D:

            .normalise() -> None:
                normalise the length

        ----------------------------------------------------------------------------------------------------------------

        supported operations:

            + ; += : add each component

            - ; -= : sub each component
                     if put right before the object, multiply by -1 each component

            * ; *= : multiply by a scalar or a matrix of same size place to the left

            / ; // : divide by a scalar != 0

            == : test if each of the components are equal

            [y] : return the y-th coordinate

        ----------------------------------------------------------------------------------------------------------------

        :param x: int or float
        :param y: int or float
        :param z: int or float
        :param t: int or float
        """
        super().__init__(4)

        self.x = x
        self.y = y
        self.z = z
        self.t = t

        self.length = 0
        self.update_length()

    def __add__(self, other):
        """
        Implement self + other

        :param other: a Vector4D object or a tuple or a list
        :return: a Vector4D object
        """
        if isinstance(other, Vector4D):
            return Vector4D(self.x + other.x, self.y + other.y, self.z + other.z, self.t + other.t)
        elif type(other) in (list, tuple):
            if len(other) < 4:
                raise _err.LengthError
            return Vector4D(self.x + other[0], self.y + other[1], self.z + other[2], self.t + other[3])
        else:
            raise TypeError

    def __sub__(self, other):
        """
        Implement self - other

        :param other: a Vector4D object or a tuple or a list
        :return: a Vector4D object
        """
        if isinstance(other, Vector4D):
            return Vector4D(self.x - other.x, self.y - other.y, self.z - other.z, self.t - other.t)
        elif type(other) in (list, tuple):
            if len(other) < 4:
                raise _err.LengthError
            return Vector4D(self.x - other[0], self.y - other[1], self.z - other[2], self.t - other[0])
        else:
            raise TypeError

    def __mul__(self, other: [int, float]):
        """
        Implement self * other

        :param other: a number
        :return: a Vector4D object
        """
        if type(other) in (int, float):
            return Vector4D(other * self.x, other * self.y, other * self.z, other * self.t)
        elif isinstance(other, matrix.Matrix4x4):
            return Vector4D(
                other.matrix[0][0] * self.x + other.matrix[0][1] * self.y + other.matrix[0][3] * self.t,
                other.matrix[1][0] * self.x + other.matrix[1][1] * self.y + other.matrix[1][3] * self.t,
                other.matrix[2][0] * self.x + other.matrix[2][1] * self.y + other.matrix[2][3] * self.t,
                other.matrix[3][0] * self.x + other.matrix[3][1] * self.y + other.matrix[3][3] * self.t,
            )
        elif type(other) in (tuple, list):
            if len(other) < 4:
                raise _err.LengthError

            i, i_max, test_size, test_type = 0, 4, True, True
            while i < i_max and test_size and test_type:
                test_type = test_type and type(other[i]) in [list, tuple]
                test_size = test_size and len(other) >= 4
                i += 1
            if not test_size:
                raise _err.LengthError
            if not test_type:
                raise TypeError

            return Vector4D(
                other[0][0] * self.x + other[0][1] * self.y + other[0][2] * self.z + other[0][3] * self.t,
                other[1][0] * self.x + other[1][1] * self.y + other[1][2] * self.z + other[1][3] * self.t,
                other[2][0] * self.x + other[2][1] * self.y + other[2][2] * self.z + other[2][3] * self.t,
                other[3][0] * self.x + other[3][1] * self.y + other[3][2] * self.z + other[3][3] * self.t,
            )
        else:
            raise TypeError

    def __truediv__(self, other: [int, float]):
        """
        Implement self / other

        :param other: a number
        :return: a Vector4D object
        """
        if other == 0:
            raise ZeroDivisionError
        return Vector4D(self.x / other, self.y / other, self.z / other, self.t / other)

    def __radd__(self, other):
        """
        Implement other + self
        :param other: a Vector4D object or a tuple or a list
        :return: a Vector4D object
        """
        if isinstance(other, Vector4D):
            return Vector4D(other.x + self.x, other.y + self.y, other.z + self.z, other.t + self.t)
        elif type(other) in (list, tuple):

            if len(other) < 4:
                raise _err.LengthError
            return Vector4D(other[0] + self.x, other[1] + self.y, other[2] + self.z, other[3] + self.t)
        else:
            raise TypeError

    def __rsub__(self, other):
        """
        Implement other - self

        :param other: a Vector4D object or a tuple or a list
        :return: a Vector4D object
        """
        if isinstance(other, Vector4D):
            return Vector4D(other.x - self.x, other.y - self.y, other.z - self.z, other.t - self.t)
        elif type(other) in (list, tuple):
            if len(other) < 4:
                raise _err.LengthError
            return Vector4D(other[0] - self.x, other[1] - self.y, other[2] - self.z, other[3] - self.t)
        else:
            raise TypeError

    def __rmul__(self, other: [int, float]):
        """
        Implement other * self

        :param other: a number or a Matrix4x4 object or a list or tuple of list or tuple
        :return: a Vector4D object
        """
        if type(other) in (int, float):
            return Vector4D(other * self.x, other * self.y, other * self.z, other * self.t)
        else:
            raise TypeError

    def __iadd__(self, other):
        """
        Implement self += other

        :param other: a Vector4D object or a tuple or a list
        """
        if isinstance(other, Vector4D):
            self.x += other.x
            self.y += other.y
            self.z += other.z
            self.t += other.t
        elif type(other) in (list, tuple):
            if len(other) < 4:
                raise _err.LengthError
            self.x += other[0]
            self.y += other[1]
            self.z += other[2]
            self.t += other[3]
        else:
            raise TypeError

    def __isub__(self, other):
        """
        Implement self -= other

        :param other: a Vector4D object or a tuple or a list
        """
        if isinstance(other, Vector4D):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
            self.t -= other.t
        elif type(other) in (list, tuple):
            if len(other) < 4:
                raise _err.LengthError
            self.x -= other[0]
            self.y -= other[1]
            self.z -= other[2]
            self.t -= other[3]
        else:
            raise TypeError

    def __imul__(self, other: [int, float]):
        """
        Implement self *= other

        :param other: a number
        """
        self.x *= other
        self.y *= other
        self.z *= other
        self.t *= other

    def __itruediv__(self, other: [int, float]):
        """
        Implement self /= other

        :param other: a number
        """
        if other == 0:
            raise ZeroDivisionError
        self.x /= other
        self.y /= other
        self.z /= other
        self.t /= other

    def __neg__(self):
        """
        Implement -self
        """
        self.x, self.y, self.z, self.t = -self.x, -self.y, -self.z, -self.t

    def __eq__(self, other) -> bool:
        """
        Implement self == other

        :param other: a Vector4D object, a list or a tuple
        :return: bool
        """
        if isinstance(other, Vector4D):
            test = self.x == other.x and self.y == other.y and self.z == other.z and self.t == other.t
        elif type(other) in (tuple, list):
            test = len(other) >= 4 and self.x == other[0] and self.y == other[1] \
                   and self.z == other[2] and self.t == other[3]
        else:
            test = False
        return test

    def update_length(self):
        """
        method that update self.length
        """
        self.length = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.t * self.t)

    def copy(self):
        """
        method that return a copy of the vector

        :return: a Vector4D object
        """
        return Vector4D(self.x, self.y, self.z, self.t)

    def get_tuple(self) -> tuple:
        """
        method that return the coord in a tuple

        form of the tuple :
            (x, y, z)

        :return: tuple of int or float
        """
        return self.x, self.y, self.z, self.t

    def set_tuple(self, new_coord: [tuple, list]):
        """
        method that change the coord for new_coord

        form of the tuple or list :
            (x, y, z, t)
            [x, y, z, t]

        :param new_coord: list or tuple of int or float
        """
        if len(new_coord) < 4:
            raise _err.LengthError
        if type(new_coord[0]) not in (int, float):
            raise TypeError
        if type(new_coord[1]) not in (int, float):
            raise TypeError
        if type(new_coord[2]) not in (int, float):
            raise TypeError
        if type(new_coord[3]) not in (int, float):
            raise TypeError

        self.x, self.y, self.z, self.t = new_coord
        self.update_length()

    def get_normalise(self):
        """
        method that return a new vector with normalised length

        :return: a Vector2D object
        """
        if self.length != 0 and self.length != 1:
            return Vector4D(self.x / self.length, self.y / self.length, self.z / self.length, self.t / self.length)
        return Vector4D(self.x, self.y, self.z, self.t)

    def normalise(self):
        """
        method that normalize the length of the vector
        """
        if self.length != 0 and self.length != 1:
            self.x /= self.length
            self.y /= self.length
            self.z /= self.length
            self.t /= self.length


# specials vectors :
null_vector_2D = Vector2D(0, 0)
null_vector_3D = Vector3D(0, 0, 0)
null_vector_4D = Vector4D(0, 0, 0, 0)


# vectors' functions :
def dot_product(vect_1: Vector, vect_2: Vector) -> [int, float]:
    """
    function to compute the dot product between two vectors
    the two vectors must be of same dimension

    :param vect_1: a Vector object
    :param vect_2: a Vector object
    :return: a number
    """
    if isinstance(vect_1, Vector2D) and isinstance(vect_2, Vector2D):
        return vect_1.x * vect_2.x + vect_1.y * vect_2.y

    elif isinstance(vect_1, Vector3D) and isinstance(vect_2, Vector3D):
        return vect_1.x * vect_2.x + vect_1.y * vect_2.y + vect_1.z * vect_2.z

    elif isinstance(vect_1, Vector4D) and isinstance(vect_2, Vector4D):
        return vect_1.x * vect_2.x + vect_1.y * vect_2.y + vect_1.z * vect_2.z + vect_1.t * vect_2.t

    else:
        raise TypeError


def cross_product(vect_1: [Vector3D], vect_2: [Vector3D]) -> [Vector3D]:
    """
    function to compute the cross product between two vectors
    the two vectors must be of same dimension
    and the dimension must be equal to 3

    :param vect_1: a Vector object
    :param vect_2: a Vector object
    :return: a Vector object
    """
    if isinstance(vect_1, Vector3D) and isinstance(vect_2, Vector3D):
        return Vector3D(
            vect_1.y * vect_2.z - vect_1.z * vect_2.y,
            vect_1.z * vect_2.x - vect_1.x * vect_2.z,
            vect_1.x * vect_2.y - vect_1.y * vect_2.x,
        )
    else:
        raise TypeError
