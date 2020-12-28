#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to handle the menu views
    of this chess tournament manager
"""

import curses

from view.main import CurseView


class MenuView(CurseView):
    """ D """

    @staticmethod
    def display_menu(stdscr, current_row, options):

        # turn off cursor blinking
        curses.curs_set(0)

        # add color scheme for selected row
        curses.init_pair(
            1, curses.COLOR_BLACK, curses.COLOR_WHITE
        )  # TODO move to init ?

        # clear screen
        stdscr.clear()

        # get screen size
        h, w = stdscr.getmaxyx()

        # display menu
        for i, option in enumerate(options):
            x = w // 2 - len(option) // 2
            y = h // 2 - len(options) // 2 + i

            if i == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, option)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, option)

        # update screen
        stdscr.refresh()
