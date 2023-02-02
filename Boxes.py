
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


def test_and_handle_ymd(year_input, month_input, day_input) -> tuple[str, str, str]:
    """
    function to test the year, month and day for the BoxDate and BoxDateRange
    and if needed, modify them or raise error

    --------------------------------------------------------------------------------------------------------------------

    :param year_input: the raw year input from the input of the Box
    :type: str
    :param month_input: the raw mont input from the input of the Box
    :type: str
    :param day_input: the raw day input from the input of the Box
    :type: str

    :return:
    :type: tuple[str, str, str)
    """
    year = year_input  .replace(' ', '')[:4]
    month = month_input.replace(' ', '')[:2]
    day = day_input    .replace(' ', '')[:2]

    if not year.isnumeric():
        raise ValueError("Year must be a number")

    if (not month.isnumeric()) or len(month) == 0 or month is None:
        month = '00'

    if (not day.isnumeric()) or len(day) == 0 or day is None:
        day = '00'

    if not (0 <= int(month) <= 12):
        raise ValueError("Month must be between 0 and 12")

    # compute the number maximum of day in a month
    max_day = (29 if int(year) % 4 else 28) if int(month) == 2 else (30 if int(month) % 2 else 31)
    if not (0 <= int(day) <= max_day):
        raise ValueError(f"Day must be between 0 and {max_day}")

    return year, month, day


class Box(object):
    def __init__(self, world, index: int, box_type: str = "Normal"):
        """
        Base class to create a box for the Google butler app

        This class uses the packages pygame and pygame_widgets

        This class has a default parser :
            ' ' -> '+'

        This class allow you to customize the type and to add a parsing function

        Please refer to the documentation of each method for further explanation
        You can do that with help(Box.{method_name})

        ----------------------------------------------------------------------------------------------------------------

        Methods:

            .display_text(text, start_pos, color)

            .update_index(new_index)

            .delete_widgets()
                delete every widget of the box

            .get_text() -> parsed_text

            .get_raw_text() -> input_text

        ----------------------------------------------------------------------------------------------------------------

        :param world: the World class from the main.py class in the Google butler app
        :type: the World class from the main.py class in the Google butler app
        :param index: a positive integer, the position of this box in your line of boxes to create the query
        :type: int

        :param box_type: the name and representation of what the box is, optional defaulted to "Normal"
        :type: str
        """
        if index < 0:
            raise ValueError("iIndex must be positive")

        self.world = world
        self.box_type = box_type
        self.index = index
        self.x, self.y = self.coord = (15 + (index * 160), 260)
        self.opp_x, self.opp_y = self.opp_coord = self.x + 150, self.y + 100
        self._create()

    def _create(self):
        """
        method to create the GUI (border, buttons, labels and inputs)
        method used internally only
        """
        x, y = self.coord
        opp_x, opp_y = self.opp_coord

        # border :

        pygame.draw.line(self.world.screen, colors.colors["white"], (x,     y),     (x,     opp_y), 2)  # left
        pygame.draw.line(self.world.screen, colors.colors["white"], (opp_x, y),     (opp_x, opp_y), 2)  # right
        pygame.draw.line(self.world.screen, colors.colors["white"], (x,     y),     (opp_x, y),     2)  # top
        pygame.draw.line(self.world.screen, colors.colors["white"], (x,     opp_y), (opp_x, opp_y), 2)  # bottom

        # label
        self.display_text(self.box_type.capitalize(), (x + 75, y + 15),
                          colors.colors["white"], is_center=(True, True), font_size=23)

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

        ----------------------------------------------------------------------------------------------------------------

        :param text: your text
        :type: str
        :param start_pos: the coordinates of the top right corner
        :type: tuple of 2 int or float
        :param color: the rgb code of the color
        :type: tuple of 3 int or float

        :param is_center: is the text center on the start_pos coord, defaulted to (False, False)
        :type: tuple of 2 bool
        :param font: file path to another font, defaulted to None (uses the default font of pygame)
        :type: str
        :param font_size: size of the font, defaulted to 20
        :type: int
        """
        if start_pos[0] < 0 or start_pos[1] < 0:
            raise ValueError("start_pos must have positive coordinates")

        if 0 < color[0] < 255 or 0 < color[1] < 255 or 0 < color[2] < 255:
            raise ValueError("color must use the rgb system, with 3 values ranging from 0 to 255")

        text_render = pygame.font.Font(font, font_size).render(text, True, color)

        if is_center[0]:
            start_pos = (start_pos[0] - (text_render.get_size()[0] // 2), start_pos[1])
        if is_center[1]:
            start_pos = (start_pos[0], start_pos[1] - (text_render.get_size()[1] // 2))

        self.world.screen.blit(text_render, start_pos)

    def update_index(self, new_index: int):
        """
        method to change the position of this box relative to the other ones

        ----------------------------------------------------------------------------------------------------------------

        :param new_index: the new index where this box is located
        :type: int
        """
        if new_index < 0:
            raise ValueError("new_index must be positive")

        text_transfer = self.text_input.getText()
        self.delete_widgets()
        self.index = new_index
        self.x, self.y = self.coord = (15 + (new_index * 160), 260)
        self.opp_x, self.opp_y = self.opp_coord = self.x + 150, self.y + 100
        self._create()
        self.text_input.setText(text_transfer)

    def delete_widgets(self):
        """
        method to delete all the widgets of the box

        used internally in to update the position
        and to use if you need to delete the box, to have the widgets deleted from the display
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

    def get_text(self, parser=lambda x=0: x) -> str:
        """
        method to obtain the text from the input of this box

         parsing :
            ' ' -> '+'

        you can add a parser in parameter of the form :
            parser([str]) -> str

        ----------------------------------------------------------------------------------------------------------------

        :param parser: a function tacking a string as input and returning a string, optional defaulted to identity
        :type: function

        :return: the parsed input
        :type: str
        """
        if (parser() is None) or (parser is None):
            return self.text_input.getText().strip().replace(' ', '+')
        return parser(self.text_input.getText())

    def get_raw_text(self) -> str:
        """
        method to obtain the raw text from the input of this box, without any modification

        ----------------------------------------------------------------------------------------------------------------

        :return: the raw input
        :type: str
        """
        return self.text_input.getText()


