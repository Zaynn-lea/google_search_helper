
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

import colors
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
        self.x, self.y = self.coord = (15 + (index * 160), 260)
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
        self.left_button = pwi.Button(self.world.screen, x + 10, y + 30, 30, 20, text="<-",
                                      textColour=colors.colors["green"], font_size=30,
                                      onClick=lambda: self.world.box_go_left(self.index))
        self.delete_button = pwi.Button(self.world.screen, x + 60, y + 30, 30, 20, text="X",
                                        textColour=colors.colors["red"], font_size=30,
                                        onClick=lambda: self.world.delete_box(self.index))
        self.right_button = pwi.Button(self.world.screen, x + 110, y + 30, 30, 20, text="->",
                                       textColour=colors.colors["green"], font_size=30,
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
        self.x, self.y = self.coord = (15 + (new_index * 160), 260)
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

    def get_raw_text(self):
        """
        TODO
        """
        return self.text_input.getText()


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
        self.left_button = pwi.Button(self.world.screen, x + 10, y + 45, 30, 20, text="<-",
                                      textColour=colors.colors["green"], font_size=30,
                                      onClick=lambda: self.world.box_go_left(self.index))
        self.delete_button = pwi.Button(self.world.screen, x + 60, y + 45, 30, 20, text="X",
                                        textColour=colors.colors["red"], font_size=30,
                                        onClick=lambda: self.world.delete_box(self.index))
        self.right_button = pwi.Button(self.world.screen, x + 110, y + 45, 30, 20, text="->",
                                       textColour=colors.colors["green"], font_size=30,
                                       onClick=lambda: self.world.box_go_right(self.index))

    def update_index(self, new_index: int):
        """
        TODO
        """
        self.delete_widgets()
        self.index = new_index
        self.x, self.y = self.coord = (15 + (new_index * 160), 260)
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


class BoxDate(Box):
    def __init__(self, world, index: int, box_type: str = "Before"):
        """
        TODO
        """
        super().__init__(world, index, box_type=box_type)
        self.separator = '-'

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

        # label :
        self.display_text(self.box_type, (x + 75, y + 15), colors.colors["white"], is_center=(True, True), font_size=23)

        # buttons
        self.left_button = pwi.Button(self.world.screen, x + 10, y + 25, 30, 20, text="<-",
                                      textColour=colors.colors["green"], font_size=30,
                                      onClick=lambda: self.world.box_go_left(self.index))
        self.delete_button = pwi.Button(self.world.screen, x + 60, y + 25, 30, 20, text="X",
                                        textColour=colors.colors["red"], font_size=30,
                                        onClick=lambda: self.world.delete_box(self.index))
        self.right_button = pwi.Button(self.world.screen, x + 110, y + 25, 30, 20, text="->",
                                       textColour=colors.colors["green"], font_size=30,
                                       onClick=lambda: self.world.box_go_right(self.index))

        # date input
        self.year_input = pwi.TextBox(self.world.screen,  x + 5,   y + 65, 55, 30)
        self.month_input = pwi.TextBox(self.world.screen, x + 70,  y + 65, 35, 30)
        self.day_input = pwi.TextBox(self.world.screen,   x + 115, y + 65, 35, 30)

        # label for the input
        self.display_text("year",  (x + 32,  y + 50), colors.colors["white"], is_center=(True, False), font_size=20)
        self.display_text("month", (x + 87,  y + 50), colors.colors["white"], is_center=(True, False), font_size=20)
        self.display_text("day",   (x + 132, y + 50), colors.colors["white"], is_center=(True, False), font_size=20)

        # " / " between input boxes
        self.display_text('/', (x + 65,  y + 80), colors.colors["white"], is_center=(True, True), font_size=40)
        self.display_text('/', (x + 110, y + 80), colors.colors["white"], is_center=(True, True), font_size=40)

    def update_index(self, new_index: int):
        """
        TODO
        """
        year_transfer = self.year_input.getText()
        month_transfer = self.month_input.getText()
        day_transfer = self.day_input.getText()

        self.delete_widgets()
        self.index = new_index
        self.x, self.y = self.coord = (15 + (new_index * 160), 260)
        self.opp_x, self.opp_y = self.opp_coord = self.x + 150, self.y + 100
        self._create()

        self.year_input.setText(year_transfer)
        self.month_input.setText(month_transfer)
        self.day_input.setText(day_transfer)

    def delete_widgets(self):
        """
        TODO
        """
        self.delete_button.disable()
        self.left_button.disable()
        self.right_button.disable()
        self.year_input.disable()
        self.month_input.disable()
        self.day_input.disable()

        self.delete_button.hide()
        self.left_button.hide()
        self.right_button.hide()
        self.year_input.hide()
        self.month_input.hide()
        self.day_input.hide()

        del self.delete_button
        del self.left_button
        del self.right_button
        del self.year_input
        del self.month_input
        del self.day_input

    def get_text(self, parser=lambda x=0: None):
        """
        TODO
        """
        year = self.year_input.getText()
        month = self.month_input.getText()
        day = self.day_input.getText()

        if (len(year) == 0 or year is None)\
                and (len(month) == 0 or month is None)\
                and (len(day) == 0 or day is None):
            return ''

        # if not(year.isnumeric() and month.isnumeric() and day.isnumeric()):
        #     return ''  # TODO : better error handling in that case, like informing the user
        # TODO beter text for the isnumeric, the length and the order

        text = f"{self.box_type}:{year}{self.separator}" \
               f"{'00' if len(month) == 0 or month is None else month}{self.separator}" \
               f"{'00' if len(day) == 0 or day is None else day}"

        return text


class BoxDateRange(Box):
    def __init__(self, world, index: int):
        """
        TODO
        """
        super().__init__(world, index, box_type="Range")
        self.separator = '-'

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

        # label :
        self.display_text(self.box_type, (x + 75, y + 15), colors.colors["white"], is_center=(True, True), font_size=23)

        # buttons
        self.left_button = pwi.Button(self.world.screen, x + 10, y + 25, 30, 20, text="<-",
                                      textColour=colors.colors["green"], font_size=30,
                                      onClick=lambda: self.world.box_go_left(self.index))
        self.delete_button = pwi.Button(self.world.screen, x + 60, y + 25, 30, 20, text="X",
                                        textColour=colors.colors["red"], font_size=30,
                                        onClick=lambda: self.world.delete_box(self.index))
        self.right_button = pwi.Button(self.world.screen, x + 110, y + 25, 30, 20, text="->",
                                       textColour=colors.colors["green"], font_size=30,
                                       onClick=lambda: self.world.box_go_right(self.index))

        # first date input
        self.first_year_input = pwi.TextBox(self.world.screen,  x + 5,   y + 50, 55, 25)
        self.first_month_input = pwi.TextBox(self.world.screen, x + 70,  y + 50, 35, 25)
        self.first_day_input = pwi.TextBox(self.world.screen,   x + 115, y + 50, 35, 25)

        # last date input
        self.last_year_input = pwi.TextBox(self.world.screen,  x + 5,   y + 70, 55, 25)
        self.last_month_input = pwi.TextBox(self.world.screen, x + 70,  y + 70, 35, 25)
        self.last_day_input = pwi.TextBox(self.world.screen,   x + 115, y + 70, 35, 25)

        # label for the input
        # self.display_text("year",  (x + 32,  y + 50), colors.colors["white"], is_center=(True, False), font_size=20)
        # self.display_text("month", (x + 87,  y + 50), colors.colors["white"], is_center=(True, False), font_size=20)
        # self.display_text("day",   (x + 132, y + 50), colors.colors["white"], is_center=(True, False), font_size=20)

        # TODO : make the interface more easy to use

        # " / " between input boxes
        self.display_text('/', (x + 65,  y + 85), colors.colors["white"], is_center=(True, True), font_size=40)
        self.display_text('/', (x + 110, y + 85), colors.colors["white"], is_center=(True, True), font_size=40)

        self.display_text('/', (x + 65,  y + 65), colors.colors["white"], is_center=(True, True), font_size=40)
        self.display_text('/', (x + 110, y + 65), colors.colors["white"], is_center=(True, True), font_size=40)

    def update_index(self, new_index: int):
        """
        TODO
        """
        first_year_transfer = self.first_year_input.getText()
        first_month_transfer = self.first_month_input.getText()
        first_day_transfer = self.first_day_input.getText()
        last_year_transfer = self.last_year_input.getText()
        last_month_transfer = self.last_month_input.getText()
        last_day_transfer = self.last_day_input.getText()

        self.delete_widgets()
        self.index = new_index
        self.x, self.y = self.coord = (15 + (new_index * 160), 260)
        self.opp_x, self.opp_y = self.opp_coord = self.x + 150, self.y + 100
        self._create()

        self.first_year_input.setText(first_year_transfer)
        self.first_month_input.setText(first_month_transfer)
        self.first_day_input.setText(first_day_transfer)
        self.last_year_input.setText(last_year_transfer)
        self.last_month_input.setText(last_month_transfer)
        self.last_day_input.setText(last_day_transfer)

    def delete_widgets(self):
        """
        TODO
        """
        self.delete_button.disable()
        self.left_button.disable()
        self.right_button.disable()
        self.first_year_input.disable()
        self.first_month_input.disable()
        self.first_day_input.disable()
        self.last_year_input.disable()
        self.last_month_input.disable()
        self.last_day_input.disable()

        self.delete_button.hide()
        self.left_button.hide()
        self.right_button.hide()
        self.first_year_input.hide()
        self.first_month_input.hide()
        self.first_day_input.hide()
        self.last_year_input.hide()
        self.last_month_input.hide()
        self.last_day_input.hide()

        del self.delete_button
        del self.left_button
        del self.right_button
        del self.first_year_input
        del self.first_month_input
        del self.first_day_input
        del self.last_year_input
        del self.last_month_input
        del self.last_day_input

    def get_text(self, parser=lambda x=0: None):
        """
        TODO
        """
        first_year = self.first_year_input.getText()
        first_month = self.first_month_input.getText()
        first_day = self.first_day_input.getText()
        last_year = self.last_year_input.getText()
        last_month = self.last_month_input.getText()
        last_day = self.last_day_input.getText()

        if (len(first_year) == 0 or first_year is None)\
                and (len(first_month) == 0 or first_month is None)\
                and (len(first_day) == 0 or first_day is None)\
                and (len(last_year) == 0 or last_year is None)\
                and (len(last_month) == 0 or last_month is None)\
                and (len(last_day) == 0 or last_day is None):
            return ''

        # if not(first_year.isnumeric() and first_month.isnumeric() and first_day.isnumeric()
        #         and last_year.isnumeric() and last_month.isnumeric() and last_day.isnumeric()):
        #     return ''  # TODO : better error handling in that case, like informing the user
        # TODO beter text for the isnumeric, the length and the order

        text = f"{first_year}{self.separator}" \
               f"{'00' if len(first_month) == 0 or first_month is None else first_month}{self.separator}" \
               f"{'00' if len(first_day) == 0 or first_day is None else first_day}{self.separator}" \
               f"::{last_year}{self.separator}" \
               f"{'00' if len(last_month) == 0 or last_month is None else last_month}{self.separator}" \
               f"{'00' if len(last_day) == 0 or last_day is None else last_day}{self.separator}"

        return text
