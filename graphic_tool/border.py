
"""
submodule du package graphic_tool made to handle color definition and manipulation

@author: Zaynn-Lea

see on gitHub :
    * author :
        - Zaynn-Lea : https://github.com/Zaynn-lea

------------------------------------------------------------------------------------------------------------------------

this module contains :

    - Border : a class to have a border with the option of rounded corner with other options than pygame.draw.rect
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
    new_col = []

    for elt in col:
        if err.test_class(elt, float, int):
            new_col.append(int(elt))

        else:
            raise TypeError("The collection must contain only real number")

    if err.test_class(col, tuple):
        return tuple(new_col)
    return new_col


def _collection_to_abs(col: [list, tuple]) -> [list, tuple]:
    """
    TODO
    """
    new_col = []

    for elt in col:
        if err.test_class(elt, float, int):
            new_col.append(abs(elt))

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
                 border_radius:    [int, tuple[int, int, int, int], list[int, int, int, int], vector.Vector4D] = 0,
                 border_width:     int = 1):
        """
        TODO
        corner 0 ________________ corner 1
                /                \
                |                |
                |                |
        corner 2\________________/ corner 3
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
        # we need the absolute value when dealing with distances
        self.border_radius_dist = _collection_to_abs(border_temp)

        # border_width :

        self.border_width = border_width

    def draw(self, surface: pygame.Surface):
        """
        TODO
        """
        # top border :
        pygame.draw.line(surface, self.color,
                         (self.x_1 + self.border_radius_dist[0], self.y_1),
                         (self.x_2 - self.border_radius_dist[1], self.y_1), self.border_width)

        # bottom border :
        pygame.draw.line(surface, self.color,
                         (self.x_1 + self.border_radius_dist[2], self.y_2),
                         (self.x_2 - self.border_radius_dist[3], self.y_2), self.border_width)

        # left border :
        pygame.draw.line(surface, self.color,
                         (self.x_1, self.y_1 + self.border_radius_dist[0]),
                         (self.x_1, self.y_2 - self.border_radius_dist[2]), self.border_width)

        # right border :
        pygame.draw.line(surface, self.color,
                         (self.x_2, self.y_1 + self.border_radius_dist[1]),
                         (self.x_2, self.y_2 - self.border_radius_dist[3]), self.border_width)

        # top right corner :
        if self.border_radius[0] > 0:
            t_r_rect = pygame.Rect(self.x_1, self.y_1, self.border_radius_dist[0] * 2, self.border_radius_dist[0] * 2)
            pygame.draw.arc(surface, self.color, t_r_rect, 90, 180, self.border_width)

        elif self.border_radius[0] < 0:
            t_r_rect = pygame.Rect(
                self.x_1 - self.border_radius_dist[0],
                self.y_1 - self.border_radius_dist[0],
                self.border_radius_dist[0] * 2,
                self.border_radius_dist[0] * 2
            )
            pygame.draw.arc(surface, self.color, t_r_rect, 270, 0, self.border_width)

        # top left corner :
        if self.border_radius[1] > 0:
            t_r_rect = pygame.Rect(self.x_2, self.y_1, self.border_radius_dist[1] * 2, self.border_radius_dist[1] * 2)
            pygame.draw.arc(surface, self.color, t_r_rect, 0, 90, self.border_width)

        elif self.border_radius[1] < 0:
            t_r_rect = pygame.Rect(
                self.x_2 + self.border_radius_dist[1],
                self.y_1 - self.border_radius_dist[1],
                self.border_radius_dist[1] * 2,
                self.border_radius_dist[1] * 2
            )
            pygame.draw.arc(surface, self.color, t_r_rect, 180, 270, self.border_width)

        # bottom right corner :
        if self.border_radius[2] > 0:
            t_r_rect = pygame.Rect(self.x_1, self.y_2, self.border_radius_dist[2] * 2, self.border_radius_dist[2] * 2)
            pygame.draw.arc(surface, self.color, t_r_rect, 180, 270, self.border_width)

        elif self.border_radius[0] < 0:
            t_r_rect = pygame.Rect(
                self.x_1 - self.border_radius_dist[2],
                self.y_2 + self.border_radius_dist[2],
                self.border_radius_dist[2] * 2,
                self.border_radius_dist[2] * 2
            )
            pygame.draw.arc(surface, self.color, t_r_rect, 0, 90, self.border_width)

        # bottom left corner :
        if self.border_radius[3] > 0:
            t_r_rect = pygame.Rect(self.x_2, self.y_2, self.border_radius_dist[3] * 2, self.border_radius_dist[3] * 2)
            pygame.draw.arc(surface, self.color, t_r_rect, 270, 0, self.border_width)

        elif self.border_radius[3] < 0:
            t_r_rect = pygame.Rect(
                self.x_2 + self.border_radius_dist[3],
                self.y_2 + self.border_radius_dist[3],
                self.border_radius_dist[3] * 2,
                self.border_radius_dist[3] * 2
            )
            pygame.draw.arc(surface, self.color, t_r_rect, 90, 180, self.border_width)

    def is_in(self, coord: [tuple[int, int], list[int, int], vector.Vector2D]) -> bool:
        """
        TODO

        test if it's in the rectangle and if yes, we test if it's inside or outside of the circled corner
        """
        x = coord[0]
        y = coord[1]

        if self.x_1 < x < self.x_2 and self.y_1 < y < self.y_2:

            # test for the corners :
            # top right :
            if self.x_1 < x < self.x_1 + self.border_radius_dist[0]\
                    and self.y_1 < y < self.y_1 + self.border_radius_dist[0]:
                if self.border_radius[0] > 0:
                    return x * x + y * y <= self.border_radius_dist[0]

                elif self.border_radius[0] < 0:
                    return x * x + y * y >= self.border_radius_dist[0]

                else:
                    return True

            # top left :
            if self.x_2 > x > self.x_2 - self.border_radius_dist[1]\
                    and self.y_1 < y < self.y_1 + self.border_radius_dist[1]:
                if self.border_radius[1] > 0:
                    return x * x + y * y <= self.border_radius_dist[1]

                elif self.border_radius[1] < 0:
                    return x * x + y * y >= self.border_radius_dist[1]

                else:
                    return True

            # bottom right :
            if self.x_1 < x < self.x_1 + self.border_radius_dist[2]\
                    and self.y_2 > y > self.y_2 - self.border_radius_dist[2]:
                if self.border_radius[2] > 0:
                    return x * x + y * y <= self.border_radius_dist[2]

                elif self.border_radius[2] < 0:
                    return x * x + y * y >= self.border_radius_dist[2]

                else:
                    return True

            # bottom left :
            if self.x_2 > x > self.x_2 + self.border_radius_dist[3]\
                    and self.y_2 > y > self.y_2 + self.border_radius_dist[3]:
                if self.border_radius[3] > 0:
                    return x * x + y * y <= self.border_radius_dist[3]

                elif self.border_radius[3] < 0:
                    return x * x + y * y >= self.border_radius_dist[3]

                else:
                    return True

        return False

    def are_in(self, coord: [list[tuple[int, int], list[int, int], vector.Vector2D],
                             tuple[tuple[int, int], list[int, int], vector.Vector2D]]) -> [bool, list]:
        """
        TODO
        """
        test = []

        for elt in coord:
            test.append(self.is_in(elt))

        return test

    def erase(self,
              surface: pygame.Surface,
              background_color: [str, [int, int, int], tuple[int, int, int], vector.Vector3D]):
        """
        TODO
        """
        if err.test_class(background_color, str):
            self.color = colors.colors[background_color]
        else:
            if err.test_class(background_color, vector.Vector3D):
                color_temp = background_color.get_tuple()
            else:
                color_temp = background_color.copy()

            if 0 < color_temp[0] < 255 or 0 < color_temp[1] < 255 or 0 < color_temp[2] < 255:
                raise ValueError("color must use the rgb system, with 3 values ranging from 0 to 255")

            self.color = color_temp

        self.draw(surface)
