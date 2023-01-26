
"""
google search butler

@author: Zaynn-Lea

see on git-hub :
    * author :
        - Zaynn-Lea : https://github.com/Zaynn-lea

    * project : https://github.com/Zaynn-lea/google_search_helper

------------------------------------------------------------------------------------------------------------------------

main file

app made in python using pygame and pygame_widgets
"""

import sys
import time
import webbrowser

import pygame
import pygame_widgets

import Boxes
import colors
import pygame_widgets_import as pwi


class World(object):
    def __init__(self, screen: pygame.surface, screen_size: tuple[int, int]):
        """
        class representing and handling the window, graphics and display

        ----------------------------------------------------------------------------------------------------------------

        Methods:

            .on_user_create() -> bool
                initialise the world

            .on_user_update(elapsed_time) -> bool
                update the world

            .display_text(start_pos, text, color)

            TODO

        ----------------------------------------------------------------------------------------------------------------

        :param screen: the pygame.surface object on witch this world is going to be applied
        :type: pygame.surface object
        :param screen_size: the width and the height of your world
        :type: a tuple of 2 integers
        """
        self.screen = screen
        self.screen_width, self.screen_high = self.screen_size = screen_size

        self.lst_box = []

    def on_user_create(self) -> bool:
        """
        method that you call to create the world before the pygame loop

        :return: bool
        """
        screen_width, screen_height = self.screen_size
        white = colors.colors["white"]

        # main app title
        self.display_text("Google Search Butler", ((screen_width // 2), 30), white,
                          is_center=(True, False), font_size=60)

        # +------------------------------------------------+
        # |  buttons to choose witch option you wanna add  |
        # +------------------------------------------------+

        # label :
        self.display_text("Add Options", ((screen_width // 2), 120), white,
                          is_center=(True, False), font_size=40)
        # buttons :
        normal_button = pwi.Button(self.screen, 50, 165, 70, 20, text="Normal", fontSize=25,
                                   onClick=lambda: self.lst_box.append(Boxes.Box(self, len(self.lst_box))))
        exact_button = pwi.Button(self.screen, 140, 165, 70, 20, text="Exact", fontSize=25,
                                  onClick=lambda: self.lst_box.append(Boxes.BoxExact(self, len(self.lst_box))))
        avoid_button = pwi.Button(self.screen, 230, 165, 70, 20, text="Avoid", fontSize=25,
                                  onClick=lambda: self.lst_box.append(Boxes.BoxAvoid(self, len(self.lst_box))))
        any_button = pwi.Button(self.screen, 320, 165, 70, 20, text="Any", fontSize=25,
                                onClick=lambda: self.lst_box.append(Boxes.BoxAny(self, len(self.lst_box))))

        def date_button_onclick():
            """
            function used locally for the date_button onClick parameter
            had to do it like that to have the try except block that you can't have using a lambda expression
            """
            selected = date_menu.getSelected()
            try:
                self.lst_box.append(selected(self, len(self.lst_box)))
            except TypeError:
                pass

        date_menu = pwi.Dropdown(self.screen, 410, 180, 70, 20, name="Type", choices=["Before", "After", "Range"],
                                 values=[
                                     lambda world, index: Boxes.BoxDate(world, index, box_type="Before"),
                                     lambda world, index: Boxes.BoxDate(world, index, box_type="After"),
                                     lambda world, index: Boxes.BoxDateRange(world, index),
                                 ], fontSize=25)
        date_button = pwi.Button(self.screen, 410, 150, 70, 20, text="Date", fontSize=25,
                                 onClick=date_button_onclick)

        # border :
        pygame.draw.line(self.screen, white, (30,                110), (30,                210), 2)  # left
        pygame.draw.line(self.screen, white, (screen_width - 30, 110), (screen_width - 30, 210), 2)  # right
        pygame.draw.line(self.screen, white, (30,                110), (screen_width - 30, 110), 2)  # top
        pygame.draw.line(self.screen, white, (screen_width - 30, 210), (30,                210), 2)  # bottom

        # +-------------------------+
        # | list of the input boxes |
        # +-------------------------+

        self.lst_box.append(Boxes.Box(self, 0))

        # +----------------------------+
        # | buttons for others actions |
        # +----------------------------+

        reset_button = pwi.Button(self.screen, (screen_width // 2) - 310, 440, 200, 40, text="Reset",
                                  fontSize=30, onClick=lambda: self.reset_lst_box())
        search_button = pwi.Button(self.screen, (screen_width // 2) - 100, 440, 200, 40, text="Search on the web",
                                   fontSize=30, onClick=lambda: self.search(search_mode_selection))
        search_mode_selection = pwi.Checkbox(self.screen, (screen_width // 2) + 110, 430, 200, 60,
                                             ("Without keyword", "With keyword"),
                                             colour=(150, 150, 150), fontSize=30)  # the same color as the button

        # TODO : making border radius to have a more pleasant experience

        return True

    def on_user_update(self, elapsed_time: float, lst_event: list) -> bool:
        """
        method that you call inside your pygame loop to update your world

        the parameter elapsed_time must be in nanosecond

        :param elapsed_time: the time since this function had been previously called
        :type: float
        :param lst_event: list of all the pygame event
        :type: list
        :return: bool
        """
        # TODO
        return True

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

        self.screen.blit(text_render, start_pos)

    def delete_box(self, box_index: int):
        """
        TODO
        """
        lst_left, del_box, lst_right = self.lst_box[:box_index], self.lst_box[box_index], self.lst_box[box_index + 1:]

        del_box_x, del_box_y = del_box.coord
        del_box_opp_x, del_box_opp_y = del_box.opp_coord

        del_box.delete_widgets()
        del del_box

        try:
            pygame.draw.rect(self.screen, colors.colors["black"],
                             (del_box_x, del_box_y, lst_right[-1].opp_x, lst_right[-1].opp_y))
        except IndexError:
            pygame.draw.rect(self.screen, colors.colors["black"],
                             (del_box_x, del_box_y, del_box_opp_x, del_box_opp_y))

        for i, box in enumerate(lst_right):
            box.update_index(box_index + i)

        self.lst_box = lst_left + lst_right

        if len(self.lst_box) == 0:
            self.lst_box.append(Boxes.Box(self, 0))

    def box_go_right(self, box_index: int):
        """
        TODO : debug, sometimes do weird stuff where the border or some entire box get blacked out
        """
        if (box_index != len(self.lst_box) - 1) and (len(self.lst_box) != 0):
            pygame.draw.rect(self.screen, colors.colors["black"],
                             (self.lst_box[box_index].x, self.lst_box[box_index].y,
                              self.lst_box[box_index + 1].opp_x, self.lst_box[box_index + 1].opp_y))

            self.lst_box[box_index + 1].update_index(box_index)
            self.lst_box[box_index].update_index(box_index + 1)

            self.lst_box[box_index + 1], self.lst_box[box_index] = self.lst_box[box_index], self.lst_box[box_index + 1]

    def box_go_left(self, box_index: int):
        """
        TODO : debug, sometimes do weird stuff where the border or some entire box get blacked out
        """
        if (box_index != 0) and (len(self.lst_box) != 0):
            pygame.draw.rect(self.screen, colors.colors["black"],
                             (self.lst_box[box_index - 1].x, self.lst_box[box_index - 1].y,
                              self.lst_box[box_index].opp_x, self.lst_box[box_index].opp_y))

            self.lst_box[box_index].update_index(box_index - 1)
            self.lst_box[box_index - 1].update_index(box_index)

            self.lst_box[box_index - 1], self.lst_box[box_index] = self.lst_box[box_index], self.lst_box[box_index - 1]

    def search(self, search_mode_selection: pwi.Checkbox):
        """
        TODO
        """
        query_parsed = "http://www.google.com/search?q="
        query_raw = "http://www.google.com/search?q="

        without_keyword, with_keyword = search_mode_selection.selected.copy()

        for i, box in enumerate(self.lst_box):
            if i:
                if box.box_type == "Avoid":
                    query_parsed += '-'
                else:
                    query_parsed += '+'
                    if box.box_type in ("Normal", "Exact"):
                        query_raw += '+'
            if box.box_type == "Avoid":
                query_parsed += box.get_text()
            else:
                query_parsed += box.get_text().strip().replace(' ', '+')
                if box.box_type in ("Normal", "Exact"):
                    query_raw += box.get_raw_text().strip().replace(' ', '+')

        if with_keyword:
            webbrowser.open(query_parsed)
        if without_keyword:
            webbrowser.open(query_raw)

    def reset_lst_box(self):
        """
        TODO
        """
        pygame.draw.rect(self.screen, colors.colors["black"],
                         (self.lst_box[0].x, self.lst_box[0].y, self.lst_box[-1].opp_x, self.lst_box[-1].opp_y))

        for box in self.lst_box:
            box.delete_widgets()
            del box

        self.lst_box.append(Boxes.Box(self, 0))


def main(*argv, **kwargv):
    pygame.init()

    screen_size = width, height = (1280, 720)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Google-Search's Butler")

    # structure to use and keep track of time
    delta_time = [time.time(), time.time(), lambda: delta_time[1] - delta_time[0]]

    # creating and starting the world
    world = World(screen, screen_size)
    world.on_user_create()

    # program/pygame loop
    running_state = True
    while running_state:

        lst_event = pygame.event.get()
        for event in lst_event:

            if event.type == pygame.QUIT:
                running_state = False

        # here's where the magic happen
        world.on_user_update(delta_time[2](), lst_event)

        pygame_widgets.update(lst_event)
        pygame.display.flip()

        # update the delta_time
        delta_time[0], delta_time[1] = delta_time[1], time.time()

    # to be sure we quit our interface
    pygame.quit()
    pygame.display.quit()


if __name__ == '__main__':
    main(*sys.argv)
