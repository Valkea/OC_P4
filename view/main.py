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
        self.headH = 1
        errorH = 1
        mainH = maxH - 10 - self.headH - errorH
        menuH = 10

        self.head = curses.newwin(self.headH, maxW, 0, 0)
        self.main = curses.newwin(mainH, maxW, self.headH, 0)
        self.error = curses.newwin(errorH, maxW, self.headH+mainH, 0)
        self.menu = curses.newwin(menuH, maxW, maxH - 10, 0)

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

    def display_error(self, text):

        # get screen size
        h, w = self.error.getmaxyx()
        x = w // 2 - len(text) // 2

        # print msg
        self.error.addstr(0, x, str(text))
        self.error.refresh()
        curses.napms(2500)  # TODO blocking
        self.error.clear()
        self.error.refresh()

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

    # --- FORMS ---

    def init_form(self, screen, rows, source=None):

        logging.info("INIT FORM")
        # self._save_last_draw(screen, rows)

        curses.curs_set(1)  # turn on cursor blinking
        self._set_background_color(screen)

        text_boxes, text_wins, error_box = self._draw_them_all(screen, rows, source)
        screen.border()
        screen.refresh()
        return text_boxes, text_wins, error_box

    def close_form(self, screen):
        logging.info("CLOSE FORM")
        # screen.clear()
        # screen.refresh()
        # textboxes = self._draw_them_all(screen, rows)
        # screen.move(5, 5)
        curses.curs_set(0)  # turn off cursor blinking

    def set_input_focus(self, input_win, input_tb, control_function):

        v = input_tb.gather().strip()

        input_win.clear()
        input_win.addstr(v)

        input_tb.edit(control_function)
        pass

    def _draw_them_all(self, screen, rows, source=None):

        maxW = max([len(x["label"]) for x in rows])

        text_boxes = []
        text_wins = []

        s = 4
        h, w = screen.getmaxyx()
        x = w // 2 - maxW // 2
        y = (h - self.headH - len(rows) * s) // 2

        for i, row in enumerate(rows):
            y += s

            # label display
            label = row["label"]
            screen.addstr(y - self.head.getmaxyx()[0], x, label)

            # note display
            has_name = row.get("name", False)
            if has_name is False:
                y -= s - 1
                continue

            # size option
            input_size = row.get("size", False)
            if input_size:
                width = input_size
            else:
                width = max(maxW, 35)

            # same_row option
            x_off = x
            y_off = y
            same_row = row.get("same_row", False)
            if same_row:
                y_off = y - 2
                x_off = x + maxW // 2 - input_size // 2
                y -= 1

            # input box
            sub = screen.subwin(3, width, y_off + 1, x_off)
            sub.border()

            sub2 = sub.subwin(1, width - 2, y_off + 2, x_off + 1)
            if source is not None:
                sub2.addstr(str(eval("source." + row["name"])))
            elif row["placeholder"] is not None:
                sub2.addstr(str(row["placeholder"]))
            tb = curses.textpad.Textbox(sub2)

            # save instances
            text_boxes.append(tb)
            text_wins.append(sub2)

        error_win = screen.subwin(3, max(maxW, 35), y + 5, x)

        return text_boxes, text_wins, error_win

    # --- FOCUS ---

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

    # --- GENERIC ---

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
