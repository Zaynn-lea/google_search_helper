
"""
submodule of the graphic_tool package made to handle definitions of triangles adn meshes of triangles

made by Gely Lea

------------------------------------------------------------------------------------------------------------------------

    - parse_char_index : a function to parse a string or list and extract a certain element surrounded by a character


    - Triangle : a class to represent a triangle in 3D space defined with its 3 vertices (Vector3D object)


    - Mesh : a class to represent a collection of Triangle
"""

from . import _error_handling as _err
from . import vector


# +-----------------------+
# |   parsing functions   |
# +-----------------------+
def parse_char_index(line: [str, list], char: str, index: int) -> [str, list]:
    """
    function that take a list or string and return the index + 1 th separated with the specified character

    :param line: a string or a list
    :param char: a character
    :param index: a positive integer
    :return: a string or a list
    """
    if len(char) != 1:
        raise _err.LengthError
    if index < 0:
        raise IndexError

    list_flag = isinstance(line, list)

    if list_flag:
        sub_line = list()  # for a list
    else:
        sub_line = str()  # for a string

    i, j, max_i, state = 0, 0, len(line), True

    # for each character in the line
    while i < max_i and state:
        # select the sub-line
        if str(line[i]) == char or i == 0:
            if j == index:
                while str(line[i]) == char:
                    i += 1
                k = i
                # extract the sub-line
                while k < max_i and str(line[k]) != char:
                    if list_flag:
                        sub_line.append(line[k])  # for a list
                    else:
                        sub_line += line[k]  # for a string
                    k += 1
                state = False
            else:
                j += 1
        i += 1

    return sub_line


# +--------------------+
# |   Triangle class   |
# +--------------------+
class Triangle(object):
    def __init__(self, vertex_1: [vector.Vector3D, list, tuple],
                 vertex_2: [vector.Vector3D, list, tuple],
                 vertex_3: [vector.Vector3D, list, tuple]):
        """
        class to represent a triangle in 3D space

        ----------------------------------------------------------------------------------------------------------------

        methods :

            .copy() -> Triangle

            .get_line(nbr) -> Vector3D

            .get_normal() -> Vector3D

            .get_middle() -> Vector3D

        ----------------------------------------------------------------------------------------------------------------

        supported operations:

            == : test if each vertex are equal

            [y] : return the y-th vertex

        ----------------------------------------------------------------------------------------------------------------

        :param vertex_1: Vector3D (or list or tuple of 3 int or float)
        :param vertex_2: Vector3D (or list or tuple of 3 int or float)
        :param vertex_3: Vector3D (or list or tuple of 3 int or float)
        """
        # to assure self.vertex_1 is a Vector3D object
        if type(vertex_1) != vector.Vector3D:
            if type(vertex_1[0]) not in (int, float):
                raise TypeError
            if type(vertex_1[1]) not in (int, float):
                raise TypeError
            if type(vertex_1[2]) not in (int, float):
                raise TypeError
            self.vertex_1 = vector.Vector3D(vertex_1[0], vertex_1[1], vertex_1[2])
        else:
            self.vertex_1 = vertex_1

        # to assure self.vertex_2 is a Vector3D object
        if type(vertex_2) != vector.Vector3D:
            if type(vertex_2[0]) not in (int, float):
                raise TypeError
            if type(vertex_2[1]) not in (int, float):
                raise TypeError
            if type(vertex_2[2]) not in (int, float):
                raise TypeError
            self.vertex_2 = vector.Vector3D(vertex_2[0], vertex_2[1], vertex_2[2])
        else:
            self.vertex_2 = vertex_2

        # to assure self.vertex_3 is a Vector3D object
        if type(vertex_3) != vector.Vector3D:
            if type(vertex_3[0]) not in (int, float):
                raise TypeError
            if type(vertex_3[1]) not in (int, float):
                raise TypeError
            if type(vertex_3[2]) not in (int, float):
                raise TypeError
            self.vertex_3 = vector.Vector3D(vertex_3[0], vertex_3[1], vertex_3[2])
        else:
            self.vertex_3 = vertex_3

    def __getitem__(self, y):
        """
        Implement self[y]

        :param y: a positive integer
        :return: a number
        """
        if y < -1 or y >= 3:
            raise IndexError

        match y:
            case 0:
                return self.vertex_1
            case 1:
                return self.vertex_2
            case 2:
                return self.vertex_3

    def __eq__(self, other):
        """
        Implement self == other

        :param other: a Triangle object
        :return: bool
        """
        return self.vertex_3 == other.vertex_3 and self.vertex_2 == other.vertex_2 and self.vertex_1 == other.vertex_1

    def copy(self):
        """
        method that return a copy of the triangle

        :return: a Triangle object
        """
        return Triangle(self.vertex_1, self.vertex_2, self.vertex_3)

    def get_line(self, nbr: int, inverse=False) -> vector.Vector3D:
        """
        method that return the line between vertex_nbr et vertex_(nbr+1) mod(3)
        so 1 <= nbr <= 3

        you can pass an optional parameter inverse, if it's True, it'll inverse the first and last point of the line

        :param nbr: an integer
        :param inverse: bool
        :return: a Vector3D object
        """
        if nbr < 0 or nbr > 3:
            raise ValueError
        if not isinstance(inverse, bool):
            raise TypeError

        signe = 1
        if inverse:
            signe = -1

        if nbr == 1:
            return signe * (self.vertex_2 - self.vertex_1)

        elif nbr == 2:
            return signe * (self.vertex_3 - self.vertex_2)

        elif nbr == 3:
            return signe * (self.vertex_1 - self.vertex_3)

    def get_normal(self) -> vector.Vector3D:
        """
        method that return the normal vector to the triangle, with normalise length

        :return: a Vector3D object
        """
        # normal = line1 ^ line2 (cross product)
        normal = vector.cross_product(self.get_line(3), -self.get_line(1))

        # normalising the length
        normal.normalise()

        return normal

    def get_middle(self) -> vector.Vector3D:
        """
        method that return the middle point of the triangle

        :return: a vector 3D object
        """
        return (self.vertex_1 + self.vertex_2 + self.vertex_3) / 3


