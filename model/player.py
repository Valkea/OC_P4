#! /usr/bin/env python3
# coding: utf-8

""" This module handles the actors of the tournaments
"""

import json


class Player:
    """_This class handles the chess players

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
    games = list
        the list of all the opponents played along with their final score

    Methods
    -------
    TODO !!!!!!!!!!!!!!!!!!!!!!!
    add_to_score(value)
        add to the current player's score
    fullname()
        return a concatenation of the first and family names
    toJSON()
        convert the current instance to a JSON dictionnary
    """

    labels = {
        "family_name": "Nom de famille",
        "first_name": "Prénom",
        "birthdate": "Date de naissance",
        "elo": "Classement ELO",
        "sex": "Sexe",
        "format_date": "[Jour/Mois/Année]",
        "format_sex": "[H, F]",
    }

    def __init__(self, family_name, first_name, birthdate, sex, elo):
        self.family_name = family_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.sex = sex
        self.elo = elo
        self.score = 0
        self.games = []

    def add_game(self, opponent):
        """_Register a game in the player's history.
            We only register the opponent with its score,
            but as the sum of the game worth 1pt we can deduce
            the current player score.

        Parameters
        ----------
        opponent : list(Player, int)
            A list containing a Player instance and its game score
        """
        try:

            score = 1 - opponent[1]
            self._add_to_score(score)
            self.games.append(opponent)

        except ValueError as e:
            raise e

    def _add_to_score(self, value):
        """_Add the given value to the current player score
            if the value is 0>=value<=1

        Parameters
        ----------
        value : int
            the score value to add to the current player's score
        """

        if value < 0 or value > 1:
            raise ValueError("Le score doit être compris entre 0 et 1")

        self.score += value

    def has_played(self, player):
        """ Return True if the given Player instance is in the games history """

        return player in [game[0] for game in self.games]

    def fullname(self):
        """ Return the concatenation of the fist and family names """

        return self.first_name[0] + self.family_name[0]  # TODO TMP
        return self.first_name + " " + self.family_name

    def toJSON(self):
        """ Return a JSON representation of the Player instance """

        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __repr__(self):
        return (
            f"Player('{self.family_name}', '{self.first_name}', "
            f"'{self.birthdate}', '{self.sex}', {self.elo}, {self.score})"
        )

    @classmethod
    def get_fields_new(cls):
        """ D """

        fields = [
            {
                "name": "family_name",
                "label": cls.labels["family_name"],
                "test": "value != ''",
                "errormsg": "Vous devez saisir un nom de famille",
                "placeholder": None,
            },
            {
                "name": "first_name",
                "label": cls.labels["first_name"],
                "placeholder": None,
                "test": "value != ''",
                "errormsg": "Vous devez saisir un prénom",
            },
            {
                "name": "birthdate",
                "label": cls.labels["birthdate"] + " " + cls.labels["format_date"],
                "placeholder": "20/02/1991",
                "test": "Validation.is_valid_date(value)",
                "errormsg": "Le format demandé est JJ/MM/YYYY",
            },
            {
                "name": "elo",
                "label": cls.labels["elo"],
                "placeholder": "1000",
                "test": "Validation.is_valid_posint(value)",
                "errormsg": "Vous devez saisir un entier positif",
            },
            {
                "name": "sex",
                "label": cls.labels["sex"] + " " + cls.labels["format_sex"],
                "placeholder": None,
                "test": "Validation.is_valid_sex(value)",
                "errormsg": "Vous devez saisir l'une de ces options; H pour Homme, F pour Femme",
            },
        ]

        return fields
