#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to handle the menu views
    of this chess tournament manager
"""

# import curses


class CurseView:
    """ D """

    @staticmethod
    def print_center(stdscr, text):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        x = w // 2 - len(text) // 2
        y = h // 2
        stdscr.addstr(y, x, text)
        stdscr.refresh()


class MainView(CurseView):
    """ D """

    @classmethod
    def say_goodbye(cls, stdscr):
        cls.print_center(stdscr, "Vous quittez le programme")
