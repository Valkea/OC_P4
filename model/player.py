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
    """This class handles the chess players.

    Attributes
    ----------
    family_name : str
    first_name : str
    birthdate : str
        Must be a 'DD/MM/YYYY' str
    sex : str
        Should be either 'M' or 'F'
    elo : int
        Current 'classement' of the player
    score : int
        Total points earned by the player
    played_actors : set(int)
        Opponent's id the player has already played
    uid : str
        A unique universal identifier to share with other classes

    Getters & Setters
    -----------------
    birthdate(self)
        Return the _birthdate datetime.datetime as a str
    birthdate(self, v)
        Convert various date inputs to a datetime.datetime object stored in _birthdate.
    age(self)
        Return the age based on the _birthdate
    sex(self)
        Return _sex
    sex(self, v)
        Ensure the sex is saved as a single CAP letter (the first one of the provided str)
    elo()
        Return the current ELO as an int
    elo(v)
        Ensure the elo is saved as an int

    Public Methods
    --------------
    add_to_score(value)
        Add to the current player's total score (game scores are stored in the Round/game instances)
    set_played(player_id)
        Record an opponant id in the list of the opponent already met
    has_played(player_id)
        Check if the provided opponant has already played with the current Player
    get_fullname()
        Return a composition based on the family_name and the first_name
    one_line(ljustv=20, age=True, sex=True, elo=True, score=True, extra=False)
        Return a complete presentation of the player in one line
    serialize()
        Serialize the content of this class for TinyDB exports

    Private Methods
    ---------------
    _gen_UID()
        Generate a unique universal identifier

    Static & Class Methods
    ----------------------
    get_fields(cls)
        Return the fields requiered to input or edit any player instance
    get_sort_key(sortby)
        Return an orderering sequence based on a sortby paramater
    multisort(xs, specs)
        Sort a given container based on the given order sequence (get_sort_key)
    select_actor(sortby, world)
        Return tuples containing the available players
        and the appropriate controller methods to call in order to 'open' them
    list_actors(tournament, world, sortby)
        Return a sorted tuples containing the available players in the provided tournament
    list_all_actors(world, sortby)
        Return a sorted tuples containing the available players in the whole app
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
        self.played_actors = set()
        self.uid = uid if uid is not None else self._gen_UID()

    # --- GETTERS & SETTERS ---

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

    @property
    def elo(self):
        return int(self._elo)

    @elo.setter
    def elo(self, v):
        self._elo = int(v)

    # --- PUBLIC METHODS ---

    def add_to_score(self, value):
        """Add the given value to the current player's total score.

        Game scores are stored in the Round/game instances, not in Player's instances.

        Parameters
        ----------
        value : int
            the score to add to the current player's score

        Raises
        ------
        ValueError
            if the value is not >= 0 and <= 1
        """

        if value < 0 or value > 1:
            raise ValueError("Le score doit être compris entre 0 et 1")

        self.score += value

    def set_played(self, player_id):
        """Record an opponant id in the list of the opponent already met.

        Parameters
        ----------
        player_id : str
            The uid attribute of the opponent Player's instance met
        """

        self.played_actors.add(player_id)

    def has_played(self, player_id):
        """Return True if the given Player instance is in the games history.

        Parameters
        ----------
        player_id : str
            The uid attribute of the opponent Player's instance potentially met
        """

        return player_id in self.played_actors

    def get_fullname(self):
        """ Return the concatenation of the fist and family names. """

        return f"{self.family_name} {self.first_name}".title()

    def one_line(
        self, ljustv=20, age=True, sex=True, elo=True, score=True, extra=False
    ):
        """Return a full resume of the actor in one line.

        Parameters
        ----------
        ljustv : int(20)
            The minimum of space taken by the family_name + first_name (ensure alignement)
        age : bool(True)
            Should the line include age attribute ?
        sex : bool(True)
            Should the line include sex attribute ?
        elo : bool(True)
            Should the line include ELO attribute ?
        score : bool(True)
            Should the line include score attribute ?
        extra : bool(False)
            Should the line include exta attributes ?
        """

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

    # --- PRIVATE METHODS ---

    def _gen_UID(self):
        """ Generate a unique universal identifier. """

        # return id(self)
        return uuid.uuid1().hex

    # def __repr__(self):
    #     return (
    #         f"Player('{self.family_name}', '{self.first_name}', "
    #         f"'{self._birthdate}', '{self.sex}', {self.elo}, {self.score})"
    #     )

    # def __dict__(self):
    #     retv = {
    #         "family_name": self.family_name,
    #         "first_name": self.first_name,
    #         "sex": self.sex,
    #         "birthdate": self.birthdate,
    #         "elo": self.elo,
    #         "score": self.score,
    #     }
    #     return retv

    # --- STATIC & CLASS METHODS ---

    @classmethod
    def get_fields(cls):
        """ Return the fields requiered to input or edit any player instance. """

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
        """Return an orderering sequence based on a sortby paramater.

        Parameters
        ----------
        sortby : str
            A string indicating the ordering sequence expected in return
        """

        if sortby is None:
            sortby = "alpha"

        if sortby == "alpha":
            return (
                ("family_name", False),
                ("first_name", False),
                ("elo", False),
                ("score", False),
            )
        elif sortby == "elo":
            return (
                ("elo", True),
                ("score", True),
                ("family_name", True),
                ("first_name", True),
            )
        elif sortby == "score":
            return (
                ("score", True),
                ("elo", True),
                ("family_name", True),
                ("first_name", True),
            )
        elif sortby == "age":
            return (("age", True), ("family_name", True), ("first_name", True))
        elif sortby == "sex":
            return (("sex", False), ("family_name", False), ("first_name", False))

    @staticmethod
    def multisort(container, seqsort):
        """Sort a given container based on the given order sequence (get_sort_key).

        Parameters
        ---------
        container : any container
            The list/tuple etc to sort
        seqsort : tuple(tuple('field_name', reversed_bool))
            A sequence of sorting actions to apply to the container
        """

        for key, reverse in reversed(seqsort):
            container.sort(key=attrgetter(key), reverse=reverse)
        return container

    # --- Generate list for Curses views ---

    @staticmethod
    def select_actor(sortby, world):
        """Return tuples containing the available players and the
        appropriate controller methods to call in order to 'open' them.

        Parameters
        ----------
        sortby : str
            A string indicating the sorting sequence to use
        world : World
            the world instance containing all tournament's and player's instances.
        """

        actors = Player.multisort(world.get_actors(), Player.get_sort_key(sortby))

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
        """Return sorted tuples containing the available players in the provided tournament.

        Parameters
        ----------
        tournament: Tournament
            The instance of the tournament
        world : World
            the world instance containing all tournament's and player's instances
        sortby : str
            A string indicating the sorting sequence to use
        """

        actors = Player.multisort(world.get_actors(), Player.get_sort_key(sortby))

        if len(actors) > 0:
            retv = [(f" {actor.one_line()} ", None) for actor in actors]
            return tuple(retv)
        else:
            return (("Aucun acteur", "go_back"),)

    @staticmethod
    def list_all_actors(world, sortby):
        """Return a sorted tuples containing the available players in the whole app.

        Parameters
        ----------
        world : World
            the world instance containing all tournament's and player's instances
        sortby : str
            A string indicating the sorting sequence to use
        """

        actors = Player.multisort(world.get_actors(), Player.get_sort_key(sortby))

        if len(actors) > 0:
            retv = [(f" {actor.one_line()} ", None) for actor in actors]
            return tuple(retv)
        else:
            return (("Aucun acteur", "go_back"),)
