#! /usr/bin/env python3
# coding: utf-8

import logging
import traceback

from controller.main import Controller

logging.basicConfig(filename="CTM.log", filemode="w", level=logging.INFO)

try:
    control = Controller()
    control.open_menu_base()
    control.start()
except Exception as e:
    tb = traceback.format_exc()
    logging.error(f"{e} {tb}")
