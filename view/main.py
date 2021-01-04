#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to handle the menu views
    of this chess tournament manager
"""

import curses
import curses.textpad
import inspect
import logging


class CurseView:
    def __init__(self):
        logging.info("< Open Main View")

        self.screen = curses.initscr()

        # tweak terminal settings
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        curses.curs_set(0)

        # Colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected row
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Menu 1
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)  # Menu 2

        self.screen.refresh()

        # Init menu window & main window
        maxH, maxW = self.screen.getmaxyx()
        headH = 1
        self.head = curses.newwin(headH, maxW, 0, 0)
        self.main = curses.newwin(maxH - 10 - headH, maxW, headH, 0)
        self.menu = curses.newwin(10, maxW, maxH - 10, 0)

        self.focus = self.menu
        self.last_draws = {}

    def close(self):
        logging.info("> Close Main View")

        # reverse terminal settings
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()

        # close the application
        curses.endwin()

    def clear_head(self):
        self.head.clear()
        self.head.refresh()

    def clear_main(self):
        self.main.clear()
        self.main.refresh()

    def clear_menu(self):
        self.menu.clear()
        self.menu.refresh()

    # --------------------------------

    def display_list(self, screen, options, current_row, colors=[1, 2]):
        self._save_last_draw(screen, options, current_row, colors=colors)

        # turn off cursor blinking
        curses.curs_set(0)

        self._set_background_color(screen)
        colors[0] = 1  # TODO

        # clear screen
        screen.clear()

        # get screen size
        h, w = screen.getmaxyx()

        # display select list
        for i, option in enumerate(options):
            x = w // 2 - len(option) // 2
            y = h // 2 - len(options) // 2 + i

            if i == current_row:
                screen.attron(curses.color_pair(colors[0]))
                screen.addstr(y, x, option)
                screen.attroff(curses.color_pair(colors[0]))
            else:
                screen.addstr(y, x, option)

        # update screen
        self._set_focus_design()
        screen.refresh()

    def print_center_multi(self, screen, rows, colors=[1, 2]):
        self._save_last_draw(screen, rows, colors=colors)

        self._set_background_color(screen)

        h, w = screen.getmaxyx()
        max_txt = max([len(x) for x in rows])
        x = w // 2 - max_txt // 2
        y = (h - len(rows)) // 2
        for i, row in enumerate(rows):
            screen.addstr(y + i, x, row)

        # update screen
        self._set_focus_design()
        screen.refresh()

    def print_center(self, screen, text, colors=[1, 2]):
        self._save_last_draw(screen, text, colors=colors)

        self._set_background_color(screen)

        h, w = screen.getmaxyx()
        x = w // 2 - len(text) // 2
        y = h // 2
        screen.addstr(y, x, text)

        # update screen
        self._set_focus_design()
        screen.refresh()

    def get_input(self, screen, label, placeholder=None, errormsg=None, colors=[1, 2]):
        self._save_last_draw(
            screen, label, placeholder=placeholder, errormsg=errormsg, colors=colors
        )

        # self.set_focus(screen, False)

        curses.curs_set(1)  # turn on cursor blinking
        self._set_background_color(screen)

        # Place one line input
        h, w = screen.getmaxyx()
        x = w // 2 - len(label) // 2
        y = h // 2

        screen.addstr(y - self.head.getmaxyx()[0], x, label)

        # logging.error(f"ERROR TXT: {errormsg}")
        if errormsg is not None:
            x = w // 2 - len(errormsg) // 2
            screen.addstr(y + 5, x, errormsg)

        x = w // 2 - 40 // 2
        sub = screen.subwin(3, 40, y + 1, x)
        sub.border()

        sub2 = sub.subwin(1, 38, y + 2, x + 1)
        if placeholder is not None:
            sub2.addstr(placeholder)

        tb = curses.textpad.Textbox(sub2)
        screen.refresh()

        def check_key(k):
            logging.debug(k)
            if k == 9:
                raise Exception("Test")
                self.swap_focus()
            return k

        tb.edit(check_key)
        screen.refresh()

        value = tb.gather()[:-1].strip()
        # logging.debug(f"INPUT: ->{value}<-")

        # Reset the content of the input window
        tb.do_command(curses.ascii.SOH)
        tb.do_command(curses.ascii.VT)
        tb.do_command(curses.ascii.FF)
        sub.border()
        sub.refresh()

        curses.curs_set(0)  # turn off cursor blinking

        # update screen
        self._set_focus_design()
        screen.refresh()

        return value

    def swap_focus(self):
        if self.focus == self.menu:
            self.set_focus(self.main)
        else:
            self.set_focus(self.menu)

    def set_focus(self, focus, refresh=True):
        self.focus = focus

        if refresh is False:
            return

        for win in self.last_draws.values():
            eval(f"self.{win[0]}")(*win[1], **win[2])

        self._set_focus_design()

    def _set_focus_design(self):
        self.focus.border()
        self.focus.refresh()
        #self.main.refresh()
        #self.menu.refresh()
        #self.head.refresh()
        #self.screen.refresh()

    def _save_last_draw(self, *args, **kwargs):
        f = inspect.stack()[1][3]  # caller function name
        if args[0] == self.main:
            self.last_draws["main"] = [f, args, kwargs]
        elif args[0] == self.menu:
            self.last_draws["menu"] = [f, args, kwargs]
        elif args[0] == self.head:
            self.last_draws["head"] = [f, args, kwargs]
        elif args[0] == self.screen:
            self.last_draws["full"] = [f, args, kwargs]

    def _set_background_color(self, screen):
        screen.clear()
        if screen is self.main:
            screen.bkgd(" ", curses.color_pair(2) | curses.A_BOLD)
        else:
            screen.bkgd(" ", curses.color_pair(3) | curses.A_BOLD)

    def get_win_name(self, win):
        if win == self.main:
            return "main"
        elif win == self.menu:
            return "menu"
        elif win == self.head:
            return "head"
        elif win == self.screen:
            return "full"
