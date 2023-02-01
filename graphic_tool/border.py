
"""
submodule du package graphic_tool made to handle color definition and manipulation

@author: Zaynn-Lea

see on gitHub :
    * author :
        - Zaynn-Lea : https://github.com/Zaynn-lea

------------------------------------------------------------------------------------------------------------------------

this module contains :

    - TODO
"""

import pygame

from . import _error_handling as err
from . import colors
from . import functions
from . import vector


# +-------------------+
# |   internal tool   |
# +-------------------+
def _collection_to_int(col: [list, tuple]) -> [list, tuple]:
    """
    TODO
    """
    # TODO : error checking

    new_col = []

    for elt in col:
        if err.test_class(elt, float, int):
            new_col.append(int(elt))

        else:
            raise TypeError("The collection must contain only real number")

    if err.test_class(col, tuple):
        return tuple(new_col)
    return new_col


# +---------------------+
# |   Borders classes   |
# +---------------------+
class Border(object):
    def __init__(self,
                 coord_up_left:    [tuple[int, int], list[int, int], vector.Vector2D],
                 coord_down_right: [tuple[int, int], list[int, int], vector.Vector2D],
                 color:            [str, [int, int, int], tuple[int, int, int], vector.Vector3D],
                 border_radius:    [int, tuple[int, int, int, int], list[int, int, int, int], vector.Vector4D] = 0):
        """
        TODO
        """
        # coord_up_left :

        if err.test_class(coord_up_left, vector.Vector2D):
            self.x_1, self.y_1 = self.coord_up_left = _collection_to_int(coord_up_left.get_tuple())
        else:
            self.x_1, self.y_1 = self.coord_up_left = coord_up_left.copy()

        # coord_down_right :

        if err.test_class(coord_down_right, vector.Vector2D):
            self.x_2, self.y_2 = self.coord_up_left = _collection_to_int(coord_down_right.get_tuple())
        else:
            self.x_2, self.y_2 = self.coord_up_left = coord_down_right.copy()

        # sizes :

        self.width = functions.distance(self.x_1, self.x_2)
        self.height = functions.distance(self.y_1, self.y_2)
        self.size = self.width, self.height

        # colors :

        if err.test_class(color, str):
            self.color = colors.colors[color]
        else:
            if err.test_class(color, vector.Vector3D):
                color_temp = color.get_tuple()
            else:
                color_temp = color.copy()

            if 0 < color_temp[0] < 255 or 0 < color_temp[1] < 255 or 0 < color_temp[2] < 255:
                raise ValueError("color must use the rgb system, with 3 values ranging from 0 to 255")

            self.color = color_temp

        # border_radius :

        if err.test_class(border_radius, int):
            border_temp = [border_radius] * 4
        elif err.test_class(border_radius, vector.Vector3D):
            border_temp = _collection_to_int(border_radius.get_tuple())
        else:
            border_temp = border_radius.copy()

        if self.width > self.height:
            mini = self.height // 2
            mini_type = "height"
        else:
            mini = self.width // 2
            mini_type = "width"

        for i in range(4):
            if abs(border_radius[i]) > mini:
                raise ValueError(f"border_radius must not exceed half of {mini_type} ")

        self.border_radius = border_temp
