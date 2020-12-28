#! /usr/bin/env python3
# coding: utf-8

""" This module handles the controllers
    of this chess tournament manager
"""

import curses
import sys
import atexit
import logging

from view.main import CurseView
# from view.menu import MenuView
# from view.main import MainView

from model.menu import Menu

logging.basicConfig(filename="debug.txt", filemode="w", level=logging.DEBUG)


class Controller:
    """D """

    def __init__(self):
        logging.debug("< Open Controller")
        self.curses_view = CurseView()
        self.menu_model = Menu()

        atexit.register(self._close)

    def _close(self):
        logging.debug("> Close Controller")
        self.curses_view.close()

    # Main controls #

    def open_goodbye(self):
        self.curses_view.say_goodbye()
        # self._control_center()

    def open_test2(self):
        self.curses_view.print_center("Test2", self.curses_view.main)  # Pas de print ici

    def open_test3(self):
        self.curses_view.print_center("Test3", self.curses_view.main)  # Pas de print ici

    # Menu controls #

    def open_menu_base(self):
        options = self.menu_model.menu_base()
        colorset = [1, 2]
        self._control_menu(options, colorset)

    def open_tournois(self):
        options = self.menu_model.menu_tournois()
        colorset = [1, 2]
        self._control_menu(options, colorset)

    def open_tournois_select(self):
        options = self.menu_model.menu_tournois_select()
        colorset = [1, 2]
        self._control_menu(options, colorset)

    def open_tournoi_actions(self):
        options = self.menu_model.menu_tournoi_actions()
        colorset = [1, 2]
        self._control_menu(options, colorset)

    def open_rapports(self):
        options = self.menu_model.menu_rapports()
        colorset = [1, 2]
        self._control_menu(options, colorset)

    def quit(self):
        self.curses_view.say_goodbye()
        curses.napms(1000)
        sys.exit(0)

    # Private methods #

    def _align_to_larger(self, options):
        max_size = max([len(option) for option in options])
        return [option.ljust(max_size) for option in options]

    def _control_menu(self, options, colorset):

        logging.debug(f"CONTROL MENU : {options}")
        logging.debug(f"CONTROL MENU : {self.curses_view}")

        current_row = 0
        labels = [x[0] for x in options]
        actions = [x[1] for x in options]
        buttons = self._align_to_larger(labels)

        self.curses_view.display_menu(buttons, current_row, colorset)

        logging.debug("CONTROL MENU : pre while")

        while 1:
            key = self.curses_view.screen.getch()
            logging.debug(f"CONTROL MENU : key = {key}")
            logging.debug(f"CONTROL MENU : current_row = {current_row}")

            # clear existing texts
            self.curses_view.menu.clear()

            if key == curses.KEY_UP:
                logging.debug("KEY UP")
                if current_row > 0:
                    current_row -= 1
                else:
                    current_row = len(buttons) - 1
            elif key == curses.KEY_DOWN:
                logging.debug("KEY DOWN")
                if current_row < len(buttons) - 1:
                    current_row += 1
                else:
                    current_row = 0
            elif key == curses.KEY_ENTER or key in [10, 13]:
                logging.debug("KEY ENTER")

                if actions[current_row] is None:
                    self.curses_view.print_center(
                        "You selected '{}'".format(labels[current_row]),
                        self.curses_view.main
                    )
                    self.curses_view.screen.getch()
                else:
                    eval("self." + actions[current_row] + "()")

            self.curses_view.display_menu(buttons, current_row, colorset)
