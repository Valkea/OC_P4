#! /usr/bin/env python3
# coding: utf-8

""" This module handles the actors of the tournaments
"""

import datetime
import re
import math
import uuid

from operator import attrgetter


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
    get_fullname()
        return a concatenation of the first and family names
    serialize()
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

    def __init__(
        self,
        family_name,
        first_name,
        birthdate,
        sex,
        elo,
        score=0,
        games=None,
        uid=None,
    ):
        self.family_name = family_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.sex = sex
        self.elo = elo
        self.score = score
        # self.games = games if games is not None else []
        self.played_actors = set()
        self.uid = uid if uid is not None else self._gen_UID()

    def _gen_UID(self):
        # return id(self)
        return uuid.uuid1().hex

    @property
    def birthdate(self):
        return self._birthdate.strftime("%d/%m/%Y")

    @birthdate.setter
    def birthdate(self, v):
        s = re.search("^([0-9]{1,2})[-/. ]([0-9]{1,2})[-/. ]([0-9]{2,4})$", v).groups()
        self._birthdate = datetime.datetime(int(s[2]), int(s[1]), int(s[0]))

    @property
    def age(self):
        """ Return the current age of the actor in years """
        now = datetime.datetime.now()
        delta = now - self._birthdate
        return math.floor(delta.days / 365.2425)

    @property
    def sex(self):
        """ Return the sex of the actor as F or H """
        return self._sex

    @sex.setter
    def sex(self, v):
        self._sex = v[0:1].capitalize()

    def add_to_score(self, value):
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

    def has_played(self, player_id):
        """ Return True if the given Player instance is in the games history """

        return player_id in self.played_actors

    def set_played(self, player_id):
        """ D """

        self.played_actors.add(player_id)

    def get_fullname(self):
        """ Return the concatenation of the fist and family names """

        return f"{self.family_name} {self.first_name}".title()

    def one_line(
        self, ljustv=20, age=True, sex=True, elo=True, score=True, extra=False
    ):
        """ Return a full resume of the actor in one line """

        retv = []
        retv.append(self.get_fullname().ljust(ljustv)[:ljustv])
        if age:
            retv.append(f"{self.age:2} ans")
        if sex:
            retv.append(self.sex)
        if elo:
            retv.append(f"ELO:{int(self.elo):4}")
        if score:
            retv.append(f"PTS:{self.score:3}")
        if extra:
            retv.append(extra)

        return "|".join(retv)

    def serialize(self):
        """ Return a JSON representation of the Player instance """
        return {
            "uid": self.uid,
            "family_name": self.family_name,
            "first_name": self.first_name,
            "birthdate": self.birthdate,
            "sex": self.sex,
            "elo": self.elo,
            "score": self.score,
            # "games": self.games,
        }

    def __repr__(self):
        return (
            f"Player('{self.family_name}', '{self.first_name}', "
            f"'{self._birthdate}', '{self.sex}', {self.elo}, {self.score})"
        )

    def __dict__(self):
        retv = {
            "family_name": self.family_name,
            "first_name": self.first_name,
            "sex": self.sex,
            "birthdate": self.birthdate,
            "elo": self.elo,
            "score": self.score,
        }
        return retv

    @classmethod
    def get_fields(cls):
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

    @staticmethod
    def get_sort_key(sortby):
        if sortby is None:
            sortby = "alpha"

        if sortby == "alpha":
            return (attrgetter("family_name", "first_name", "elo", "score"), False)
        elif sortby == "elo":
            return (attrgetter("elo", "score", "family_name", "first_name"), True)
        elif sortby == "score":
            return (attrgetter("score", "elo", "family_name", "first_name"), True)
        elif sortby == "age":
            return (attrgetter("age", "family_name", "first_name"), True)
        elif sortby == "sex":
            return (attrgetter("sex", "family_name", "first_name"), False)

    # --- Generate list for Curses views ---

    @staticmethod
    def select_actor(sortby, world):

        sortTuple = Player.get_sort_key(sortby)
        actors = sorted(world.get_actors(), key=sortTuple[0], reverse=sortTuple[1])

        if len(actors) > 0:
            retv = [
                (f" {actor.one_line()} ", "open_input_actor_edit", actor)
                for actor in actors
            ]
            return tuple(retv)
        else:
            return (("Aucun acteur", "go_back"),)

    @staticmethod
    def list_actors(tournament, world, sortby):

        sortTuple = Player.get_sort_key(sortby)
        actors = sorted(
            world.get_actors(tournament), key=sortTuple[0], reverse=sortTuple[1]
        )

        if len(actors) > 0:
            retv = [(f" {actor.one_line()} ", None) for actor in actors]
            return tuple(retv)
        else:
            return (("Aucun acteur", "go_back"),)

    @staticmethod
    def list_all_actors(world, sortby):

        sortTuple = Player.get_sort_key(sortby)
        actors = sorted(world.get_all_actors(), key=sortTuple[0], reverse=sortTuple[1])

        if len(actors) > 0:
            retv = [(f" {actor.one_line()} ", None) for actor in actors]
            return tuple(retv)
        else:
            return (("Aucun acteur", "go_back"),)
