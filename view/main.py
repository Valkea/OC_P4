#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to handle the menu views
    of this chess tournament manager
"""

import curses
import logging


class CurseView:
    def __init__(self):
        logging.debug("< Open Main View")

        self.screen = curses.initscr()

        # tweak terminal settings
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        curses.curs_set(0)

        # Colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected row
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Menu 1
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)  # Menu 2

        self.screen.refresh()

        # Init menu window & main window
        maxH, maxW = self.screen.getmaxyx()
        self.menu = curses.newwin(10, maxW, 0, 0)
        self.main = curses.newwin(maxH-10, maxW, 10, 0)

    def close(self):
        logging.debug("> Close Main View")

        # reverse terminal settings
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()

        # close the application
        curses.endwin()

    def say_goodbye(self):
        self.print_center("Vous quittez le programme", self.screen)

    def display_menu(self, options, current_row, colors=[1, 2]):

        logging.debug(f"DISPLAY MENU : {options}, {current_row}")

        # turn off cursor blinking
        curses.curs_set(0)

        self.menu.bkgd(" ", curses.color_pair(colors[1]) | curses.A_BOLD)

        # clear screen
        self.menu.clear()

        # get screen size
        h, w = self.menu.getmaxyx()

        # display menu
        for i, option in enumerate(options):
            x = w // 2 - len(option) // 2
            y = h // 2 - len(options) // 2 + i

            if i == current_row:
                self.menu.attron(curses.color_pair(colors[0]))
                self.menu.addstr(y, x, option)
                self.menu.attroff(curses.color_pair(colors[0]))
            else:
                self.menu.addstr(y, x, option)

        # add window borders
        # self.menu.box("*", "*")
        self.menu.border()

        # update screen
        logging.debug("REFRESH")
        self.menu.refresh()

    def print_center(self, text, screen):
        screen.clear()
        h, w = screen.getmaxyx()
        x = w // 2 - len(text) // 2
        y = h // 2
        screen.addstr(y, x, text)
        screen.refresh()
