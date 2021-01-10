#! /usr/bin/env python3
# coding: utf-8

""" This module handles the controllers
    of this chess tournament manager
"""

import curses
import sys
import atexit
import logging

from controller.validation import Validation

from view.tiny import TinyDbView
from view.curses import CurseView

from model.player import Player
from model.round import Round
from model.menu import Menu
from model.world import World
from model.tournament import (
    Tournament,
    IsComplete,
    IsNotReady,
    WrongPlayersNumber,
    Status,
)

from utils import FakePlayer


def saveNav(f):
    """ Decorator used to track the navigation history. """

    global nav_history
    nav_history = []

    def wrapper(*args, **kwargs):
        global nav_history
        nav_history.append([f, args, kwargs])
        return f(*args, **kwargs)

    return wrapper


def resetNav(f):
    """ Decorator used to clear the navigation history. """

    def wrapper(*args, **kwargs):
        global nav_history
        nav_history = []
        nav_history.append([f, args, kwargs])
        return f(*args, **kwargs)

    return wrapper


class Controller:
    """ This Class offers various methods to control the overall app.

        By using this controller, you can collect data from models,
        display them with views  (CurseView & TinyDbView) and
        control the overall tournament process.

    Attributes
    ----------
    curses_view : CurseView
        one instance of the CurseView Class, so we can draw stuffs coming from controlers


    Public Methods
    --------------

    start()
        Start the 'infinite' loop than runs the app
    close()
        Clean-up at exit
    start_new_round(tournament=None)
        Start a new round in the active tournament

    open_menu_base()
        Open the root page with the main menu

    open_input_tournament_new()
        Open the page used to input a new tournament
    open_input_tournament_edit(tournament=None)
        Open the page used to edit an existing tournament
    open_select_tournament_load()
        Open the page that offers to select an existing tournament then load it

    open_tournament_current(tournament=None)
        Call the appropriate opening method depending on the tournament current Status
    open_tournament_initialize(tournament=None)
        Open the tournament page that corresponds to the Status.INITIALIZED status
    open_input_round_results(tournament=None)
        Open the page for the round results inputs
    open_input_final_note(tournament=None)
        Open the page for the final note input
    open_tournament_opened(tournament=None)
        Open the tournament page that corresponds to the Status.PLAYING status
    open_tournament_finalize(tournament=None)
        Open the tournament page that corresponds to the Status.CLOSING status
    open_tournament_closed(tournament=None)
        Open the tournament page that corresponds to the Status.CLOSED status

    open_input_actor_new()
        Open the page used to input a new actor
    open_input_actor_edit(actor)
        Open the page used to edit an existing actor
    open_select_actor(sortby=None)
        Open the page used to select an actor (for editing it)
    open_menu_actor_sortby(sortby)
        Open the menu used to sort the user-lists

    open_reports(source)
        Open the base menu used to acces the various reports from the root menu
    open_report_all_actors(sortby=None)
        Open the page displaying all the actors of all the tournaments
    open_report_all_tournament()
        Open the page displaying all the existing tournaments
    open_select_tournament_report(route)
        Open the page that offers to select an existing tournament then dislay the corresponding report
    open_report_tournament_actors(tournament=None, sortby=None)
        Open the page displaying the actors of the selected tournament (or current one)
    open_report_tournament_rounds(tournament=None)
        Open the page displaying the rounds of the selected tournament (or current one)
    open_report_tournament_matchs(tournament=None)
        Open the page displaying the games (matchs) of the selected tournament (or current one)

    open_save()
        Save the content of the app and display a message
    open_load()
        Load the content of the app and display a message
    open_load_save()
        Open the menu offering to load or save data

    open_quit_menu()
        Open the menu offering to quit with or without saving data
    quit()
        Display an exit message and close the application
    save_n_quit()
        Save the data and display a message, then call quit()

    go_back()
        Open the last page (minus the current one) registerd with the @saveNav decorator

    Private Methods
    ---------------

    _generate_fake_players()
        Demo method used to quickly generate fake players (bind to CTRL+F12)
    _align_to_larger(options)
        Align the size of the provided list to the size of the larger item (filling with space)
    _move_selection(key)
        Control the mouvement of the selection when displaying a menu or a  list of selectable items

    _set_focus(focus)
        Control the CurseView focus
    _set_head_view(action, **kwargs)
        _set_view shortcut to control the content of the head window of the CurseView
    _set_menu_view(action, **kwargs)
        _set_view shortcut to control the content of the menu window of the CurseView
    _set_main_view(action, **kwargs)
        _set_view shortcut to control the content of the main window of the CurseView
    _set_full_view(action, **kwargs)
        _set_view shortcut to control the content of the base window (full screen) of the CurseView
    _set_view(view, action, **kwargs)
        Control the content of the given window of the CurseView

    _form_setup(screen, rows, exit_func, source=None)
        Initialize a new form
    _form_input_swap(x, rows, text_boxes, text_wins, error_box, swap_func, exit_func, source)
        Control the form navigation (TAB & SHIFT + TAB)
    _form_test(value, test, errormsg, error_win)
        Control the form tests
    _form_gather_inputs(text_boxes, rows, exit_func, source)
        Gather form inputs and transmit to callback functions

    _form_exit_new_tournament(inputs, source)
        Process the new tournament informations and transmit to the model
    _form_exit_edit_tournament(inputs, source)
        Process the tournament modified informations and transmit to the model
    _form_exit_new_actor(inputs, source)
        Process the new actor informations and transmit to the model
    _form_exit_edit_actor(inputs, source)
        Process the actor modified informations and transmit to the model
    _form_exit_edit_final_note(inputs, source)
        Process the final note input and transmit to the model
    _form_exit_input_scores(inputs, source)
        Process the round score inputs and transmit to the model

    """

    def __init__(self):
        logging.info("< Open Controller")

        self.curses_view = CurseView()
        self._list_data = {}

        atexit.register(self.close)

    # === PUBLIC METHODS ===

    def start(self):
        """ Start the 'infinite' loop than runs the app. """

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
                self.go_back()

            self._move_selection(key)

    def close(self):
        """ Clean-up at exit. """

        logging.info("> Close Controller")
        self.curses_view.close()

    def start_new_round(self, tournament=None):
        """ Start a new round in the active tournament.

        Parameters
        ----------
        tournament : Tournament
            The optional tournament instance to target.
            Will use the current open tournament otherwise.
        """

        if tournament is None:
            tournament = World.get_active_tournament()

        try:
            logging.info("START_NEW_ROUND")
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

    # === PUBLIC NAVIGATION METHODS ===

    @resetNav
    def open_menu_base(self):
        """ Open the root page with the main menu. """

        World.set_active_tournament(None)
        self._set_focus("menu")
        self._set_head_view("print-line", text="Menu général")
        self._set_main_view("clear")
        self._set_menu_view("list", call=Menu.base, colors=[2, 3])

    # --- Tournament pages ---

    @saveNav
    def open_input_tournament_new(self):
        """ Open the page used to input a new tournament. """

        self._set_focus("main")
        self._set_head_view("print-line", text="Nouveau tournoi")
        self._set_menu_view("list", call=Menu.only_back)
        self._set_main_view(
            "form",
            rows=Tournament.get_fields(),
            exit_func=self._form_exit_new_tournament,
        )

    @saveNav
    def open_input_tournament_edit(self, tournament=None):
        """ Open the page used to edit an existing tournament.

        Parameters
        ----------
        tournament : Tournament
            The optional tournament instance to target.
            Will use the current open tournament otherwise.
        """

        logging.info(f"EDIT tournament: {tournament}")

        if tournament is None:
            tournament = World.get_active_tournament()

        self._set_focus("main")
        self._set_head_view(
            "print-line", text=f"Modification du tournoi <{tournament.name}>"
        )
        self._set_menu_view("list", call=Menu.only_back)
        self._set_main_view(
            "form",
            rows=Tournament.get_fields(),
            exit_func=self._form_exit_edit_tournament,
            source=tournament,
        )

    @saveNav
    def open_select_tournament_load(self):
        """ Open the page that offers to select an existing tournament then load it. """

        self._set_focus("main")
        self._set_head_view("print-line", text="Chargement d'un tournoi")
        self._set_menu_view("list", call=Menu.only_back)
        self._set_main_view(
            "list",
            call=Tournament.select_tournament_load,
            call_params={"world": World},
        )

    def open_tournament_current(self, tournament=None):
        """ Call the appropriate opening method depending on the tournament current Status.

        Parameters
        ----------
        tournament : Tournament
            The optional tournament instance to target.
            Will use the current open tournament otherwise.
        """

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

    @resetNav
    def open_tournament_initialize(self, tournament=None):
        """ Open the tournament page that corresponds to the Status.INITIALIZED status.

        Parameters
        ----------
        tournament : Tournament
            The optional tournament instance to target.
            Will use the current open tournament otherwise.
        """

        if tournament is None:
            tournament = World.get_active_tournament()

        tournament.status = Status.INITIALIZED

        self._set_focus("menu")
        self._set_head_view(
            "print-line", text=f"Tournoi <{tournament.name}> en phase préparatoire"
        )
        self._set_main_view("print-lines", rows=tournament.get_overall_infos().values())
        self._set_menu_view("list", call=Menu.tournament_initialize)

    @saveNav
    def open_input_round_results(self, tournament=None):
        """ Open the page for the round results inputs.

        Parameters
        ----------
        tournament : Tournament
            The optional tournament instance to target.
            Will use the current open tournament otherwise.
        """

        logging.info(f"EDIT final note: {tournament}")

        if tournament is None:
            tournament = World.get_active_tournament()

        self._set_focus("main")
        self._set_head_view(
            "print-line",
            text=f"Saisies de resultats pour <{tournament.current_round().name}>",
        )
        self._set_menu_view("list", call=Menu.only_back)
        self._set_main_view(
            "form",
            rows=tournament.get_fields_input_scores(),
            exit_func=self._form_exit_input_scores,
        )

    @saveNav
    def open_input_final_note(self, tournament=None):
        """ Open the page for the final note input.

        Parameters
        ----------
        tournament : Tournament
            The optional tournament instance to target.
            Will use the current open tournament otherwise.
        """

        logging.info(f"EDIT final note: {tournament}")

        if tournament is None:
            tournament = World.get_active_tournament()

        self._set_focus("main")
        self._set_head_view(
            "print-line",
            text=f"Saisie de la note finale du tournoi <{tournament.name}>",
        )
        self._set_menu_view("list", call=Menu.only_back)
        self._set_main_view(
            "form",
            rows=Tournament.get_fields_final_note(),
            exit_func=self._form_exit_edit_final_note,
            source=tournament,
        )

    @resetNav
    def open_tournament_opened(self, tournament=None):
        """ Open the tournament page that corresponds to the Status.PLAYING status.

        Parameters
        ----------
        tournament : Tournament
            The optional tournament instance to target.
            Will use the current open tournament otherwise.
        """

        if tournament is None:
            tournament = World.get_active_tournament()

        tournament.status = Status.PLAYING

        self._set_focus("menu")
        self._set_head_view(
            "print-line",
            text=f"Tournoi <{tournament.name}> : <{tournament.current_round().name}>",
        )
        self._set_main_view("print-lines", rows=tournament.get_overall_infos().values())
        self._set_menu_view("list", call=Menu.tournament_opened)

    @resetNav
    def open_tournament_finalize(self, tournament=None):
        """ Open the tournament page that corresponds to the Status.CLOSING status.

        Parameters
        ----------
        tournament : Tournament
            The optional tournament instance to target.
            Will use the current open tournament otherwise.
        """

        if tournament is None:
            tournament = World.get_active_tournament()

        tournament.status = Status.CLOSING

        self._set_focus("menu")
        self._set_head_view(
            "print-line", text=f"Tournoi <{tournament.name}> en phase finale"
        )
        self._set_main_view("print-lines", rows=tournament.get_overall_infos().values())
        self._set_menu_view("list", call=Menu.tournament_finalize)

    @resetNav
    def open_tournament_closed(self, tournament=None):
        """ Open the tournament page that corresponds to the Status.CLOSED status.

        Parameters
        ----------
        tournament : Tournament
            The optional tournament instance to target.
            Will use the current open tournament otherwise.
        """

        if tournament is None:
            tournament = World.get_active_tournament()

        tournament.status = Status.CLOSED

        self._set_focus("menu")
        self._set_head_view("print-line", text=f"Tournoi <{tournament.name}> clos")
        self._set_main_view("print-lines", rows=tournament.get_overall_infos().values())
        self._set_menu_view("list", call=Menu.tournament_closed)

    # --- Actor' pages ---

    @saveNav
    def open_input_actor_new(self):
        """ Open the page used to input a new actor. """

        self._set_focus("main")
        self._set_head_view("print-line", text="Nouvel acteur")
        self._set_menu_view("list", call=Menu.only_back)
        self._set_main_view(
            "form",
            rows=Player.get_fields(),
            exit_func=self._form_exit_new_actor,
        )

    @saveNav
    def open_input_actor_edit(self, actor):
        """ Open the page used to edit an existing actor.

        Parameters
        ----------
        actor : Player
            The Player instance to modifiy
        """

        logging.info(f"EDIT actor: {actor}")

        self._set_focus("main")
        self._set_head_view(
            "print-line", text=f"Modification de l'acteur <{actor.get_fullname()}>"
        )
        self._set_menu_view("list", call=Menu.only_back)
        self._set_main_view(
            "form",
            rows=Player.get_fields(),
            exit_func=self._form_exit_edit_actor,
            source=actor,
        )

    @saveNav
    def open_select_actor(self, sortby=None):
        """ Open the page used to select an actor (for editing it).

        Parameters
        ----------
        sortby : str
            The optional sorting sequence name to apply on the result.
        """

        self._set_focus("main")
        self._set_head_view("print-line", text="Selection d'un acteur à modifier")
        self._set_menu_view("list", call=Menu.actors_sortby)
        self._set_main_view(
            "list",
            call=Player.select_actor,
            call_params={"sortby": sortby, "world": World},
        )

    def open_menu_actor_sortby(self, sortby):
        """ Open the menu used to sort the user-lists.

        Parameters
        ----------
        sortby : str
            The sorting sequence name  used to know which version of the menu must be opened
        """

        target = nav_history[-1]
        target[2]["sortby"] = sortby
        target[0](*target[1], **target[2])
        self._set_menu_view(
            "list", call=Menu.actors_sortby, call_params={"sortby": sortby}
        )

    # --- Report' pages---

    @saveNav
    def open_reports(self, source):
        """ Open the base menu used to acces the various reports from the root menu.

        Parameters
        ----------
        source : str
            Indicate the source menu (base or tournament) in order to adapt the content
        """

        self._set_focus("menu")
        self._set_head_view("print-line", text="Rapports")
        self._set_main_view("clear")
        if source == "base":
            self._set_menu_view("list", call=Menu.reports_base)
        else:
            self._set_menu_view("list", call=Menu.reports_tournament)

    @saveNav
    def open_report_all_actors(self, sortby=None):
        """ Open the page displaying all the actors of all the tournaments.

        Parameters
        ----------
        sortby : str
            The optional sorting sequence name to apply on the result.
        """
        self._set_focus("menu")
        self._set_head_view("print-line", text="Liste de l'ensemble des acteurs")
        self._set_menu_view("list", call=Menu.actors_sortby)
        self._set_main_view(
            "list",
            call=Player.list_all_actors,
            call_params={"sortby": sortby, "world": World},
            autostart=False,
        )

    @saveNav
    def open_report_all_tournament(self):
        """ Open the page displaying all the existing tournaments. """

        self._set_focus("menu")
        self._set_head_view("print-line", text="Chargement d'un tournoi")
        self._set_menu_view("list", call=Menu.only_back)
        self._set_main_view(
            "list",
            call=Tournament.select_tournament_load,
            call_params={"world": World},
            active_links=False,
            autostart=False,
        )

    @saveNav
    def open_select_tournament_report(self, route):
        """ Open the page that offers to select an existing
            tournament then dislay the corresponding report.

        Parameters
        ----------
        route : str
            The name of the function to call once the tournament is selected
        """

        self._set_focus("main")
        self._set_head_view("print-line", text="Selection d'un tournoi")
        self._set_menu_view("list", call=Menu.only_back)
        self._set_main_view(
            "list",
            call=Tournament.select_tournament_report,
            call_params={"route": route, "world": World},
        )

    @saveNav
    def open_report_tournament_actors(self, tournament=None, sortby=None):
        """ Open the page displaying the actors of
            the selected tournament (or current one).

        Parameters
        ----------
        tournament : Tournament
            The optional tournament instance to target.
            Use the current open tournament otherwise.
        sortby : str
            The optional sorting sequence name to apply on the result.
        """

        if tournament is None:
            tournament = World.get_active_tournament()

        self._set_focus("menu")
        self._set_head_view(
            "print-line",
            text=f"Liste de l'ensemble des acteurs du tournoi <{tournament.name}>",
        )
        self._set_menu_view("list", call=Menu.actors_sortby)
        self._set_main_view(
            "list",
            call=Player.list_actors,
            call_params={"tournament": tournament, "world": World, "sortby": sortby},
            autostart=False,
        )

    @saveNav
    def open_report_tournament_rounds(self, tournament=None):
        """ Open the page displaying the rounds of
            the selected tournament (or current one).

        Parameters
        ----------
        tournament : Tournament
            The optional tournament instance to target.
            Use the current open tournament otherwise.
        """

        if tournament is None:
            tournament = World.get_active_tournament()

        self._set_focus("menu")
        self._set_head_view(
            "print-line",
            text=f"Liste des rounds du tournoi <{tournament.name}>",
        )
        self._set_menu_view("list", call=Menu.only_back)
        self._set_main_view(
            "list",
            call=Round.list_rounds,
            call_params={"tournament": tournament},
            autostart=False,
        )

    @saveNav
    def open_report_tournament_matchs(self, tournament=None):
        """ Open the page displaying the games (matchs) of
            the selected tournament (or current one).

        Parameters
        ----------
        tournament : Tournament
            The optional tournament instance to target.
            Use the current open tournament otherwise.
        """

        if tournament is None:
            tournament = World.get_active_tournament()

        self._set_focus("menu")
        self._set_head_view(
            "print-line",
            text=f"Liste des matchs du tournoi <{tournament.name}>",
        )
        self._set_menu_view("list", call=Menu.only_back)
        self._set_main_view(
            "list",
            call=Round.list_games,
            call_params={"tournament": tournament, "world": World},
            autostart=False,
        )

    # --- Save & Load pages ---

    def open_save(self):
        """ Save the content of the app and display a message. """

        self._set_focus("menu")

        self.curses_view.display_error("Sauvegarde ...")
        TinyDbView.save_all()

        logging.info("SAVED")
        curses.napms(500)

        self.curses_view.display_error("")
        self.go_back()

    def open_load(self):
        """ Load the content of the app and display a message. """

        self._set_focus("menu")

        self.curses_view.display_error("Chargement ...")
        World.load(*TinyDbView.load_all())

        logging.info("LOADED")
        curses.napms(500)

        self.curses_view.display_error("")
        # self.go_back()
        self.open_select_tournament_load()

    @saveNav
    def open_load_save(self):
        """ Open the menu offering to load or save data. """

        self._set_menu_view("list", call=Menu.save_n_load)

    # --- Quit menu ---

    def open_quit_menu(self):
        """ Open the menu offering to quit with or without saving data. """

        self._set_menu_view("list", call=Menu.quit)

    def quit(self):
        """ Display an exit message and close the application. """

        self._set_full_view("print-line", text="Closing...")
        curses.napms(500)
        self._set_full_view("print-line", text="Bye!")
        curses.napms(500)
        sys.exit(0)

    def save_n_quit(self):
        """ Save the data and display a message, then call quit()."""

        self._set_full_view("print-line", text="Sauvegarde...")
        TinyDbView.save_all()
        curses.napms(500)
        self.quit()

    # --- Back menu ---

    def go_back(self):
        """ Open the last page (minus the current one) registerd with the @saveNav decorator. """

        if len(nav_history) > 1:
            nav_history.pop()
            target = nav_history[-1]
            target[0](*target[1], **target[2])

    # === DEMO methods ===

    def _generate_fake_players(self):
        """ Demo method used to quickly generate fake players (bind to CTRL+F12). """

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
        """ Align the size of the provided list to the size
            of the larger item (filling with space).

        Parameters
        ----------
        options : list
            The list to adjust to its larger element
        """

        max_size = max([len(option) for option in options])
        return [option.ljust(max_size) for option in options]

    def _move_selection(self, key):
        """ Control the mouvement of the selection when
            displaying a menu or a  list of selectable items.

        Parameters
        ----------
        key : int
            A key number
        """

        for screen in self._list_data.keys():

            sdata = self._list_data[screen]
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

            self._list_data[screen]["current_row"] = current_row
            # colorset = self._list_data["colorset"]

            self.curses_view.display_select(screen, buttons, current_row)

    # === View controls ===

    def _set_focus(self, focus):
        """ Control the CurseView focus.

        Parameters
        ----------
        focus : str ('main'/'menu'/'full')
            A shortname to indicate where to place the focus
        """

        if focus == "main":
            self.curses_view.focus = self.curses_view.main
        elif focus == "full":
            self.curses_view.focus = self.curses_view.screen
        else:
            self.curses_view.focus = self.curses_view.menu

    def _set_head_view(self, action, **kwargs):
        """ _set_view shortcut to control the content
            of the head window of the CurseView

        Parameters
        ----------
        view : Curse.window
            Determine the CurseView used to draw the requested content
        action : str
            Determine the kind of content to draw
        **kwargs : *
            Used to pass various parameters depending upon the action
        """

        return self._set_view("head", action, **kwargs)

    def _set_menu_view(self, action, **kwargs):
        """ _set_view shortcut to control the content
            of the menu window of the CurseView

        Parameters
        ----------
        view : Curse.window
            Determine the CurseView used to draw the requested content
        action : str
            Determine the kind of content to draw
        **kwargs : *
            Used to pass various parameters depending upon the action
        """

        return self._set_view("menu", action, **kwargs)

    def _set_main_view(self, action, **kwargs):
        """ _set_view shortcut to control the content
            of the main window of the CurseView

        Parameters
        ----------
        view : Curse.window
            Determine the CurseView used to draw the requested content
        action : str
            Determine the kind of content to draw
        **kwargs : *
            Used to pass various parameters depending upon the action
        """

        return self._set_view("main", action, **kwargs)

    def _set_full_view(self, action, **kwargs):
        """ _set_view shortcut to control the content of
            the base window (full screen) of the CurseView

        Parameters
        ----------
        view : Curse.window
            Determine the CurseView used to draw the requested content
        action : str
            Determine the kind of content to draw
        **kwargs : *
            Used to pass various parameters depending upon the action
        """

        return self._set_view("full", action, **kwargs)

    def _set_view(self, view, action, **kwargs):
        """ Control the content of the given window of the CurseView.

        Parameters
        ----------
        view : Curse.window
            Determine the CurseView used to draw the requested content
        action : str
            Determine the kind of content to draw
        **kwargs : *
            Used to pass various parameters depending upon the action
        """

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
            self.curses_view.display_text(screen, "")

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

            self._list_data[screen] = {
                "screen": screen,
                "current_row": current_row,
                "labels": labels,
                "actions": actions,
                "params": params,
                "buttons": buttons,
                "colors": colors,
                "active_links": active_links,
            }

            self.curses_view.display_select(screen, buttons, current_row, colors)

        # --- Print one text line into the view ---
        elif action == "print-line":
            self.curses_view.display_text(screen, kwargs.get("text", "Error"), colors)

        # --- Print several text lines into the view ---
        elif action == "print-lines":
            self.curses_view.display_list(screen, kwargs.get("rows", ["Error"]), colors)

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

    # === Form controls ===

    def _form_setup(self, screen, rows, exit_func, source=None):
        """ Initialize a new form. """

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
        """ Control the form navigation (TAB & SHIFT + TAB). """

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
        """ Control the form tests. """

        if test is None or eval(test) is True:
            error_win.clear()
            error_win.refresh()
            return True
        else:
            error_win.clear()
            error_win.addstr(errormsg)
            error_win.refresh()

    def _form_gather_inputs(self, text_boxes, rows, exit_func, source):
        """ Gather form inputs and transmit to callback functions. """

        inputs = {}
        valid_rows = [x for x in rows if x.get("name", False)]

        for row, tb in zip(valid_rows, text_boxes):
            if row.get("name", False):
                inputs[row["name"]] = tb.gather().strip()

        exit_func(inputs, source)

        raise UnstackAll("SUBMIT")

    def _form_exit_new_tournament(self, inputs, source):
        """ Process the new tournament informations and transmit to the model.

        Parameters
        ----------
        inputs : list
            The collected input' value
        source : list
            The original values if provided (receive None otherwise)
        """

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
        """ Process the tournament modified informations and transmit to the model.

        Parameters
        ----------
        inputs : list
            The collected input' value
        source : list
            The original values if provided (receive None otherwise)
        """

        logging.info(f"EDIT TOURNAMENT VALUES: {inputs}")
        source.name = inputs["name"]
        source.place = inputs["place"]
        source.start_date = inputs["start_date"]
        source.end_date = inputs["end_date"]
        source.game_type = inputs["game_type"]
        source.description = inputs["description"]
        source.num_rounds = int(inputs["num_rounds"])

        # self.go_back()
        self.open_tournament_initialize()

    def _form_exit_new_actor(self, inputs, source):
        """ Process the new actor informations and transmit to the model.

        Parameters
        ----------
        inputs : list
            The collected input' value
        source : list
            The original values if provided (receive None otherwise)
        """

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
        """ Process the actor modified informations and transmit to the model.

        Parameters
        ----------
        inputs : list
            The collected input' value
        source : list
            The original values if provided (receive None otherwise)
        """

        logging.info(f"EDIT ACTOR VALUES: {inputs}")
        source.family_name = inputs["family_name"]
        source.first_name = inputs["first_name"]
        source.birthdate = inputs["birthdate"]
        source.sex = inputs["sex"]
        source.elo = inputs["elo"]

        self.go_back()

    def _form_exit_edit_final_note(self, inputs, source):
        """ Process the final note input and transmit to the model.

        Parameters
        ----------
        inputs : list
            The collected input' value
        source : list
            The original values if provided (receive None otherwise)
        """

        logging.info(f"EDIT FINAL NOTE: {inputs}")
        source.description = inputs["description"]

        self.open_tournament_closed()

    def _form_exit_input_scores(self, inputs, source):
        """ Process the round score inputs and transmit to the model.

        Parameters
        ----------
        inputs : list
            The collected input' value
        source : list
            The original values if provided (receive None otherwise)
        """
        logging.info(f"INPUT SCORES: {inputs}")

        tournament = World.get_active_tournament()

        for i, k in enumerate(inputs):
            tournament.set_results(i, *Round.convert_score_symbol(inputs[k]))

        self.start_new_round()


class UnstackAll(Exception):
    """Exception used to exit nested curses edit calls.

    There must be a better way to do that, but that's my best call at the moment..
    """

    pass


""" I initialize this variable to get ride of flake8 error...
Validation is used by my eval expessions and thus it's not directly visible.
On a real project I wouldn't add this variable """
v = Validation()