class BoxExact(Box):
    def __init__(self, world, index: int):
        """
        Derived class to create a box for the Google butler app

        This class uses the packages pygame and pygame_widgets
        This class inherit from the Box class

        This class is specialized with a default parser :
            ' ' -> '+'
            the text get surrounded by double quotes "" [...] ""
                (must use "" ... "" instead of " ... " to trick webbrowser.open())

        Please refer to the documentation of each method for further explanation
        You can do that with help(BoxExact.{method_name})

        ----------------------------------------------------------------------------------------------------------------

        Methods:

            .display_text(text, start_pos, color)

            .update_index(new_index)

            .delete_widgets()
                delete every widget of the box

            .get_text() -> parsed_text

            .get_raw_text() -> input_text

        ----------------------------------------------------------------------------------------------------------------

        :param world: the World class from the main.py class in the Google butler app
        :type: the World class from the main.py class in the Google butler app
        :param index: a positive integer, the position of this box in your line of boxes to create the query
        :type: int
        """
        super().__init__(world, index, box_type="Exact")

        self.separator_left, self.separator_right = self.separators = ('""', '""')

    def get_text(self, parser=lambda x=0: None) -> str:
        """
        method to obtain the text from the input of this box

        specialized with a parsing :
            ' ' -> '+'
            the text get surrounded by double quotes "" [...] ""
                (must use "" ... "" instead of " ... " to trick webbrowser.open())

        you can add a parser in parameter of the form :
            parser([str]) -> str

        ----------------------------------------------------------------------------------------------------------------

        :param parser: a function tacking a string as input and returning a string, optional defaulted to identity
        :type: function

        :return: the parsed input
        :type: str
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
        Derived class to create a box for the Google butler app

        This class uses the packages pygame and pygame_widgets
        This class inherit from the Box class

        This class is specialized with a default parser :
            ' ' -> '+'
            add - at the beginning of the text

        Please refer to the documentation of each method for further explanation
        You can do that with help(BoxAvoid.{method_name})

        ----------------------------------------------------------------------------------------------------------------

        Methods:

            .display_text(text, start_pos, color)

            .update_index(new_index)

            .delete_widgets()
                delete every widget of the box

            .get_text() -> parsed_text

            .get_raw_text() -> input_text

        ----------------------------------------------------------------------------------------------------------------

        :param world: the World class from the main.py class in the Google butler app
        :type: the World class from the main.py class in the Google butler app
        :param index: a positive integer, the position of this box in your line of boxes to create the query
        :type: int
        """
        super().__init__(world, index, box_type="Avoid")

        self.separator = '-'

    def get_text(self, parser=lambda x=0: None) -> str:
        """
        method to obtain the text from the input of this box

        specialized with a parsing :
            ' ' -> '+'
            add - at the beginning of the text

        you can add a parser in parameter of the form :
            parser([str]) -> str

        ----------------------------------------------------------------------------------------------------------------

        :param parser: a function tacking a string as input and returning a string, optional defaulted to identity
        :type: function

        :return: the parsed input
        :type: str
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
        Derived class to create a box for the Google butler app

        This class uses the packages pygame and pygame_widgets
        This class inherit from the Box class

        This class will return only ' * ' as text since it has no input

        Please refer to the documentation of each method for further explanation
        You can do that with help(BoxAny.{method_name})

        ----------------------------------------------------------------------------------------------------------------

        Methods:

            .display_text(text, start_pos, color)

            .update_index(new_index)

            .delete_widgets()
                delete every widget of the box

            .get_text() -> parsed_text

            .get_raw_text() -> input_text

        ----------------------------------------------------------------------------------------------------------------

        :param world: the World class from the main.py class in the Google butler app
        :type: the World class from the main.py class in the Google butler app
        :param index: a positive integer, the position of this box in your line of boxes to create the query
        :type: int
        """
        super().__init__(world, index, box_type="Any")

        self.separator = '*'

    def _create(self):
        """
        method to create the GUI (border, buttons, labels and inputs)
        method used internally only

        had to overwrite it because the buttons aren't in the same place, and it has no input
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
        self.display_text(self.box_type.capitalize(), (x + 75, y + 20),
                          colors.colors["white"], is_center=(True, True), font_size=23)

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
        method to change the position of this box relative to the other ones

        had to overwrite it because it has no input

        ----------------------------------------------------------------------------------------------------------------

        :param new_index: the new index where this box is located
        :type: int
        """
        if new_index < 0:
            raise ValueError("new_index must be positive")

        self.delete_widgets()
        self.index = new_index
        self.x, self.y = self.coord = (15 + (new_index * 160), 260)
        self.opp_x, self.opp_y = self.opp_coord = self.x + 150, self.y + 100
        self._create()

    def delete_widgets(self):
        """
        method to delete all the widgets of the box

        had to overwrite it because it has no input

        used internally in to update the position
        and to use if you need to delete the box, to have the widgets deleted from the display
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

    def get_text(self, parser=lambda x=0: None) -> str:
        """
        method to obtain the text from the input of this box


        This class will return only ' * ' as text since it has no input

        you can add a parser in parameter of the form :
            parser([str]) -> str

        ----------------------------------------------------------------------------------------------------------------

        :param parser: a function tacking a string as input and returning a string, optional defaulted to identity
        :type: function

        :return: ' * ', or ' * ' parsed
        :type: str
        """
        if (parser() is None) or (parser is None):
            return '*'
        return parser('*')


class BoxDate(Box):
    def __init__(self, world, index: int, box_type: str = "Before"):
        """
        Derived class to create a box for the Google butler app

        This class uses the packages pygame and pygame_widgets
        This class inherit from the Box class

        This class is specialized with a default parser :
            [" before " or " after "]:yyyy-mm-dd

        Please refer to the documentation of each method for further explanation
        You can do that with help(BoxDate.{method_name})

        ----------------------------------------------------------------------------------------------------------------

        Methods:

            .display_text(text, start_pos, color)

            .update_index(new_index)

            .delete_widgets()
                delete every widget of the box

            .get_text() -> parsed_text

            .get_raw_text() -> input_text

        ----------------------------------------------------------------------------------------------------------------

        :param world: the World class from the main.py class in the Google butler app
        :type: the World class from the main.py class in the Google butler app
        :param index: a positive integer, the position of this box in your line of boxes to create the query
        :type: int

        :param box_type: the name and representation of what the box is, optional defaulted to "Before"
        :value: "Before" or "After"
        :type: str
        """
        if box_type.lower() not in ("before", "after"):
            raise ValueError("Box type for a date must be \" before \" or \" after \".")

        super().__init__(world, index, box_type=box_type)

        self.separator = '-'

    def _create(self):
        """
        method to create the GUI (border, buttons, labels and inputs)
        method used internally only

        had to overwrite it because the buttons aren't in the same place, and it has more inputs and labels
        """
        x, y = self.coord
        opp_x, opp_y = self.opp_coord

        # border :

        pygame.draw.line(self.world.screen, colors.colors["white"], (x,     y),     (x,     opp_y), 2)  # left
        pygame.draw.line(self.world.screen, colors.colors["white"], (opp_x, y),     (opp_x, opp_y), 2)  # right
        pygame.draw.line(self.world.screen, colors.colors["white"], (x,     y),     (opp_x, y),     2)  # top
        pygame.draw.line(self.world.screen, colors.colors["white"], (x,     opp_y), (opp_x, opp_y), 2)  # bottom

        # label :
        self.display_text(self.box_type.capitalize(), (x + 75, y + 15),
                          colors.colors["white"], is_center=(True, True), font_size=23)

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
        method to change the position of this box relative to the other ones

        had to overwrite it because it has more inputs and labels

        ----------------------------------------------------------------------------------------------------------------

        :param new_index: the new index where this box is located
        :type: int
        """
        if new_index < 0:
            raise ValueError("new_index must be positive")

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
        method to delete all the widgets of the box

        had to overwrite it because it has more inputs

        used internally in to update the position
        and to use if you need to delete the box, to have the widgets deleted from the display
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

    def get_text(self, parser=lambda x=0: None) -> str:
        """
        method to obtain the text from the input of this box

        This class is specialized with a default parser :
            [" before " or " after "]:yyyy-mm-dd

        you can add a parser in parameter of the form :
            parser([str]) -> str

        ----------------------------------------------------------------------------------------------------------------

        :param parser: a function tacking a string as input and returning a string, optional defaulted to identity
        :type: function

        :return: the parsed input
        :type: str
        """
        year, month, day = test_and_handle_ymd(
            self.year_input.getText(),
            self.month_input.getText(),
            self.day_input.getText()
        )

        text = f"{self.box_type.lower()}:{year}{self.separator}{month}{self.separator}{day}"

        if (parser() is None) or (parser is None):
            return text
        return parser(text)


