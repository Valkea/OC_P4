#! /usr/bin/env python3
# coding: utf-8

import logging

from controller.menu import Controller  # , MenuController

logging.basicConfig(filename="debug.txt", filemode="w", level=logging.DEBUG)

try:
    control = Controller()
    control.open_menu_base()
    control.start()
except Exception as e:
    logging.error(e)
