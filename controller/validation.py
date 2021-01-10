#! /usr/bin/env python3
# coding: utf-8

""" This module handles the form imput validations """

import re
import logging


class Validation:
    """ D """

    @staticmethod
    def is_valid_date(v):
        """ D """
        try:
            s = re.search(
                "^([0-9]{1,2})[-/. ]([0-9]{1,2})[-/. ]([0-9]{2,4})$", v
            ).groups()
            if int(s[0]) > 31 or int(s[1]) > 12 or len(s) != 3:
                return False
            return True
        except AttributeError:
            return False

    @staticmethod
    def is_valid_posint(v):
        """ D """
        try:
            return int(v) > 0
        except ValueError:
            return False

    @staticmethod
    def is_valid_gtype(v):
        """ D """
        v = v.lower()
        if v == "bullet" or v == "blitz" or v == "coups rapides" or v == "coup rapide":
            return True
        return False

    @staticmethod
    def is_valid_sex(v):
        """ D """
        v = v.lower()[0:1]
        if v == "h" or v == "f":
            return True
        return False

    @staticmethod
    def is_valid_score_symbol(v):
        """ D """
        logging.info(f"is_valid_score_symbol: {v}")
        if v == "<" or v == ">" or v == "=":
            return True
        return False
