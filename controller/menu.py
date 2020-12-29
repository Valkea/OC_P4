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
# from view.menu import MenuView
# from view.main import MainView

from model.menu import Menu


class Controller:
    """D """

    def __init__(self):
        logging.info("< Open Controller")
        self.curses_view = CurseView()
        self.menu_model = Menu()
        self.focus = "menu"

        atexit.register(self._close)

    def _close(self):
        logging.info("> Close Controller")
        self.curses_view.close()

    # Main controls #

    def open_goodbye(self):
        self.curses_view.say_goodbye()
        # self._control_center()
        self.focus = "main"

    def open_test2(self):
        #self.curses_view.print_center("Test2", self.curses_view.screen)  # Pas de print ici
        self._set_main()
        self.focus = "main"

    def open_test3(self):
        self.curses_view.print_center("Test3", self.curses_view.main)  # Pas de print ici

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
        #self.focus = "main"

    def open_tournois_select(self):
        options = self.menu_model.menu_tournois_select()
        colorset = [1, 2]
        self._set_menu(options, colorset)

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
                    self.curses_view.main
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

    def open_new_tournament(self):
        logging.debug("START SET MAIN")
        #self.curses_view.clear_menu()
        
        name = self.check_input("Nom du tournoi", "x.isalpha()", None, "Des lettres...")
        place = self.check_input("Lieu du tournoi", "len(x) > 3", None, "Plus de 3...")
        start_date = self.check_input("Date de début", "self.test(x)", None, "Plus de 4...")
        end_date = self.curses_view.get_input("Date de fin [JJ/MM/YYYY]")
        num_rounds = self.curses_view.get_input("Nombre de tours")
        time_control = self.curses_view.get_input("Contrôle de temps [Bullet|Blitz|Coup rapide]")
        description = self.curses_view.get_input("Description")
        self.curses_view.clear_main()
        logging.debug("END SET MAIN")

    def test(self, v):
        if len(v) > 4:
            return True
        else:
            return False

    def check_input(self, label, test, placeholder=None, error=None):

        e = None
        testx = test.replace("x", "value")
        while 1:
            value = self.curses_view.get_input(label, e)
            if eval(testx):
                break
            else:
                e = error

        return value


    def open_new_actor(self):
        logging.debug("START SET MAIN")
        #self.curses_view.clear_menu()
        self.curses_view.get_input("Nom")
        self.curses_view.get_input("Prénom")
        self.curses_view.get_input("Date de naissance [JJ/MM/AAAA]")
        self.curses_view.clear_main()
        logging.debug("END SET MAIN")

    def _get_main(self, key):
        self.focus = "menu"
        self.open_menu_base()
        #x = random.randint(0, 100)
        #self.curses_view.print_center(f"Test {x}", self.curses_view.screen)
        pass
