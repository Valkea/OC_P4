#! /usr/bin/env python3
# coding: utf-8

""" This module handles the actors of the tournaments
"""

import json


class Player:
    """This class handles the chess players

    Attributes
    ----------
    first_name : str
    family_name : str
    birthdate : str
        must be a 'DD/MM/YYYY' string
    sex = str
        can be either 'M' or 'F'
    elo = int
        must be greater than 0
    score = int
        points earned in the current tournament

    Methods
    -------
    add_to_score(value)
        add to the current player's score
    fullname()
        return a concatenation of the first and family names
    toJSON()
        convert the current instance to a JSON dictionnary
    """

    def __init__(self, family_name, first_name, birthdate, sex, elo):
        self.family_name = family_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.sex = sex
        self.elo = elo
        self.score = 0

    def add_to_score(self, value):
        """Add the given value to the current player score
            if the value is 0>=value<=1

        Parameters
        ----------
        value : int
            the score value to add to the current player's score
        """

        if value < 0 or value > 1:
            raise ValueError("Le score doit être compris entre 0 et 1")

        self.score += value

    def fullname(self):
        """ Return the concatenation of the fist and family names """

        return self.first_name + " " + self.family_name

    def toJSON(self):
        """ Return a JSON representation of the Player instance """

        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __repr__(self):
        return (
            f"Player('{self.family_name}', '{self.first_name}', "
            f"'{self.birthdate}', '{self.sex}', {self.elo}, {self.score})"
        )