class BoxDateRange(Box):
    def __init__(self, world, index: int):
        """
        Derived class to create a box for the Google butler app

        This class uses the packages pygame and pygame_widgets
        This class inherit from the Box class

        This class is specialized with a default parser :
            yyyy-mm-dd::yyyy-mm-dd

        Please refer to the documentation of each method for further explanation
        You can do that with help(BoxDateRange.{method_name})

        ----------------------------------------------------------------------------------------------------------------

        Methods:

            .display_text(text, start_pos, color)

            .update_index(new_index)

            .delete_widgets()
                delete every widget of the box

            .get_text() -> parsed_text

            .get_raw_text() -> input_text

        ----------------------------------------------------------------------------------------------------------------

        :param world: the World class from the main.py class in the Google butler app
        :type: the World class from the main.py class in the Google butler app
        :param index: a positive integer, the position of this box in your line of boxes to create the query
        :type: int
        """
        super().__init__(world, index, box_type="Range")

        self.separator = '-'

    def _create(self):
        """
        method to create the GUI (border, buttons, labels and inputs)
        method used internally only

        had to overwrite it because the buttons aren't in the same place, and it has more inputs and labels
        """
        x, y = self.coord
        opp_x, opp_y = self.opp_coord

        # border :

        pygame.draw.line(self.world.screen, colors.colors["white"], (x,     y),     (x,     opp_y), 2)  # left
        pygame.draw.line(self.world.screen, colors.colors["white"], (opp_x, y),     (opp_x, opp_y), 2)  # right
        pygame.draw.line(self.world.screen, colors.colors["white"], (x,     y),     (opp_x, y),     2)  # top
        pygame.draw.line(self.world.screen, colors.colors["white"], (x,     opp_y), (opp_x, opp_y), 2)  # bottom

        # label :
        self.display_text(self.box_type.capitalize(), (x + 75, y + 15),
                          colors.colors["white"], is_center=(True, True), font_size=23)

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
        method to change the position of this box relative to the other ones

        had to overwrite it because it has more inputs and labels

        ----------------------------------------------------------------------------------------------------------------

        :param new_index: the new index where this box is located
        :type: int
        """
        if new_index < 0:
            raise ValueError("new_index must be positive")

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
        method to delete all the widgets of the box

        had to overwrite it because it has more inputs

        used internally in to update the position
        and to use if you need to delete the box, to have the widgets deleted from the display
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

    def get_text(self, parser=lambda x=0: None) -> str:
        """
        method to obtain the text from the input of this box

        This class is specialized with a default parser :
            yyyy-mm-dd::yyyy-mm-dd

        you can add a parser in parameter of the form :
            parser([str]) -> str

        ----------------------------------------------------------------------------------------------------------------

        :param parser: a function tacking a string as input and returning a string, optional defaulted to identity
        :type: function

        :return: the parsed input
        :type: str
        """
        first_year, first_month, first_day = test_and_handle_ymd(
            self.first_year_input.getText(),
            self.first_month_input.getText(),
            self.first_day_input.getText()
        )
        last_year, last_month, last_day = test_and_handle_ymd(
            self.last_year_input.getText(),
            self.last_month_input.getText(),
            self.last_day_input.getText()
        )

        text = f"{first_year}{self.separator}{first_month}{self.separator}{first_day}" \
               f"::{last_year}{self.separator}{last_month}{self.separator}{last_day}"

        if (parser() is None) or (parser is None):
            return text
        return parser(text)
