
"""
google search butler

@author: Zaynn-Lea

see on git-hub :
    * author :
        - Zaynn-Lea : https://github.com/Zaynn-lea

    * project : https://github.com/Zaynn-lea/google_search_helper

------------------------------------------------------------------------------------------------------------------------

file to handle the boxes used to have a good GUI for creating the query

app made in python using pygame and pygame_widgets
"""

import pygame
import pygame_widgets

from graphic_tool import colors
import pygame_widgets_import as pwi


class Box(object):
    def __init__(self, world, index: int, box_type: str = "Normal"):
        """
        TODO

        ----------------------------------------------------------------------------------------------------------------

        Methods:

            .display_text(start_pos, text, color)

        ----------------------------------------------------------------------------------------------------------------

        TODO
        """
        self.world = world
        self.box_type = box_type
        self.index = index
        self.x, self.y = self.coord = (15 + (index * 160), 230)
        self.opp_x, self.opp_y = self.opp_coord = self.x + 150, self.y + 100
        self._create()

    def _create(self):
        """
        TODO
        """
        x, y = self.coord
        opp_x, opp_y = self.opp_coord

        # border :

        pygame.draw.line(self.world.screen, colors.colors["white"], (x,     y),     (x,     opp_y), 2)  # left
        pygame.draw.line(self.world.screen, colors.colors["white"], (opp_x, y),     (opp_x, opp_y), 2)  # right
        pygame.draw.line(self.world.screen, colors.colors["white"], (x,     y),     (opp_x, y),     2)  # top
        pygame.draw.line(self.world.screen, colors.colors["white"], (x,     opp_y), (opp_x, opp_y), 2)  # bottom

        # label
        self.display_text(self.box_type, (x + 75, y + 15), colors.colors["white"], is_center=(True, True), font_size=23)

        # buttons
        self.left_button = pwi.Button(self.world.screen, x + 10, y + 30, 30, 20,
                                      text="<-", textColour=colors.colors["green"], font_size=30,
                                      onClick=lambda: self.world.box_go_left(self.index))
        self.delete_button = pwi.Button(self.world.screen, x + 60, y + 30, 30, 20,
                                        text="X", textColour=colors.colors["red"], font_size=30,
                                        onClick=lambda: self.world.delete_box(self.index))
        self.right_button = pwi.Button(self.world.screen, x + 110, y + 30, 30, 20,
                                       text="->", textColour=colors.colors["green"], font_size=30,
                                       onClick=lambda: self.world.box_go_right(self.index))

        # input:
        self.text_input = pwi.TextBox(self.world.screen, x + 5, y + 60, 140, 30)

    def display_text(self,
                     text:      str,
                     start_pos: tuple[[int, float], [int, float]],
                     color:     tuple[int, int, int],
                     is_center: tuple[bool, bool] = (False, False),
                     font:      str = None,
                     font_size: int = 20):
        """
        method to make displaying text more easy

        :param text: your text
        :type: str
        :param start_pos: the coordinates of the top right corner
        :type: tuple of 2 int or float
        :param color: the rgb code of the color
        :type: tuple of 3 int or float
        :param is_center: is the text center on the start_pos coord, defaulted to (False, False)
        :type: tuple of 2 bool
        :param font: file path to another font, defaulted to None (=default font of pygame)
        :type: str
        :param font_size: size of the font, defaulted to 20
        :type: int
        """
        text_render = pygame.font.Font(font, font_size).render(text, True, color)

        if is_center[0]:
            start_pos = (start_pos[0] - (text_render.get_size()[0] // 2), start_pos[1])
        if is_center[1]:
            start_pos = (start_pos[0], start_pos[1] - (text_render.get_size()[1] // 2))

        self.world.screen.blit(text_render, start_pos)

    def update_index(self, new_index: int):
        """
        TODO
        """
        text_transfer = self.text_input.getText()
        self.delete_widgets()
        self.index = new_index
        self.x, self.y = self.coord = (15 + (new_index * 160), 230)
        self.opp_x, self.opp_y = self.opp_coord = self.x + 150, self.y + 100
        self._create()
        self.text_input.setText(text_transfer)

    def delete_widgets(self):
        """
        TODO
        """
        self.delete_button.disable()
        self.left_button.disable()
        self.right_button.disable()
        self.text_input.disable()

        self.delete_button.hide()
        self.left_button.hide()
        self.right_button.hide()
        self.text_input.hide()

        del self.delete_button
        del self.left_button
        del self.right_button
        del self.text_input

    def get_text(self, parser=lambda x=0: None):
        """
        TODO
        """
        if (parser() is None) or (parser is None):
            return self.text_input.getText()
        return parser(self.text_input.getText())


class BoxExact(Box):
    def __init__(self, world, index: int):
        """
        TODO

        reminder : must use "" ... "" instead of " ... " to trick webbrowser.open()
        """
        super().__init__(world, index, box_type="Exact")
        self.separator_left, self.separator_right = self.separators = ('""', '""')

    def get_text(self, parser=lambda x=0: None):
        """
        TODO
        """
        text = self.separator_left

        for i, word in enumerate(self.text_input.getText().split(' ')):
            if i:
                text += '+'
            text += word

        text += self.separator_right

        if (parser() is None) or (parser is None):
            return text
        return parser(text)


class BoxAvoid(Box):
    def __init__(self, world, index: int):
        """
        TODO
        """
        super().__init__(world, index, box_type="Avoid")
        self.separator = '-'

    def get_text(self, parser=lambda x=0: None):
        """
        TODO
        """
        text = ''

        for i, word in enumerate(self.text_input.getText().split(' ')):
            if i:
                text += self.separator
            text += word

        return text


class BoxAny(Box):
    def __init__(self, world, index: int):
        """
        TODO
        """
        super().__init__(world, index, box_type="Any")
        self.separator = '*'

    def _create(self):
        """
        TODO
        """
        x, y = self.coord
        opp_x, opp_y = self.opp_coord

        # border :

        pygame.draw.line(self.world.screen, colors.colors["white"], (x,     y),     (x,     opp_y), 2)  # left
        pygame.draw.line(self.world.screen, colors.colors["white"], (opp_x, y),     (opp_x, opp_y), 2)  # right
        pygame.draw.line(self.world.screen, colors.colors["white"], (x,     y),     (opp_x, y),     2)  # top
        pygame.draw.line(self.world.screen, colors.colors["white"], (x,     opp_y), (opp_x, opp_y), 2)  # bottom

        # the label and buttons are centered because there is no input_text
        # label :
        self.display_text(self.box_type, (x + 75, y + 20), colors.colors["white"], is_center=(True, True), font_size=23)

        # buttons :
        self.left_button = pwi.Button(self.world.screen, x + 10, y + 45, 30, 20,
                                      text="<-", textColour=colors.colors["green"], font_size=30,
                                      onClick=lambda: self.world.box_go_left(self.index))
        self.delete_button = pwi.Button(self.world.screen, x + 60, y + 45, 30, 20,
                                        text="X", textColour=colors.colors["red"], font_size=30,
                                        onClick=lambda: self.world.delete_box(self.index))
        self.right_button = pwi.Button(self.world.screen, x + 110, y + 45, 30, 20,
                                       text="->", textColour=colors.colors["green"], font_size=30,
                                       onClick=lambda: self.world.box_go_right(self.index))

    def update_index(self, new_index: int):
        """
        TODO
        """
        self.delete_widgets()
        self.index = new_index
        self.x, self.y = self.coord = (15 + (new_index * 160), 230)
        self.opp_x, self.opp_y = self.opp_coord = self.x + 150, self.y + 100
        self._create()

    def delete_widgets(self):
        """
        TODO
        """
        self.delete_button.disable()
        self.left_button.disable()
        self.right_button.disable()

        self.delete_button.hide()
        self.left_button.hide()
        self.right_button.hide()

        del self.delete_button
        del self.left_button
        del self.right_button

    def get_text(self, parser=lambda x=0: None):
        """
        TODO
        """
        return '*'
