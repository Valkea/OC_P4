#! /usr/bin/env python3
# coding: utf-8

""" This module handles the controllers
    of this chess tournament manager
"""

import curses
import sys
import atexit
import logging

# import random

from view.main import CurseView
from model.tournament import Tournament, World

# from view.menu import MenuView
# from view.main import MainView

from model.menu import Menu


class Controller:
    """D """

    def __init__(self):
        logging.info("< Open Controller")

        self.curses_view = CurseView()
        self.world_model = World()
        self.menu_model = Menu()

        self.focus = "menu"
        atexit.register(self._close)

    def _close(self):
        logging.info("> Close Controller")
        self.curses_view.close()

    # Main controls #

    def start(self):
        while 1:
            logging.debug(f"LOOP {self.focus}")
            key = self.curses_view.screen.getch()
            logging.debug(f"LOOP : key = {key}")

            if key == 9:
                self.focus = "main" if self.focus == "menu" else "menu"

            if self.focus == "menu":
                self._get_menu(key)
            else:
                logging.debug("RIEN")
                self._get_main(key)

            self.getkey = True

    # Menu controls #

    def open_menu_base(self):
        options = self.menu_model.menu_base()
        colorset = [1, 2]
        self._set_menu(options, colorset)

    def open_tournois(self):
        options = self.menu_model.menu_tournois()
        colorset = [1, 2]
        self._set_menu(options, colorset)
        # self.focus = "main"

    def open_tournois_select(self):
        options = self.menu_model.menu_tournois_select(self.world_model)
        colorset = [1, 2]
        self._set_menu(options, colorset)

    # def test(self):
    #     logging.warning("ICI")
    #     options = self.menu_model.menu_tournois_select(self.world_model)
    #     self._set_menu(options, colorset)

    def open_tournoi_actions(self):
        options = self.menu_model.menu_tournoi_actions()
        colorset = [1, 2]
        self._set_menu(options, colorset)

    def open_rapports(self):
        options = self.menu_model.menu_rapports()
        colorset = [1, 2]
        self._set_menu(options, colorset)

    def quit(self):
        self.curses_view.say_goodbye()
        curses.napms(1000)
        sys.exit(0)

    def open_new_tournament(self):
        logging.debug("START SET MAIN")
        # self.curses_view.clear_menu()

        fields = Tournament.get_fields_new()
        inputs = {}
        for field in fields:
            logging.debug(f">>>{field} {type(field)}")
            inputs[field["name"]] = self._check_input(
                field["label"],
                field["placeholder"],
                field["test"],
                field["errormsg"],
            )

        self.curses_view.clear_main()
        logging.debug("END SET MAIN")
        # TODO renvoyer vers la page principal du tournoi + menu tournoi

        self.world_model.add_tournament(
            inputs["name"],
            inputs["place"],
            [inputs["start_date"], inputs["end_date"]],
            inputs["rounds"],
            inputs["gtype"],
            inputs["desc"],
        )

    def open_new_actor(self):
        logging.debug("START SET MAIN")
        # self.curses_view.clear_menu()
        self.curses_view.get_input("Nom")
        self.curses_view.get_input("Prénom")
        self.curses_view.get_input("Date de naissance [JJ/MM/AAAA]")
        self.curses_view.clear_main()
        logging.debug("END SET MAIN")

    # Private methods #

    def _align_to_larger(self, options):
        max_size = max([len(option) for option in options])
        return [option.ljust(max_size) for option in options]

    def _get_menu(self, key):
        logging.info("GET MENU")

        current_row, labels, actions, buttons, colorset = self.menu_data

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
                    self.curses_view.main,
                )
            else:
                eval("self." + actions[current_row] + "()")
                return

        self.menu_data[0] = current_row

        self.curses_view.display_menu(buttons, current_row, colorset)

    def _set_menu(self, options, colorset):
        logging.info(f"SET MENU : {options} {colorset}")

        current_row = 0
        labels = [x[0] for x in options]
        actions = [x[1] for x in options]
        buttons = self._align_to_larger(labels)

        self.menu_data = [current_row, labels, actions, buttons, colorset]
        self.curses_view.display_menu(buttons, current_row, colorset)

    def _get_main(self, key):
        self.focus = "menu"
        self.main_data[0]()
        # self.open_menu_base()
        # x = random.randint(0, 100)
        # self.curses_view.print_center(f"Test {x}", self.curses_view.screen)
        pass

    # def _set_main(self, hook, colorset):
    #     self.focus = "main"
    #     self.main_data = [hook, colorset]

    def _check_input(self, label, placeholder=None, test=None, error=None):

        logging.debug(f"_check_input::{test}")

        errormsg = None
        if test is not None:
            test = test.replace("x", "value")
        while 1:
            value = self.curses_view.get_input(label, placeholder, errormsg)
            if test is None or eval(test) is True:
                break
            else:
                errormsg = error

        return value
