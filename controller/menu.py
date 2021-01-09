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

from view.tiny import TinyDBView
from view.main import CurseView
from model.world import World
from model.tournament import (
    Tournament,
    IsComplete,
    IsNotReady,
    WrongPlayersNumber,
    Status,
)
from model.player import Player
from model.round import Round
from model.menu import Menu

from utils import FakePlayer


def saveNav(f):
    """ Decorator used to track the navigation history """

    global nav_history
    nav_history = []

    def wrapper(*args, **kwargs):
        global nav_history
        nav_history.append([f, args, kwargs])
        return f(*args, **kwargs)

    return wrapper


class Controller:
    """D """

    def __init__(self):
        logging.info("< Open Controller")

        self.tinyView = TinyDBView()
        self.curses_view = CurseView()
        self.menu_model = Menu()
        self.list_data = {}

        atexit.register(self._close)

    def _close(self):
        logging.info("> Close Controller")
        self.curses_view.close()

    def start(self):
        while 1:
            key = self.curses_view.screen.getch()
            logging.debug(f"LOOP : key = {key}")

            if key == 147:  # TAB
                self.curses_view.swap_focus()
            elif key == curses.KEY_RESIZE:
                logging.warning("RESIZE")  # TODO ?
            elif key == 300:  # CTRL + F12
                self._generate_fake_players()
            elif key == 263:  # BACKSPACE
                self.goback()

            self._move_selection(key)

    # === PUBLIC NAVIGATION METHODS ===

    @saveNav
    def open_menu_base(self):

        World.set_active_tournament(None)
        self._set_focus("menu")
        self._set_head_view("print-line", text="Menu général")
        self._set_main_view("clear")
        self._set_menu_view("list", call=self.menu_model.base, colors=[2, 3])

    @saveNav
    def open_input_tournament_new(self):

        self._set_focus("main")
        self._set_head_view("print-line", text="Nouveau tournoi")
        self._set_menu_view("list", call=self.menu_model.only_back)
        self._set_main_view(
            "form",
            rows=Tournament.get_fields(),
            exit_func=self._form_exit_new_tournament,
        )

    @saveNav
    def open_select_tournament_load(self):

        self._set_focus("main")
        self._set_head_view("print-line", text="Chargement d'un tournoi")
        self._set_menu_view("list", call=self.menu_model.only_back)
        self._set_main_view(
            "list",
            call=self.menu_model.select_tournament_load,
        )

    @saveNav
    def open_input_tournament_edit(self, tournament=None):

        logging.info(f"EDIT tournament: {tournament}")

        if tournament is None:
            tournament = World.get_active_tournament()

        self._set_focus("main")
        self._set_head_view(
            "print-line", text=f"Modification du tournoi <{tournament.name}>"
        )
        self._set_menu_view("list", call=self.menu_model.only_back)
        self._set_main_view(
            "form",
            rows=Tournament.get_fields(),
            exit_func=self._form_exit_edit_tournament,
            source=tournament,
        )

    def open_tournament_current(self, tournament=None):

        if tournament is not None:
            World.set_active_tournament(tournament)

        tournament = World.get_active_tournament()

        if (
            tournament.status == Status.UNINITIALIZED
            or tournament.status == Status.INITIALIZED
        ):
            self.open_tournament_initialize(tournament)
        elif tournament.status == Status.PLAYING:
            self.open_tournament_opened(tournament)
        elif tournament.status == Status.CLOSING:
            self.open_tournament_finalize(tournament)
        elif tournament.status == Status.CLOSED:
            self.open_tournament_closed(tournament)

    @saveNav
    def open_tournament_initialize(self, tournament=None):

        if tournament is None:
            tournament = World.get_active_tournament()

        tournament.status = Status.INITIALIZED

        self._set_focus("menu")
        self._set_head_view(
            "print-line", text=f"Tournoi <{tournament.name}> en phase préparatoire"
        )
        self._set_main_view("print-lines", rows=tournament.get_overall_infos().values())
        self._set_menu_view("list", call=self.menu_model.tournament_initialize)

    def start_new_round(self, tournament=None):

        if tournament is None:
            tournament = World.get_active_tournament()

        try:
            logging.info("START_NEW_ROUND try")
            tournament.start_round()
            self.open_tournament_opened(tournament)

        except WrongPlayersNumber as e:
            self.curses_view.display_error(str(e))
            curses.napms(3000)
            self.curses_view.display_error("")
        except IsNotReady as e:
            logging.critical(
                "Calling start_new_round on an uninitialized or closed tournament"
            )
            raise e
        except IsComplete:
            self.open_tournament_finalize(tournament)

    def input_round_results(self, tournament=None):

        logging.info(f"EDIT final note: {tournament}")

        if tournament is None:
            tournament = World.get_active_tournament()

        self._set_focus("main")
        self._set_head_view(
            "print-line",
            text=f"Saisies de resultats pour <{tournament.current_round().name}>",
        )
        self._set_menu_view("list", call=self.menu_model.only_back)
        self._set_main_view(
            "form",
            rows=tournament.get_fields_input_scores(),
            exit_func=self._form_exit_input_scores,
        )

    def input_final_note(self, tournament=None):

        logging.info(f"EDIT final note: {tournament}")

        if tournament is None:
            tournament = World.get_active_tournament()

        self._set_focus("main")
        self._set_head_view(
            "print-line",
            text=f"Saisie de la note finale du tournoi <{tournament.name}>",
        )
        self._set_menu_view("list", call=self.menu_model.only_back)
        self._set_main_view(
            "form",
            rows=Tournament.get_fields_final_note(),
            exit_func=self._form_exit_edit_final_note,
            source=tournament,
        )

    @saveNav
    def open_tournament_opened(self, tournament=None):

        if tournament is None:
            tournament = World.get_active_tournament()

        tournament.status = Status.PLAYING

        self._set_focus("menu")
        self._set_head_view(
            "print-line",
            text=f"Tournoi <{tournament.name}> : <{tournament.current_round().name}>",
        )
        self._set_main_view("print-lines", rows=tournament.get_overall_infos().values())
        self._set_menu_view("list", call=self.menu_model.tournament_opened)

    @saveNav
    def open_tournament_finalize(self, tournament=None):

        if tournament is None:
            tournament = World.get_active_tournament()

        tournament.status = Status.CLOSING

        self._set_focus("menu")
        self._set_head_view(
            "print-line", text=f"Tournoi <{tournament.name}> en phase finale"
        )
        self._set_main_view("print-lines", rows=tournament.get_overall_infos().values())
        self._set_menu_view("list", call=self.menu_model.tournament_finalize)

    @saveNav
    def open_tournament_closed(self, tournament=None):

        if tournament is None:
            tournament = World.get_active_tournament()

        tournament.status = Status.CLOSED

        self._set_focus("menu")
        self._set_head_view("print-line", text=f"Tournoi <{tournament.name}> clos")
        self._set_main_view("print-lines", rows=tournament.get_overall_infos().values())
        self._set_menu_view("list", call=self.menu_model.tournament_closed)

    @saveNav
    def open_input_actor_new(self):

        self._set_focus("main")
        self._set_head_view("print-line", text="Nouvel acteur")
        self._set_menu_view("list", call=self.menu_model.only_back)
        self._set_main_view(
            "form",
            rows=Player.get_fields(),
            exit_func=self._form_exit_new_actor,
        )

    @saveNav
    def open_select_actor(self, sortby=None):

        self._set_focus("main")
        self._set_head_view("print-line", text="Selection d'un acteur à modifier")
        self._set_menu_view("list", call=self.menu_model.actors_sortby)
        self._set_main_view(
            "list",
            call=self.menu_model.select_actor,
            call_params={"sortby": sortby},
        )

    def open_menu_actor_sortby(self, sortby):

        target = nav_history[-1]
        target[2]["sortby"] = sortby
        target[0](*target[1], **target[2])
        self._set_menu_view(
            "list", call=self.menu_model.actors_sortby, call_params={"sortby": sortby}
        )

        logging.debug(f"TRI: {target}")

    @saveNav
    def open_input_actor_edit(self, actor):

        logging.info(f"EDIT actor: {actor}")

        self._set_focus("main")
        self._set_head_view(
            "print-line", text=f"Modification de l'acteur <{actor.getFullname()}>"
        )
        self._set_menu_view("list", call=self.menu_model.only_back)
        self._set_main_view(
            "form",
            rows=Player.get_fields(),
            exit_func=self._form_exit_edit_actor,
            source=actor,
        )

    @saveNav
    def open_reports(self, source):

        self._set_focus("menu")
        self._set_head_view("print-line", text="Rapports")
        self._set_main_view("clear")
        if source == "base":
            self._set_menu_view("list", call=self.menu_model.reports_base)
        else:
            self._set_menu_view("list", call=self.menu_model.reports_tournament)

    @saveNav
    def open_report_all_actors(self, sortby=None):
        self._set_focus("menu")
        self._set_head_view("print-line", text="Liste de l'ensemble des acteurs")
        self._set_menu_view("list", call=self.menu_model.actors_sortby)
        self._set_main_view(
            "list",
            call=self.menu_model.list_all_actors,
            call_params={"sortby": sortby},
            autostart=False,
        )

    @saveNav
    def open_report_all_tournament(self):
        self._set_focus("menu")
        self._set_head_view("print-line", text="Chargement d'un tournoi")
        self._set_menu_view("list", call=self.menu_model.only_back)
        self._set_main_view(
            "list",
            call=self.menu_model.select_tournament_load,
            active_links=False,
            autostart=False,
        )

    @saveNav
    def open_select_tournament_report(self, route):

        self._set_focus("main")
        self._set_head_view("print-line", text="Selection d'un tournoi")
        self._set_menu_view("list", call=self.menu_model.only_back)
        self._set_main_view(
            "list",
            call=self.menu_model.select_tournament_report,
            call_params={"route": route},
        )

    @saveNav
    def open_report_tournament_actors(self, tournament=None, sortby=None):

        if tournament is None:
            tournament = World.get_active_tournament()

        self._set_focus("menu")
        self._set_head_view(
            "print-line",
            text=f"Liste de l'ensemble des acteurs du tournoi <{tournament.name}>",
        )
        self._set_menu_view("list", call=self.menu_model.actors_sortby)
        self._set_main_view(
            "list",
            call=self.menu_model.list_actors,
            call_params={"tournament": tournament, "sortby": sortby},
            autostart=False,
        )

    @saveNav
    def open_report_tournament_rounds(self, tournament=None):

        if tournament is None:
            tournament = World.get_active_tournament()

        self._set_focus("menu")
        self._set_head_view(
            "print-line",
            text=f"Liste des rounds du tournoi <{tournament.name}>",
        )
        self._set_menu_view("list", call=self.menu_model.only_back)
        self._set_main_view(
            "list",
            call=self.menu_model.list_rounds,
            call_params={"tournament": tournament},
            autostart=False,
        )

    @saveNav
    def open_report_tournament_matchs(self, tournament=None):

        if tournament is None:
            tournament = World.get_active_tournament()

        self._set_focus("menu")
        self._set_head_view(
            "print-line",
            text=f"Liste des matchs du tournoi <{tournament.name}>",
        )
        self._set_menu_view("list", call=self.menu_model.only_back)
        self._set_main_view(
            "list",
            call=self.menu_model.list_games,
            call_params={"tournament": tournament},
            autostart=False,
        )

    def open_save(self):
        self._set_focus("menu")

        self.curses_view.display_error("Sauvegarde ...")
        self.tinyView.save_all()

        logging.info("SAVED")
        curses.napms(500)

        self.curses_view.display_error("")
        self.goback()

    def open_load(self):
        self._set_focus("menu")

        self.curses_view.display_error("Chargement ...")
        World.load(*self.tinyView.load_all())

        logging.info("LOADED")
        curses.napms(500)

        self.curses_view.display_error("")
        self.goback()

    @saveNav
    def open_load_save(self):
        self._set_menu_view("list", call=self.menu_model.iofile)

    def goback(self):
        if len(nav_history) > 1:
            nav_history.pop()
            target = nav_history[-1]
            target[0](*target[1], **target[2])

    def quit(self):
        self._set_full_view("print-line", text="Closing...")
        curses.napms(500)
        self._set_full_view("print-line", text="Bye!")
        curses.napms(500)
        sys.exit(0)

    # --- DEMO methods ---

    def _generate_fake_players(self):

        if World.get_active_tournament() is None:
            logging.warning("GEN FAKE USERS: need an active tournament")
            return

        num_players = 2
        fakeInputs = FakePlayer()
        fakePlayers = fakeInputs.gen(num_players)

        for p in fakePlayers:

            family_name = p["familyname"]
            first_name = p["firstname"]
            birthdate = p["birthdate"]
            sex = p["sex"]
            elo = p["elo"]

            player = Player(family_name, first_name, birthdate, sex, elo)
            World.add_actor(player)

        self.open_tournament_initialize()
        # self.open_select_actor()

    # === PRIVATE METHODS ===

    def _align_to_larger(self, options):
        max_size = max([len(option) for option in options])
        return [option.ljust(max_size) for option in options]

    def _move_selection(self, key):

        for screen in self.list_data.keys():

            sdata = self.list_data[screen]
            # screen = sdata["screen"]
            # screen = self.curses_view.focus

            if screen is not self.curses_view.focus:
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
                active_links = sdata["active_links"]

                if active_links is False:
                    return

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

    # === View controls ===

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

            if kwargs.get("call_params", False):
                options = kwargs["call"](**kwargs["call_params"])
            else:
                options = kwargs["call"]()

            if kwargs.get("autostart") is not False:
                current_row = 0
            else:
                current_row = -1

            if kwargs.get("active_links") is not False:
                active_links = True
            else:
                active_links = False

            labels = [x[0] for x in options]
            actions = [x[1] for x in options]
            params = [x[2] if len(x) > 2 else None for x in options]
            buttons = self._align_to_larger(labels)

            self.list_data[screen] = {
                "screen": screen,
                "current_row": current_row,
                "labels": labels,
                "actions": actions,
                "params": params,
                "buttons": buttons,
                "colors": colors,
                "active_links": active_links,
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

        # --- Print several inputs as a form ---
        elif action == "form":

            if screen == "menu":
                return

            self._form_setup(
                screen,
                kwargs.get("rows"),
                kwargs.get("exit_func"),
                kwargs.get("source"),
            )

    #        # --- Print a sequence of one-line inputs ---
    #        elif action == "input-lines":
    #
    #            if screen == "menu":
    #                return
    #
    #            inputs = {}
    #            for field in kwargs["fields"]:
    #                inputs[field["name"]] = self._check_input(
    #                    screen,
    #                    field["label"],
    #                    field["placeholder"],
    #                    field["test"],
    #                    field["errormsg"],
    #                )
    #            return inputs

    # === Form controls ===

    def _form_setup(self, screen, rows, exit_func, source=None):
        text_boxes, text_wins, error_box = self.curses_view.init_form(
            screen, rows, source
        )

        def swapfield(x):
            self._form_input_swap(
                x, rows, text_boxes, text_wins, error_box, swapfield, exit_func, source
            )
            return x

        try:
            j = 0
            text_boxes[j].edit(swapfield)

        except UnstackAll as e:
            if str(e) == "SUBMIT":
                self.curses_view.close_form(screen)
            elif str(e) == "TAB":
                return

    def _form_input_swap(
        self,
        x,
        rows,
        text_boxes,
        text_wins,
        error_box,
        swap_func,
        exit_func,
        source,
        j_save=[0],
    ):

        logging.debug(f"FORM INPUT SWAP {x}")

        swap_rows = [(x, i) for i, x in enumerate(rows) if x.get("name", False)]

        j = j_save[0]

        if x == 9 or x == 10:
            test = self._form_test(
                text_boxes[j].gather().strip(),
                swap_rows[j][0]["test"],
                swap_rows[j][0]["errormsg"],
                error_box,
            )

            if test is True:
                if j < len(swap_rows) - 1:

                    j += 1
                    j_save[0] = j

                    self.curses_view.set_input_focus(
                        text_wins[j], text_boxes[j], swap_func
                    )
                    return

                elif j == len(swap_rows) - 1:

                    j = 0
                    j_save[0] = j

                    self._form_gather_inputs(text_boxes, rows, exit_func, source)
            else:
                self.curses_view.set_input_focus(text_wins[j], text_boxes[j], swap_func)

        elif x == 353:
            if j > 0:
                j -= 1
                j_save[0] = j
                error_box.clear()
                error_box.refresh()
                self.curses_view.set_input_focus(text_wins[j], text_boxes[j], swap_func)
                return

        elif x == 147:
            raise UnstackAll("TAB")

        return x

    def _form_test(self, value, test, errormsg, error_win):

        if test is None or eval(test) is True:
            logging.debug(f"TEST {test} OK")
            error_win.clear()
            error_win.refresh()
            return True
        else:
            logging.debug(f"TEST {test} ERROR")
            error_win.clear()
            error_win.addstr(errormsg)
            error_win.refresh()

    def _form_gather_inputs(self, text_boxes, rows, exit_func, source):

        inputs = {}
        valid_rows = [x for x in rows if x.get("name", False)]

        for row, tb in zip(valid_rows, text_boxes):
            if row.get("name", False):
                inputs[row["name"]] = tb.gather().strip()

        exit_func(inputs, source)

        raise UnstackAll("SUBMIT")

    def _form_exit_new_tournament(self, inputs, source):

        logging.info(f"NEW TOURNAMENT VALUES: {inputs}")
        tournament = World.add_tournament(
            inputs["name"],
            inputs["place"],
            inputs["start_date"],
            inputs["end_date"],
            inputs["game_type"],
            inputs["description"],
            inputs["num_rounds"],
        )
        World.set_active_tournament(tournament)
        self.open_tournament_initialize()

    def _form_exit_edit_tournament(self, inputs, source):

        logging.info(f"EDIT TOURNAMENT VALUES: {inputs}")
        source.name = inputs["name"]
        source.place = inputs["place"]
        source.start_date = inputs["start_date"]
        source.end_date = inputs["end_date"]
        source.game_type = inputs["game_type"]
        source.description = inputs["description"]
        source.num_rounds = int(inputs["num_rounds"])

        # self.goback()
        self.open_tournament_initialize()

    def _form_exit_new_actor(self, inputs, source):

        logging.info(f"NEW ACTOR VALUES: {inputs}")
        tournament = World.get_active_tournament()
        actor = Player(
            inputs["family_name"],
            inputs["first_name"],
            inputs["birthdate"],
            inputs["sex"],
            inputs["elo"],
        )

        World.add_actor(actor, tournament)
        self.open_tournament_initialize()

    def _form_exit_edit_actor(self, inputs, source):

        logging.info(f"EDIT ACTOR VALUES: {inputs}")
        source.family_name = inputs["family_name"]
        source.first_name = inputs["first_name"]
        source.birthdate = inputs["birthdate"]
        source.sex = inputs["sex"]
        source.elo = inputs["elo"]

        self.goback()

    def _form_exit_edit_final_note(self, inputs, source):

        logging.info(f"EDIT FINAL NOTE: {inputs}")
        source.description = inputs["description"]

        self.open_tournament_closed()

    def _form_exit_input_scores(self, inputs, source):
        logging.info(f"INPUT SCORES: {inputs}")

        tournament = World.get_active_tournament()

        for i, k in enumerate(inputs):
            logging.info(f"--->{inputs[k]}")
            tournament.set_results(i, *Round.getScores(inputs[k]))

        self.start_new_round()


class UnstackAll(Exception):
    """Exception used to exit nested curses edit calls.

    There must be a better way to do that, but that's my best call at the moment..
    """

    pass


class Validation:
    """ D """

    @staticmethod
    def is_valid_date(v):
        """ D """
        try:
            s = re.search(
                "^([0-9]{1,2})[-/. ]([0-9]{1,2})[-/. ]([0-9]{2,4})$", v
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

    @staticmethod
    def is_valid_sex(v):
        """ D """
        v = v.lower()[0:1]
        if v == "h" or v == "f":
            return True
        return False

    @staticmethod
    def is_valid_score_symbol(v):
        """ D """
        logging.info(f"is_valid_score_symbol: {v}")
        if v == "<" or v == ">" or v == "=":
            return True
        return False