# +----------------+
# |   Mesh class   |
# +----------------+
class Mesh(object):
    def __init__(self, initial=None):
        """
        class to represent the set of all triangle in a 3D space

        you can pass an optional parameter initial which is a lis, a tuple or a set of Triangle object which are already
        present in this 3D space

        ----------------------------------------------------------------------------------------------------------------

        Methods:

            .copy() -> Mesh

            .get_list() -> list[Triangle]
                return the list of triangle

            .add_triangle(Triangle) -> None
                add a new triangle to the mesh

            .add_triangle([Triangle, ...]) -> None
                add a list of new triangle to the mesh

            .is_empty() -> bool
                return True if the mesh is empty

            .empty() -> None
                empty the current mesh

            .offset(Vector3D) -> None
                offset the entire mesh by the vector

            .open_object_file(file_name) -> None
                add the content of a .obj file to the mesh

        ----------------------------------------------------------------------------------------------------------------

        Supported operations:

            + ; += : concatenate the two meshes

            == : test if each of the triangles are equal

        ----------------------------------------------------------------------------------------------------------------

        :param initial: list or tuple or set of Triangle object
        """
        if initial is not None:
            if type(initial) not in (list, tuple, set):
                raise TypeError

            i, i_max, test = 0, len(initial), True
            while i < i_max and test:
                test = test and type(initial[i]) == Triangle
                i += 1
            if not test:
                raise TypeError

            self.mesh = list(initial)
        else:
            self.mesh = []

    def __add__(self, other):
        """
        Implement self + other (concatenation)

        :param other: a Mesh object
        :return: Mesh
        """
        if not isinstance(other, Mesh):
            raise TypeError
        return self.mesh + other.mesh

    def __radd__(self, other):
        """
        Implement other + self (concatenation)

        :param other: a Mesh object
        :return: Mesh
        """
        if not isinstance(other, Mesh):
            raise TypeError
        return other.mesh + self.mesh

    def __iadd__(self, other):
        """
        Implement self += other (concatenation)

        :param other: a Mesh object
        :return: Mesh
        """
        if not isinstance(other, Mesh):
            raise TypeError
        self.mesh += other.mesh
        return self

    def __eq__(self, other):
        """
        Implement self == other

        :param other: a Mesh object
        :return: bool
        """
        if not isinstance(other, Mesh):
            raise TypeError

        test = len(self.mesh) == len(other.mesh)
        i, i_max = 0, len(self.mesh)
        while i < i_max and test:
            test = test and self.mesh[i] == other.mesh[i]
            i += 1

        return test

    def copy(self):
        """
        method that return a copy of the mesh

        :return: a Mesh object
        """
        return Mesh(initial=self.mesh)

    def get_list(self) -> list:
        """
        method that give back the list of all the triangle inside the mesh

        :return: a list of Triangle
        """
        return self.mesh

    def add_triangle(self, new_triangle: Triangle):
        """
        method which add new_triangle to the mesh

        :param new_triangle: Triangle object
        """
        self.mesh.append(new_triangle)

    def add_triangle_list(self, new_triangle: [list, tuple, set]):
        """
        method which add new_triangle to the mesh

        :param new_triangle: Triangle object
        """
        if type(new_triangle) not in (list, tuple, set):
            raise TypeError

        i, i_max, test = 0, len(new_triangle), True
        while i < i_max and test:
            test = test and type(new_triangle[i]) == Triangle
            i += 1
        if not test:
            raise TypeError
        self.mesh += list(new_triangle)

    def is_empty(self) -> bool:
        """
        Method to know if the mesh contain no triangle

        :return: bool
        """
        return len(self.mesh) == 0

    def empty(self):
        """
        method to empty the mesh
        """
        self.mesh = list()

    def offset(self, offset_vect: vector.Vector3D):
        """
        methode to offset each vertex of each triangle of this Mash by a certain amount : by offset_vect

        :param offset_vect: a Vector3D object
        """
        if vector.Vector3D != vector.null_vector_3D:
            for tri in self.mesh:
                tri.vertex_1 += offset_vect
                tri.vertex_2 += offset_vect
                tri.vertex_3 += offset_vect

    def load_object_file(self, file_name: str):
        """
        method to load a 3D object from a .obj file, this object will be transformed into a mesh
        and return a boolean: True if it worked and false otherwise
        Warning, it append the new object to the current mesh

        :param file_name: a string
        """
        if not file_name.endswith(".obj"):
            raise _err.ExtensionError

        # handle the opening of the file
        with open(file_name) as f:
            vertices = list()

            for line in f:
                if line[0] == 'v':
                    # if the line represent a vertex, we add it to the list
                    vertices.append(
                        vector.Vector3D(
                            float(parse_char_index(line, ' ', 1)),
                            float(parse_char_index(line, ' ', 2)),
                            float(parse_char_index(line, ' ', 3)),
                        )
                    )

                if line[0] == 'f':
                    # if the line represent a face, we add it to the mesh
                    self.mesh.append(
                        Triangle(
                            vertices[int(parse_char_index(parse_char_index(line, ' ', 1), '/', 0)) - 1],
                            vertices[int(parse_char_index(parse_char_index(line, ' ', 2), '/', 0)) - 1],
                            vertices[int(parse_char_index(parse_char_index(line, ' ', 3), '/', 0)) - 1],
                        )
                    )
