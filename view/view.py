#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to handle the views
    of this chess tournament manager
"""


import curses
import sys


class View:
    def __init__(self):
        pass


# Model #
class Menu:
    def __init__(self):
        pass

    def menu_base(self):
        return (("Tournoi", None), ("Rapports", None), ("Quitter", None))


class MenuController:
    def __init__(self):
        pass

    def open_base(self):
        self.view = MenuView(
            [
                "Tournoi",
                "Rapports",
                "Quitter",
            ],
            [
                self.open_tournoi,
                self.open_reports,
                self.quit,
            ],
        )

    def quit(self):
        sys.exit(0)

    def open_tournoi(self):
        self.view = MenuView(
            [
                "Créer un tournoi",
                "Liste de tous les tournois",
                "< Retour",
            ],
            [
                None,
                self.open_tournoi_list,
                self.open_base,
            ],
        )

    def open_tournoi_list(self):
        self.view = MenuView(
            [
                "Charger",
                "Editer",
                "Supprimer",
                "< Retour",
            ],
            [
                None,
                None,
                None,
                self.open_tournoi,
            ],
        )

    def open_reports(self):
        self.view = MenuView(
            [
                "Liste de tous les acteurs de tous les tournois",
                "Liste de tous les joueurs de tous les tournois",
                "Liste de tous les tours d'un tournoi",
                "Liste de tous les matchs d'un tournoi",
                "< Retour",
            ],
            [
                None,
                None,
                None,
                None,
                self.open_base,
            ],
        )


class MenuView:
    def __init__(self, options, calls):
        self.options = options
        self.options_aligned = self.align_to_larger(options)
        self.calls = calls

        curses.wrapper(self.control_menu)

    def align_to_larger(self, options):

        max_size = max([len(option) for option in options])
        return [option.ljust(max_size) for option in options]

    def print_center(self, stdscr, text):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        x = w // 2 - len(text) // 2
        y = h // 2
        stdscr.addstr(y, x, text)
        stdscr.refresh()

    def control_menu(self, stdscr):

        current_row = 0
        self.display_menu(stdscr, current_row)

        while 1:
            key = stdscr.getch()

            # clear existing texts
            stdscr.clear()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(self.options) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:

                if self.calls[current_row] == None:
                    self.print_center(
                        stdscr, "You selected '{}'".format(self.options[current_row])
                    )
                    stdscr.getch()
                else:
                    self.calls[current_row]()
                # if user selected last row, exit the program
                # if current_row == len(self.options)-1:
                #    break
            # else:
            #    break
            self.display_menu(stdscr, current_row)

    def display_menu(self, stdscr, current_row):

        # turn off cursor blinking
        curses.curs_set(0)

        # add color scheme for selected row
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # clear screen
        stdscr.clear()

        # get screen size
        h, w = stdscr.getmaxyx()

        # display menu
        for i, option in enumerate(self.options_aligned):
            x = w // 2 - len(option) // 2
            y = h // 2 - len(self.options) // 2 + i

            if i == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, option)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, option)

        # update screen
        stdscr.refresh()


# menu = Menu(["Charger", "Editer", "Supprimer"], [None, None, None])
menu = MenuController()
menu.open_base()
