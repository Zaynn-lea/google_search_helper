
"""
submodule of the matrix subpackage made to handle the specific matrices definitions, operations and manipulations
used by JavidX9 in : https://www.youtube.com/watch?v=ih20l3pJoeU

I isolated them since they aren't the classic matrices, they are a specific implementation

@author: Zaynn-Lea

see on gitHub :
    * author :
        - Zaynn-Lea : https://github.com/Zaynn-lea

------------------------------------------------------------------------------------------------------------------------

    - XRotationMatrix4X4JavidX9, YRotationMatrix4X4JavidX9, ZRotationMatrix4X4JavidX9 :
            sub class for the rotation matrices

    - TranslationMatrixJavidX9 :
            sub class for the translation matrix

    - ProjectionMatrix4X4JavidX9 :
            sub class for the projection matrix
"""

from .matrix import *
from graphic_tool import vector


# +-------------------------------------------------+
# |     Matrix class from Javidx9's 3D tutorial     |
# |   https://www.youtube.com/watch?v=ih20l3pJoeU   |
# +-------------------------------------------------+
class XRotationMatrix4X4JavidX9(Matrix4x4):
    def __init__(self):
        """
        class to represent the rotation matrix of size 4 by 4 around the X axis used by Javidx9 in
        https://www.youtube.com/watch?v=ih20l3pJoeU
        inherit from Matrix4x4

        ----------------------------------------------------------------------------------------------------------------

        Methods :

            .update(theta) -> None
                update the matrix with the given angle
        """
        super().__init__(initial=[
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        self.theta = 0

    def update(self, angle: float):
        """
        method to update the rotation matrix to an angle

        :param angle: a float
        """
        self.theta = angle

        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)

        self[1][1] = cos_angle
        self[1][2] = sin_angle
        self[2][1] = -sin_angle
        self[2][2] = cos_angle


class YRotationMatrix4X4JavidX9(Matrix4x4):
    def __init__(self):
        """
        class to represent the rotation matrix of size 4 by 4 around the Y axis used by Javidx9 in
        https://www.youtube.com/watch?v=ih20l3pJoeU
        inherit from Matrix4x4

        ----------------------------------------------------------------------------------------------------------------

        Methods :

            .update(theta) -> None
                update the matrix with the given angle
        """
        super().__init__(initial=[
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        self.theta = 0

    def update(self, angle: float):
        """
        method to update the rotation matrix to an angle

        :param angle: a float
        """
        self.theta = angle

        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)

        self[0][0] = cos_angle
        self[0][2] = sin_angle
        self[2][0] = -sin_angle
        self[2][2] = cos_angle


class ZRotationMatrix4X4JavidX9(Matrix4x4):
    def __init__(self):
        """
        class to represent the rotation matrix of size 4 by 4 around the Z axis used by Javidx9 in
        https://www.youtube.com/watch?v=ih20l3pJoeU
        inherit from Matrix4x4

        ----------------------------------------------------------------------------------------------------------------

        Methods :

            .update(theta) -> None
                update the matrix with the given angle
        """
        super().__init__(initial=[
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        self.theta = 0

    def update(self, angle: float):
        """
        method to update the rotation matrix to an angle

        :param angle: a float
        """
        self.theta = angle

        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)

        self[0][0] = cos_angle
        self[0][1] = sin_angle
        self[1][0] = -sin_angle
        self[1][1] = cos_angle


class TranslationMatrixJavidX9(Matrix4x4):
    def __init__(self, initial_vector: [tuple, list, vector.Vector3D] = None):
        """
        class to represent the translation matrix of size 4 by 4 used by Javidx9 in
        https://www.youtube.com/watch?v=ih20l3pJoeU
        inherit from Matrix4x4

        ----------------------------------------------------------------------------------------------------------------

        Methods :

            .update_vector(new_vector) -> None
                update the matrix with the given vector

            .update_x(new_x) -> None
                update the matrix with the given coordinate

            .update_y(new_y) -> None
                update the matrix with the given coordinate

            .update_z(new_z) -> None
                update the matrix with the given coordinate

        ----------------------------------------------------------------------------------------------------------------

        :param initial_vector: a Vector3D object or a tuple of number or a list of number, optional, defaulted to None
        """
        x = y = z = 0
        if initial_vector is not None:
            if type(initial_vector) in (list, tuple):
                x, y, z = initial_vector

                if type(x) not in (int, float):
                    raise TypeError
                if type(y) not in (int, float):
                    raise TypeError
                if type(z) not in (int, float):
                    raise TypeError

                self.deplace_vector = vector.Vector3D(x, y, z)
            elif isinstance(initial_vector, vector.Vector3D):
                x, y, z = initial_vector.get_tuple()
                self.deplace_vector = initial_vector
            else:
                raise TypeError

        super().__init__([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [x, y, z, 1],
        ])

    def update_vector(self, new_vector: [tuple, list, vector.Vector3D],
                      operation: typing.Callable[[vector.Vector3D], vector.Vector3D] = None):
        """
        method to update the translation matrix by a new vector

        by default, it replaces the coordinate, but you can change it using the optional argument "operation"

        :param new_vector: a Vector3D object or a tuple of number or a list of number
        :param operation: a lambda function that take a Vector3D and return a Vector3D, optional, defaulted to None
        """
        x, y, z = self.deplace_vector.get_tuple()
        if type(new_vector) in (list, tuple):
            x, y, z = new_vector

            if type(x) not in (int, float):
                raise TypeError
            if type(y) not in (int, float):
                raise TypeError
            if type(z) not in (int, float):
                raise TypeError

        elif isinstance(new_vector, vector.Vector3D):
            x, y, z = new_vector.get_tuple()

        if operation is None:
            self.deplace_vector = vector.Vector3D(x, y, z)

            self[3][0] = x
            self[3][1] = y
            self[3][2] = z

        else:
            self.deplace_vector = operation(vector.Vector3D(x, y, z))

            self[3][0] = self.deplace_vector.x
            self[3][1] = self.deplace_vector.y
            self[3][2] = self.deplace_vector.z

    def update_x(self, new_x: [int, float], operation: typing.Callable[[float], float] = None):
        """
        method to update the translation matrix on the x coordinate

        by default, it replaces the coordinate, but you can change it using the optional argument "operation"

        :param new_x: a number
        :param operation: a lambda function that take a number and return a number, optional, defaulted to None
        """
        if operation is None:
            self[3][0] = self.deplace_vector.x = new_x
        else:
            self[3][0] = self.deplace_vector.x = operation(new_x)

    def update_y(self, new_y: [int, float], operation: typing.Callable[[float], float] = None):
        """
        method to update the translation matrix on the y coordinate

        by default, it replaces the coordinate, but you can change it using the optional argument "operation"

        :param new_y: a number
        :param operation: a lambda function that take a number and return a number, optional, defaulted to None
        """
        if operation is None:
            self[3][1] = self.deplace_vector.y = new_y
        else:
            self[3][1] = self.deplace_vector.y = operation(new_y)

    def update_z(self, new_z: [int, float], operation: typing.Callable[[float], float] = None):
        """
        method to update the translation matrix on the z coordinate

        by default, it replaces the coordinate, but you can change it using the optional argument "operation"

        :param new_z: a number
        :param operation: a lambda function that take a number and return a number, optional, defaulted to None
        """
        if operation is None:
            self[3][2] = self.deplace_vector.z = new_z
        else:
            self[3][2] = self.deplace_vector.z = operation(new_z)


class ProjectionMatrix4X4JavidX9(Matrix4x4):
    def __init__(self, screen_width: int,
                 screen_height: int,
                 fov: [int, float],
                 z_near: [int, float],
                 z_far: [int, float]):
        """
        class to represent the projection matrix of size 4 by 4 around the Y axis used by Javidx9 in
        https://www.youtube.com/watch?v=ih20l3pJoeU
        inherit from Matrix4x4

        ----------------------------------------------------------------------------------------------------------------

        :param screen_width: positiv integer
        :param screen_height: positiv integer
        :param fov: positiv number
        :param z_near: positiv number
        :param z_far: positiv number
        """
        if screen_width < 0:
            raise ValueError
        if screen_height < 0:
            raise ValueError

        if fov < 0:
            raise ValueError
        if z_near < 0:
            raise ValueError
        if z_far < 0:
            raise ValueError

        aspect_ratio = screen_height / screen_width
        fov_ratio = 1 / math.tan(fov * 0.5 / 180.0 * 3.1415926)

        super().__init__(initial=[
            [aspect_ratio * fov_ratio, 0,         0,                                    0],
            [0,                        fov_ratio, 0,                                    0],
            [0,                        0,         z_far / (z_far - z_near),             1],
            [0,                        0,         (-z_far * z_near) / (z_far - z_near), 0]
        ])


# special matrices :
# Pi (180°) rotation :
PI_X_rotation_matrix = Matrix4x4(initial=[
    [1,  0,  0, 0],
    [0, -1,  0, 0],
    [0,  0, -1, 0],
    [0,  0,  0, 1]
])
PI_y_rotation_matrix = Matrix4x4(initial=[
    [-1, 0,  0, 0],
    [0,  1,  0, 0],
    [0,  0, -1, 0],
    [0,  0,  0, 1]
])
PI_z_rotation_matrix = Matrix4x4(initial=[
    [-1,  0, 0, 0],
    [0,  -1, 0, 0],
    [0,   0, 1, 0],
    [0,   0, 0, 1]
])

