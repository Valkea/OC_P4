#! /usr/bin/env python3
# coding: utf-8

""" This module handles the controllers
    of this chess tournament manager
"""

import curses
import sys
import atexit
import re
import logging

from view.main import CurseView
from model.tournament import Tournament, World
from model.menu import Menu

nav_history = []


def saveNav(f):
    def wrapper(*args, **kwargs):
        global nav_history
        nav_history.append([f, args, kwargs])
        return f(*args, **kwargs)

    return wrapper


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

            if key == 9:  # Tilde Key
                self.curses_view.swap_focus()
                # self.list_data, self.list_data_swap = self.list_data_swap, self.list_data

            self._move_selection(key)
            self._input_text(key)

    def _input_text(self, key):
        logging.debug(f"_input_text: {key} --> {chr(key)}")

    # Menu controls #

    @saveNav
    def open_menu_base(self):

        self._set_focus("menu")
        self._set_head_view("print-line", text="Menu général")
        self._set_main_view("clear")
        self._set_menu_view("list", call=self.menu_model.Xbase, colors=[2, 3])

    def debug_tournoi(self):
        return (
            ("Tournoi 1", "open_tournament_initialize"),
            ("Tournoi 2", "open_tournament_initialize"),
            ("Tournoi 3", "open_tournament_initialize"),
        )

    @saveNav
    def open_input_tournament_new(self):

        try:
            self._set_focus("main")
            self._set_head_view("print-line", text="Nouveau tournoi")
            self._set_menu_view("list", call=self.menu_model.Xonly_back)
            # self._set_main_view("list", call=self.debug_tournoi)
            self._set_main_view("print-line", text="Test")

            # self.curses_view.set_focus(self.curses_view.main)
            # inputs = self._set_main_view(
            #     "input-lines", fields=Tournament.get_fields_new()
            # )

            # self.world_model.add_tournament(
            #     inputs["name"],
            #     inputs["place"],
            #     [inputs["start_date"], inputs["end_date"]],
            #     inputs["gtype"],
            #     inputs["desc"],
            #     inputs["rounds"],
            # )
            # self._set_main_view("print-line", text="Tournoi INPUTS")
            # curses.napms(10000)

            # self.open_tournament_initialize()

        except Exception as e:
            logging.debug(f"EXCEPTION: {e}")
            self.goback()

    @saveNav
    def open_select_tournament_load(self):

        # self.world_model.add_tournament(  # TODO remove
        #     "Fake tournament"
        #     "Fake place",
        #     ['01/01/1999', '02/01/1999'],
        #     "Blitz",
        #     "Desc",
        #     "4",
        # )

        # if len(self.world_model.tournaments) == 0:
        #    return self.open_input_tournament_new()

        self._set_focus("main")
        self._set_head_view("print-line", text="Chargement d'un tournoi")
        self._set_menu_view("list", call=self.menu_model.Xonly_back)
        self._set_main_view(
            "list", call=self.menu_model.select_tournament_load, param=self.world_model
        )

    @saveNav
    def open_tournament_initialize(self):

        self._set_focus("menu")
        self._set_head_view("print-line", text="Tournoi [NAME] en phase préparatoire")
        self._set_main_view("print-line", text="Infos tournoi (initialize screen)")
        self._set_menu_view("list", call=self.menu_model.Xtournament_initialize)

    @saveNav
    def open_tournament_opened(self):

        self._set_focus("menu")
        self._set_head_view("print-line", text="Tournoi [NAME] au round X/X")
        self._set_main_view(
            "print-line", text="Infos tournoi + tables du round (opened)"
        )
        self._set_menu_view("list", call=self.menu_model.Xtournament_opened)

    @saveNav
    def open_tournament_finalize(self):

        self._set_focus("menu")
        self._set_head_view(
            "print-line", text="Tournoi [NAME] en phase de finalisation"
        )
        self._set_main_view(
            "print-line", text="Infos tournoi + classement (finialized)"
        )
        self._set_menu_view("list", call=self.menu_model.Xtournament_finalize)

    @saveNav
    def open_tournament_closed(self):

        self._set_focus("menu")
        self._set_head_view("print-line", text="Tournoi clos [NAME]")
        self._set_main_view("print-line", text="Infos tournoi + classement (closed)")
        self._set_menu_view("list", call=self.menu_model.Xtournament_closed)

    @saveNav
    def open_input_actor_new(self):

        self._set_focus("main")
        self._set_head_view("print-line", text="Nouvel acteur")
        self._set_main_view("print-line", text="Inputs d'un nouvel acteur")
        self._set_menu_view("list", call=self.menu_model.Xonly_back)
        curses.napms(3000)
        self.open_tournament_initialize()

    def debug_actors(self):
        return (
            ("Bob 1", "open_input_actor_edit"),
            ("Bob 2", "open_input_actor_edit"),
            ("Bob 3", "open_input_actor_edit"),
        )

    @saveNav
    def open_select_actor(self):

        self._set_focus("main")
        self._set_head_view("print-line", text="Selection d'un acteur à modifier")
        self._set_main_view("list", call=self.debug_actors)
        self._set_menu_view("list", call=self.menu_model.Xactors_alpha)

    def open_menu_actor_order(self, order):
        if order == "elo":
            self._set_menu_view("list", call=self.menu_model.Xactors_alpha)
        else:
            self._set_menu_view("list", call=self.menu_model.Xactors_elo)

    @saveNav
    def open_input_actor_edit(self):

        self._set_focus("main")
        self._set_head_view("print-line", text="Modification d'un acteur")
        self._set_main_view("print-line", text="Modification d'un acteur")
        self._set_menu_view("list", call=self.menu_model.Xonly_back)
        curses.napms(3000)
        self.open_tournament_initialize()

    @saveNav
    def open_reports(self, source):

        self._set_focus("menu")
        self._set_head_view("print-line", text="Rapports")
        self._set_main_view("clear")
        if source == "base":
            self._set_menu_view("list", call=self.menu_model.Xreports_base)
        else:
            self._set_menu_view("list", call=self.menu_model.Xreports_tournament)

    def open_save(self):
        self._set_focus("full")
        # self._set_menu_view("list", call=self.menu_model.Xonly_back)
        self._set_full_view("print-line", text="Sauvegarde du tournoi")
        curses.napms(3000)
        self.goback()

    def goback(self):
        if len(nav_history) > 1:
            nav_history.pop()
            target = nav_history[-1]
            target[0](*target[1], **target[2])

    # --------------------------------------

    def open_menu_baseOld(self):
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
        self._set_menu_view("list", call=self.menu_model.menu_tournoi_select_actions)
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
            inputs["gtype"],
            inputs["desc"],
            inputs["rounds"],
        )

        self.open_tournois_infos()  # TODO passer un id ??

    def open_new_actor(self):
        # # self.curses_view.clear_menu()
        # self.curses_view.get_input("Nom")
        # self.curses_view.get_input("Prénom")
        # self.curses_view.get_input("Date de naissance [JJ/MM/AAAA]")
        # self.curses_view.clear_main()
        self._set_full_view("print-line", text="TODO ACTOR INPUT")  # TODO
        curses.napms(2000)
        self.open_tournoi_actors()

    def open_tournois_infos(self):
        tournaments = self.world_model.tournaments
        infos = tournaments[0].get_overall_infos()  # TODO rendre l'ID dynamique
        self._set_main_view("print-lines", rows=infos.values())
        self._set_menu_view("list", call=self.menu_model.menu_tournoi_base)

    def tmp(self):
        return (("TODO ACTOR", "open_edit_actor"),)

    def open_tournoi_actors(self):
        self._set_main_view("list", call=self.tmp)
        self._set_menu_view("list", call=self.menu_model.menu_tournoi_actor_select)

    def open_edit_actor(self):
        self._set_main_view("print-line", text="TODO ACTOR EDIT")  # TODO
        self._set_menu_view("list", call=self.menu_model.menu_tournoi_actor_manager)

    def open_tournoi_rapport(self):
        self._set_menu_view("list", call=self.menu_model.menu_tournoi_rapports)

    # def open_tournoi_menu_base(self):
    #    self._set_menu_view("list", call=self.menu_model.menu_tournoi_base)

    # Private methods #

    def _align_to_larger(self, options):
        max_size = max([len(option) for option in options])
        return [option.ljust(max_size) for option in options]

    def _move_selection(self, key):

        for screen in self.list_data.keys():
            logging.debug(f"MOVE {screen}")

            sdata = self.list_data[screen]
            # screen = sdata["screen"]
            # screen = self.curses_view.focus

            if screen is not self.curses_view.focus:
                logging.debug(
                    f"MOVE SELECT disable -- : {screen} <--> {self.curses_view.focus}"
                )
                continue

            current_row = sdata["current_row"]
            buttons = sdata["buttons"]
            colors = sdata["colors"]

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
                actions = sdata["actions"]
                params = sdata["params"]

                if actions[current_row] is None:
                    labels = sdata["labels"]
                    self._set_main_view(
                        "print-line",
                        text=f"You selected '{labels[current_row]}'",
                        colors=colors,
                    )
                else:
                    if params[current_row] is None:
                        eval(f"self.{actions[current_row]}")()
                    else:
                        eval(f"self.{actions[current_row]}")(params[current_row])
                    return

            self.list_data[screen]["current_row"] = current_row
            # colorset = self.list_data["colorset"]

            self.curses_view.display_list(screen, buttons, current_row)

    def _check_input(self, screen, label, placeholder=None, test=None, error=None):

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

    def _set_focus(self, focus):
        if focus == "main":
            self.curses_view.focus = self.curses_view.main
        elif focus == "full":
            self.curses_view.focus = self.curses_view.screen
        else:
            self.curses_view.focus = self.curses_view.menu

    def _set_head_view(self, action, **kwargs):
        return self._set_view("head", action, **kwargs)

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
        elif view == "head":
            screen = self.curses_view.head
        else:
            screen = self.curses_view.screen

        if kwargs.get("colors", False):
            colors = kwargs["colors"]
        else:
            colors = [1, 2]

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
            params = [x[2] if len(x) > 2 else None for x in options]
            buttons = self._align_to_larger(labels)

            # self.list_data_swap = self.list_data

            self.list_data[screen] = {
                "screen": screen,
                "current_row": current_row,
                "labels": labels,
                "actions": actions,
                "params": params,
                "buttons": buttons,
                "colors": colors,
            }

            self.curses_view.display_list(screen, buttons, current_row, colors)

        # --- Print one text line into the view ---
        elif action == "print-line":
            self.curses_view.print_center(screen, kwargs.get("text", "Error"), colors)

        # --- Print several text lines into the view ---
        elif action == "print-lines":
            self.curses_view.print_center_multi(
                screen, kwargs.get("rows", ["Error"]), colors
            )

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


class Validation:
    """ D """

    @staticmethod
    def is_valid_date(v):
        """ D """
        try:
            s = re.search(
                "^([0-9]{1,2})[-/. ]([0-9]{1,2})[-/. ]([0-9]{2,4})", v
            ).groups()
            if int(s[0]) > 31 or int(s[1]) > 12 or len(s) != 3:
                return False
            return True
        except AttributeError:
            return False

    @staticmethod
    def is_valid_posint(v):
        """ D """
        try:
            return int(v) > 0
        except ValueError:
            return False

    @staticmethod
    def is_valid_gtype(v):
        """ D """
        v = v.lower()
        if v == "bullet" or v == "blitz" or v == "coups rapides" or v == "coup rapide":
            return True
        return False
