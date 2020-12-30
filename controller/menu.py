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
from model.tournament import Tournament, World
from model.menu import Menu


class Controller:
    """D """

    def __init__(self):
        logging.info("< Open Controller")

        self.curses_view = CurseView()
        self.world_model = World()
        self.menu_model = Menu()
        self.list_data = {}

        atexit.register(self._close)

    def _close(self):
        logging.info("> Close Controller")
        self.curses_view.close()

    # Main controls #

    def start(self):
        while 1:
            key = self.curses_view.screen.getch()
            logging.debug(f"LOOP : key = {key}")

            if key == 9:
                if len(self.list_data_swap) > 0:
                    self.list_data, self.list_data_swap = (
                        self.list_data_swap,
                        self.list_data,
                    )

            self._move_selection(key)

    # Menu controls #

    def open_menu_base(self):
        self._set_menu_view("list", call=self.menu_model.menu_base)
        self._set_main_view("clear")

    def open_tournois(self):
        self._set_menu_view("list", call=self.menu_model.menu_tournois)
        self._set_main_view("clear")

    def open_tournois_select(self):
        self._set_main_view(
            "list", call=self.menu_model.menu_tournois_select, param=self.world_model
        )

    def open_tournoi_actions(self):
        self._set_menu_view("list", call=self.menu_model.menu_tournoi_actions)
        self._set_main_view("clear")

    def open_rapports(self):
        self._set_menu_view("list", call=self.menu_model.menu_rapports)
        self._set_main_view("clear")

    def quit(self):
        self._set_full_view("print-line", text="Closing...")
        curses.napms(500)
        self._set_full_view("print-line", text="Bye!")
        curses.napms(500)
        sys.exit(0)

    def open_new_tournament(self):
        inputs = self._set_full_view("input-lines", fields=Tournament.get_fields_new())

        self.world_model.add_tournament(
            inputs["name"],
            inputs["place"],
            [inputs["start_date"], inputs["end_date"]],
            inputs["rounds"],
            inputs["gtype"],
            inputs["desc"],
        )

        # TODO renvoyer vers la page principal du tournoi + menu tournoi
        # self.open_tournois_select()
        self._set_full_view(
            "list", call=self.menu_model.menu_tournois_select, param=self.world_model
        )

    def open_new_actor(self):
        logging.debug("START SET MAIN")
        # # self.curses_view.clear_menu()
        # self.curses_view.get_input("Nom")
        # self.curses_view.get_input("Prénom")
        # self.curses_view.get_input("Date de naissance [JJ/MM/AAAA]")
        # self.curses_view.clear_main()
        logging.debug("END SET MAIN")

    # Private methods #

    def _align_to_larger(self, options):
        max_size = max([len(option) for option in options])
        return [option.ljust(max_size) for option in options]

    def _move_selection(self, key):

        current_row = self.list_data["current_row"]
        buttons = self.list_data["buttons"]
        screen = self.list_data["screen"]

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
            actions = self.list_data["actions"]

            if actions[current_row] is None:
                labels = self.list_data["labels"]
                self._set_main_view(
                    "print-line", text=f"You selected '{labels[current_row]}'"
                ),
            else:
                eval("self." + actions[current_row] + "()")
                return

        self.list_data["current_row"] = current_row
        # colorset = self.list_data["colorset"]

        self.curses_view.display_list(screen, buttons, current_row)

    def _check_input(self, screen, label, placeholder=None, test=None, error=None):

        logging.debug(f"_check_input::{test}")

        errormsg = None
        if test is not None:
            test = test.replace("x", "value")
        while 1:
            value = self.curses_view.get_input(screen, label, placeholder, errormsg)
            if test is None or eval(test) is True:
                break
            else:
                errormsg = error

        return value

    # --- View direct controls ---

    def _set_menu_view(self, action, **kwargs):
        return self._set_view("menu", action, **kwargs)

    def _set_main_view(self, action, **kwargs):
        return self._set_view("main", action, **kwargs)

    def _set_full_view(self, action, **kwargs):
        return self._set_view("full", action, **kwargs)

    def _set_view(self, view, action, **kwargs):
        """ D """

        if view == "menu":
            screen = self.curses_view.menu
        elif view == "main":
            screen = self.curses_view.main
        else:
            screen = self.curses_view.screen

        # --- Clear the view ---
        if action == "clear":
            self.curses_view.print_center(screen, "")

        # --- Print a menu list into the view ---
        elif action == "list":

            if kwargs.get("param", False):
                options = kwargs["call"](kwargs["param"])
            else:
                options = kwargs["call"]()

            current_row = 0
            labels = [x[0] for x in options]
            actions = [x[1] for x in options]
            buttons = self._align_to_larger(labels)

            self.list_data_swap = self.list_data

            self.list_data = {
                "screen": screen,
                "current_row": 0,
                "labels": labels,
                "actions": actions,
                "buttons": buttons,
                # "colorset": colorset,
            }

            self.curses_view.display_list(screen, buttons, current_row)

        # --- Print one text line into the view ---
        elif action == "print-line":
            self.curses_view.print_center(screen, kwargs.get("text", "Error"))

        # --- Print a sequence of one-line inputs ---
        elif action == "input-lines":

            if screen == "menu":
                return

            inputs = {}
            for field in kwargs["fields"]:
                inputs[field["name"]] = self._check_input(
                    screen,
                    field["label"],
                    field["placeholder"],
                    field["test"],
                    field["errormsg"],
                )
            return inputs
