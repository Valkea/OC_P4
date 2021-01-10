#! /usr/bin/env python3
# coding: utf-8

""" This module handles the form imput validations """

import re


class Validation:
    """This class offers variours methods prepared to validate the input fields.

    Static Methods
    --------------
    is_valid_date(v)
        Check if the provided value is compatible with JJ/MM/YYYY
    is_valid_posint(v)
        Check if the provided value is a positive integer
    is_valid_gtype(v)
        Check if the provided value is a value game type (blitz/bullet/coup rapide)
    is_valid_sex(v)
        Check if the provided value either starts with h or f (Homme or Femme)
    is_valid_score_symbol(v)
        Check if the provided value is <, > or =

    """

    @staticmethod
    def is_valid_date(v):
        """ Check if the provided value is compatible with JJ/MM/YYYY. """

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
        """ Check if the provided value is a positive integer. """

        try:
            return int(v) > 0
        except ValueError:
            return False

    @staticmethod
    def is_valid_gtype(v):
        """ Check if the provided value is a value game type (blitz/bullet/coup rapide). """

        v = v.lower()
        if v == "bullet" or v == "blitz" or v == "coups rapides" or v == "coup rapide":
            return True
        return False

    @staticmethod
    def is_valid_sex(v):
        """ Check if the provided value either starts with h or f (Homme or Femme) """

        v = v.lower()[0:1]
        if v == "h" or v == "f":
            return True
        return False

    @staticmethod
    def is_valid_score_symbol(v):
        """ Check if the provided value is <, > or =. """

        if v == "<" or v == ">" or v == "=":
            return True
        return False
