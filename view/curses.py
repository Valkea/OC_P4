#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to handle terminal views """

import curses
import curses.textpad
import inspect
import logging


class CurseView:
    """This class provide various methods to display text, select.

    Attributes
    ----------
    screen : Cuses.window
        This is the main curses window (full screen)
    head : Curses.window
        This is the window in which the section title is displayed (top)
    main : Curses.window
        This is the window in which the section content is displayed (center)
    menu : Curses.window
        This is the window in which the menu is displayed (bottom)
    error : Curses.window
        This is the window in which the errors are displayed (above the menu)
    focus : Curses.window
        This is any of the previous windows

    Public Methods
    --------------
    close()
        Set the terminal back to its original settings
    clear_head()
        Clear the content of the head window
    clear_main()
        Clear the content of the main window
    clear_menu()
        Clear the content of the menu window

    display_error(text)
        Display the given message in the error window
    display_select(screen, options, current_row, colors=[1, 2])
        Display the given list as a menu and highlight the currently selected row
    display_list(screen, rows, colors=[1, 2])
        Display the given list as a centered multi-lines list
    display_text(screen, text, colors=[1, 2])
        Display the given text at the center of the given window

    init_form(screen, rows, source=None)
        Display a form and return the edit-box instances (the controller do the editing part)
    close_form(screen)
        Stop the cursor blinking

    set_input_focus(input_win, input_tb, control_function)
        Change the current input field focus to the provided one
    set_focus(focus, refresh=True)
        Change the window focus to the provided one
    swap_focus()
        Swap focus between the main and menu windows

    Private Methods
    ---------------
    _draw_form(screen, rows, source=None)
        Actually draw the form and return it to the init_form method
    _set_focus_design()
        Display a border around the currently focused window
    _save_last_draw(*args, **kwargs)
        Save the last item drawn so we can refraw it if needed (TODO problems with forms)
    _set_background_color(screen)
        Change the target window background color (and reset content... so call it first)
    """

    def __init__(self):
        logging.info("< Open Main View")

        self.screen = curses.initscr()

        # Tweak terminal settings
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
        self._headH = 1
        errorH = 1
        self._mainH = maxH - 10 - self._headH - errorH
        menuH = 10

        self.head = curses.newwin(self._headH, maxW, 0, 0)
        self.main = curses.newwin(self._mainH, maxW, self._headH, 0)
        self.error = curses.newwin(errorH, maxW, self._headH + self._mainH, 0)
        self.menu = curses.newwin(menuH, maxW, maxH - 10, 0)

        self.focus = self.menu
        self._last_draws = {}

    # === PUBLIC METHODS ===

    def close(self):
        """ Set the terminal back to its original settings. """

        logging.info("> Close Main View")

        # reverse terminal settings
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()

        # close the application
        curses.endwin()

    # --- Clear screens --

    def clear_head(self):
        self.head.clear()
        self.head.refresh()

    def clear_main(self):
        self.main.clear()
        self.main.refresh()

    def clear_menu(self):
        self.menu.clear()
        self.menu.refresh()

    # --- Display ---

    def display_error(self, text):
        """Display the given message in the error window

        Parameters
        ----------
        text : str
            The text to display
        """

        # get screen size
        h, w = self.error.getmaxyx()
        x = w // 2 - len(text) // 2

        # print msg
        if text == "":
            self.error.clear()
        else:
            self.error.addstr(0, x, str(text))

        self.error.refresh()

    def display_select(self, screen, options, current_row, colors=[1, 2]):
        """Display the given list as a menu and highlight the currently selected row.

        Parameters
        ----------
        screen : Curses.window
            The window on which the drawing takes place
        options : dict
            A dictionary containing the various informations required to draw the menu
        current_row : int
            The row index of the currently selected row
        colors : list(int)
            The colorsettings to use for drawing
        """

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
            if i < self._mainH - 1:
                x = w // 2 - len(option) // 2
                y = h // 2 - min(len(options), self._mainH - 1) // 2 + i

                if i == current_row:
                    screen.attron(curses.color_pair(colors[0]))
                    screen.addstr(y, x, option)
                    screen.attroff(curses.color_pair(colors[0]))
                else:
                    screen.addstr(y, x, option)

        # update screen
        self._set_focus_design()
        screen.refresh()

    def display_list(self, screen, rows, colors=[1, 2]):
        """Display the given list as a centered multi-lines list.

        Parameters
        ----------
        screen : Curses.window
            The window on which the drawing takes place
        rows : dict
            A dictionary containing the various informations required to draw the input fields
        colors : list(int)
            The colorsettings to use for drawing
        """

        self._save_last_draw(screen, rows, colors=colors)

        self._set_background_color(screen)

        h, w = screen.getmaxyx()
        max_txt = max([len(x) for x in rows])
        x = w // 2 - max_txt // 2
        y = (h - min(len(rows), self._mainH - 1)) // 2
        for i, row in enumerate(rows):
            if i < self._mainH - 1:
                screen.addstr(y + i, x, row)

        # update screen
        self._set_focus_design()
        screen.refresh()

    def display_text(self, screen, text, colors=[1, 2]):
        """Display the given text at the center of the given window.

        Parameters
        ----------
        screen : Curses.window
            The window on which the drawing takes place
        text : str
            The text to display
        colors : list(int)
            The colorsettings to use for drawing
        """

        self._save_last_draw(screen, text, colors=colors)

        self._set_background_color(screen)

        h, w = screen.getmaxyx()
        x = w // 2 - len(text) // 2
        y = h // 2
        screen.addstr(y, x, text)

        # update screen
        self._set_focus_design()
        screen.refresh()

    # --- Forms methods ---

    def init_form(self, screen, rows, source=None):
        """Display a form and return the edit-box instances.
            (the controller do the editing part)

        Parameters
        ----------
        screen : Curses.window
            The window on which the drawing takes place
        rows : dict
            A dictionary containing the various informations required to draw the input fields
        source :
            An optional dictionary containing the values to place in the fields (edit mode)

        Returns
        -------
        text_boxes : Curses.TextBox
        text_wins : Curses.windows
        error_win : Curses.window
        """

        # self._save_last_draw(screen, rows, source)  # TODO no refocus on redraw
        logging.info("INIT FORM")

        curses.curs_set(1)  # turn on cursor blinking
        self._set_background_color(screen)

        text_boxes, text_wins, error_box = self._draw_form(screen, rows, source)
        screen.border()
        screen.refresh()
        return text_boxes, text_wins, error_box

    def close_form(self, screen):
        """ Stop the cursor blinking. """

        logging.info("CLOSE FORM")
        curses.curs_set(0)  # turn off cursor blinking

    # --- Focus ---

    def set_input_focus(self, input_win, input_tb, control_function):
        """Change the current input field focus to the provided one.

        Parameters
        ----------
        input_win : Curses.window
            The window on which the form has been drawn
        input_tb :
            The TextBox instance to put focus on
        control_function :
            The function called on each chr input while editing
        """

        v = input_tb.gather().strip()

        input_win.clear()
        input_win.addstr(v)

        input_tb.edit(control_function)

    def set_focus(self, focus, refresh=True):
        """Change the window focus to the provided one.

        Parameters
        ----------
        focus : Curses.window
            The screen to set as the current focus
        refresh : bool(True)
            Redraw screen if needed
        """
        self.focus = focus

        if refresh is False:
            return

        for win in self._last_draws.values():
            eval(f"self.{win[0]}")(*win[1], **win[2])

        self._set_focus_design()

    def swap_focus(self):
        """ Swap focus between the main and menu windows. """

        if self.focus == self.menu:
            self.set_focus(self.main)
        else:
            self.set_focus(self.menu)

    # === PRIVATE METHODS ===

    def _draw_form(self, screen, rows, source=None):
        """Draw the form and return it to the init_form method

        Parameters
        ----------
        screen : Curses.window
            The window on which the drawng takes place
        rows : dict
            A dictionary containing the various informations required to draw the input fields
        source :
            An optional dictionary containing the values to place in the fields (edit mode)

        Returns
        -------
        text_boxes : Curses.TextBox
        text_wins : Curses.windows
        error_win : Curses.window
        """

        min_input_width = 35

        maxW = max([len(x["label"]) for x in rows])
        maxW = max(maxW, min_input_width)

        text_boxes = []
        text_wins = []

        s = 4
        estimated_size = len(rows) * s
        h, w = screen.getmaxyx()
        x = w // 2 - maxW // 2
        y = (h - estimated_size) // 2
        y -= 3

        for i, row in enumerate(rows):
            y += s

            # label display
            label = row["label"]
            screen.addstr(y - 1, x, label)

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
                width = max(maxW, min_input_width)

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

        error_win = screen.subwin(2, max(maxW, min_input_width), y + 5, x)

        return text_boxes, text_wins, error_win

    def _set_focus_design(self):
        """ Display a border around the currently focused window. """

        self.focus.border()
        self.focus.refresh()

    def _save_last_draw(self, *args, **kwargs):
        """Save the last item drawn so we can refraw it if needed.

            TODO problems with forms...

        Parameters
        ----------
        *args & ** kwargs
            The current parameters of the parent function
        """

        f = inspect.stack()[1][3]  # caller function name
        if args[0] == self.main:
            self._last_draws["main"] = [f, args, kwargs]
        elif args[0] == self.menu:
            self._last_draws["menu"] = [f, args, kwargs]
        elif args[0] == self.head:
            self._last_draws["head"] = [f, args, kwargs]
        elif args[0] == self.screen:
            self._last_draws["full"] = [f, args, kwargs]

    def _set_background_color(self, screen):
        """Change the target window background color.
            It also reset the content... so call it first !

        Parameters
        ----------
        screen : Curses.window
            The window to target
        """

        screen.clear()
        if screen is self.main:
            screen.bkgd(" ", curses.color_pair(2) | curses.A_BOLD)
        else:
            screen.bkgd(" ", curses.color_pair(3) | curses.A_BOLD)
