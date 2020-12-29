#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to handle the menu views
    of this chess tournament manager
"""

import curses
import curses.textpad
import logging


class CurseView:
    def __init__(self):
        logging.info("< Open Main View")

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
        self.menu = curses.newwin(10, maxW, maxH - 10, 0)
        self.main = curses.newwin(maxH - 10, maxW, 0, 0)

    def close(self):
        logging.info("> Close Main View")

        # reverse terminal settings
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()

        # close the application
        curses.endwin()

    def clear_menu(self):
        self.menu.clear()
        self.menu.refresh()

    def clear_main(self):
        self.main.clear()
        self.main.refresh()

    # --------------------------------

    def say_goodbye(self):
        self.print_center("Vous quittez le programme", self.screen)

    def display_menu(self, options, current_row, colors=[1, 2]):

        logging.info(f"DISPLAY MENU : {options}, {current_row}")

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
        self.menu.refresh()

    def print_center(self, text, screen):
        screen.clear()
        h, w = screen.getmaxyx()
        x = w // 2 - len(text) // 2
        y = h // 2
        screen.addstr(y, x, text)
        screen.refresh()

    def get_input(self, label, placeholder=None, errormsg=None):
        logging.info("DISPLAY INPUT")

        # turn on cursor blinking
        curses.curs_set(1)

        self.main.clear()
        h, w = self.main.getmaxyx()
        x = w // 2 - len(label) // 2
        y = h // 2
        self.main.addstr(y, x, label)

        logging.error(f"ERROR TXT: {errormsg}")
        if errormsg is not None:
            x = w // 2 - len(errormsg) // 2
            self.main.addstr(y + 5, x, errormsg)

        x = w // 2 - 40 // 2
        sub = self.main.subwin(3, 40, y + 1, x)
        sub.border()

        sub2 = sub.subwin(1, 38, y + 2, x + 1)
        if placeholder is not None:
            sub2.addstr(placeholder)

        tb = curses.textpad.Textbox(sub2)
        self.main.refresh()

        tb.edit()
        self.main.refresh()

        value = tb.gather()[:-1].strip()
        logging.debug(f"INPUT: ->{value}<-")

        # Reset the content of the input window
        tb.do_command(curses.ascii.SOH)
        tb.do_command(curses.ascii.VT)
        tb.do_command(curses.ascii.FF)
        sub.border()
        sub.refresh()

        # turn off cursor blinking
        curses.curs_set(0)

        return value
