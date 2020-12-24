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

    Methods
    -------
    toJSON()
        convert the current instance to a JSON dictionnary
    """

    def __init__(self, family_name, first_name, birthdate, sex, elo):
        self.sex = sex
        self.family_name = family_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.elo = elo
        self.score = 0

    # ----------------------------
    def add_to_score(self, value):
        if value < 0 or value > 1:
            raise ValueError("Le score doit être compris entre 0 et 1")

        self.score += value

    def fullname(self):
        return self.first_name + " " + self.family_name

    # ----------------------------

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __repr__(self):
        return (
            f"Player('{self.family_name}', '{self.first_name}', "
            f"'{self.birthdate}', '{self.sex}', {self.elo}, {self.score})"
        )
