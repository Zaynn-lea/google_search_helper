
"""
submodule du package graphic_tool made to handle color definition and manipulation

@author: Zaynn-Lea

see on gitHub :
    * author :
        - Zaynn-Lea : https://github.com/Zaynn-lea

------------------------------------------------------------------------------------------------------------------------

this module contains :

    - distance : a function to compute the distance between 2 point in n dimension
"""

import math

from . import _error_handling as err
from . import vector


# +-------------------------+
# |   geometric functions   |
# +-------------------------+
def distance(first_point: [int, float, tuple, list, vector.Vector],
             second_point: [int, float, tuple, list, vector.Vector]) -> [int, float]:
    """
    function to compute the distance between 2 points

    the dimensions aren't important, if one point have a smaller dimension than the other,
    the coordinates will be completed by 0s

    --------------------------------------------------------------------------------------------------------------------

    :param first_point: one end of the distance
    :type: number | tuple(number) | int(number) | Vector object
    :param second_point: the other end of the distance
    :type: number | tuple(number) | int(number) | Vector object

    :return: the distane
    :type: number
    """
    first_point_temp = []
    second_point_temp = []

    if err.test_class(first_point, int, float):
        first_point_temp = [first_point]

    elif err.test_class(first_point, tuple, tuple):
        first_point_temp = list(first_point)

    elif err.test_class(first_point, vector.Vector):
        first_point_temp = first_point.get_tuple()

    if err.test_class(second_point, int, float):
        second_point_temp = [second_point]

    elif err.test_class(second_point, tuple, tuple):
        second_point_temp = list(second_point)

    elif err.test_class(second_point, vector.Vector):
        second_point_temp = second_point.get_tuple()

    length_1 = len(first_point_temp)
    length_2 = len(second_point_temp)

    if length_1 == length_2 == 1:
        return abs(first_point_temp[0] - second_point_temp[0])

    max_index = max(length_1, length_2)
    dist = 0

    for i in range(max_index):
        if not (err.test_class(first_point_temp[i], int, float) and err.test_class(second_point_temp[i], int, float)):
            raise TypeError("The coordinates of the points must be real numbers")

        if i >= length_1:
            dist += second_point_temp[i] ** 2

        elif i >= length_2:
            dist += first_point_temp[i] ** 2

        else:
            dist += (first_point_temp[i] - second_point_temp[i]) ** 2

    return math.sqrt(dist)

