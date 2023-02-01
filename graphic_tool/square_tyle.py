
"""
submodule of the graphic_tool package made to handle definitions of 2D square tyles

@author: Zaynn-Lea

see on gitHub :
    * author :
        - Zaynn-Lea : https://github.com/Zaynn-lea

------------------------------------------------------------------------------------------------------------------------

    - Tyle : an abstract class to represent a tyle

    - SqTyle : a base class to represent a square tyle

    - SqPathTyle : a class to represent a square tyle containing or acting like a path

    - SqVegetationTyle : a class to represent a square tyle containing or acting like a vegetation
"""

import pygame

from . import _error_handling as _err
from . import vector


# +------------------+
# |   Tyle classes   |
# +------------------+
class Tyle(object):
    def __init__(self):
        """
        this is an abstract Tyle class, used to derive SqtTyle and HexTyle and enabling polymorphism
        """
        pass

    def draw(self, surface: pygame.Surface, coord: [tuple, list, vector.Vector2D]):
        """
        this method is to draw the tyle

        :param coord: a Vector2D object a tuple or list of integer
        :param surface: a Pygame.Surface object
        """
        pass


# +-------------------------+
# |   Square Tyle classes   |
# +-------------------------+
class SqTyle(Tyle):
    def __init__(self):
        """
        base class for square tyle objects

        ----------------------------------------------------------------------------------------------------------------

        Methods :

            .draw(surface, coord) -> None
                draw the tyle on the surface
        """
        super().__init__()

        self.is_walkable = False
        self.is_interactable = False
        self.deplacement_dificulty = 1
        self.orientation = 0

        self.image = pygame.image.load("image/tyle/nothing_tyle.png")

    def draw(self, surface: pygame.Surface, coord: [tuple, list, vector.Vector2D]):
        """
        method to draw the tyle, the coord are the top left coord

        :param coord: a Vector2D object a tuple or list of integer
        :param surface: a Pygame.Surface object
        """
        image = pygame.transform.rotate(self.image, 90 * self.orientation)

        if isinstance(coord, vector.Vector2D):
            surface.blit(image, (int(coord.get_tuple()[0]), int(coord.get_tuple()[1])))

        elif type(coord) in (list, tuple):
            if len(coord) < 2:
                raise _err.LengthError
            if type(coord[0]) not in (int, float):
                raise TypeError
            if type(coord[1]) not in (int, float):
                raise TypeError

            surface.blit(image, (int(coord[0]), int(coord[1])))

        else:
            raise TypeError


default_square_tyle = SqTyle()


class SqPathTyle(SqTyle):
    path_type_dico = {
        # classic/straight
        "end": None,
        "straight": None,
        "corner": None,
        "T": None,
        "cross": None,
    }

    def __init__(self, path_type: str, path_image: str, rotation: int = 0):
        """
        class to represent every path tyle (see bellow for list)

        ----------------------------------------------------------------------------------------------------------------

        Methods :

            .draw(surface, coord) -> None
                draw the tyle on the surface

        ----------------------------------------------------------------------------------------------------------------

        :param path_type: a string
        :param path_image: a string
        """
        super().__init__()

        self.is_walkable = True
        self.orientation = rotation

        self.path_type = path_type

        size = len(path_image)
        if path_image[size - 4:size].lower() not in (".png", ".jpg", ".gif", ".bmp"):
            raise _err.ExtensionError

        self.image = pygame.image.load(path_image)


class SqVegetationTyle(SqTyle):
    def __init__(self, path_image: str):
        """
        class to represent every path tyle (see bellow for list)

        ----------------------------------------------------------------------------------------------------------------

        Methods :

            .draw(surface, coord) -> None
                draw the tyle on the surface

        ----------------------------------------------------------------------------------------------------------------

        :param path_image: a string
        """
        super().__init__()

        size = len(path_image)
        if path_image[size - 4:size].lower() not in (".png", ".jpg", ".gif", ".bmp"):
            raise _err.ExtensionError

        self.image = pygame.image.load(path_image)
        self.deplacement_dificulty = 3
