#! /usr/bin/env python3
# coding: utf-8

""" This module handles the controllers
    of this chess tournament manager
"""

import curses
import time
import sys

from view.menu import MenuView
from view.main import MainView
from model.menu import Menu


class Controller:
    def __init__(self):
        pass


class MenuController:
    def __init__(self):
        self.view = MenuView()
        self.model = Menu()
        self.current_options = self.model.menu_base()

    # Options du menu #

    def open_menu_base(self):
        self.current_options = self.model.menu_base()
        self.open_menu()

    def open_tournois(self):
        self.current_options = self.model.menu_tournois()
        self.open_menu()

    def open_tournois_select(self):
        self.current_options = self.model.menu_tournois_select()
        self.open_menu()

    def open_tournoi_actions(self):
        self.current_options = self.model.menu_tournoi_actions()
        self.open_menu()

    def open_rapports(self):
        self.current_options = self.model.menu_rapports()
        self.open_menu()

    def quit(self):
        MainView.say_goodbye(self.stdscr)
        time.sleep(1)
        sys.exit(0)

    # Control du menu #

    def open_menu(self):
        curses.wrapper(self.control_menu)

    def close_menu(self):
        self.current_options = tuple()  # TODO ??

    def control_menu(self, stdscr):

        self.stdscr = stdscr

        current_row = 0
        labels = [x[0] for x in self.current_options]
        actions = [x[1] for x in self.current_options]
        buttons = self.align_to_larger(labels)

        self.view.display_menu(stdscr, current_row, buttons)

        while 1:
            key = stdscr.getch()

            # clear existing texts
            stdscr.clear()

            if key == curses.KEY_UP:
                if current_row > 0:
                    current_row -= 1
                else:
                    current_row = len(buttons) - 1
            elif key == curses.KEY_DOWN:
                if current_row < len(buttons) - 1:
                    current_row += 1
                else:
                    current_row = 0
            elif key == curses.KEY_ENTER or key in [10, 13]:

                if actions[current_row] is None:
                    self.view.print_center(
                        stdscr, "You selected '{}'".format(labels[current_row])
                    )
                    stdscr.getch()
                else:
                    eval("self." + actions[current_row] + "()")

            self.view.display_menu(stdscr, current_row, buttons)

    @staticmethod
    def align_to_larger(options):
        max_size = max([len(option) for option in options])
        return [option.ljust(max_size) for option in options]
