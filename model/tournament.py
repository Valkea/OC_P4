#! /usr/bin/env python3
# coding: utf-8

""" This module handles the tournaments """

import datetime
from enum import Enum
from operator import attrgetter
import json
import logging

from model.round import Round


class Status(Enum):
    """Enum reflecting the current tournament status"""

    UNINITIALIZED = 0
    INITIALIZED = 1
    PLAYING = 2
    CLOSING = 3
    CLOSED = 4


class Tournament:
    """This class handles the tournament instances.

    Attributes
    ----------
    name : str
        The tournament's name
    place : str
        The place where the tournament takes place
    start_date : str
        The stating date of the tournament
    end_date : str
        The ending date of the tournament
    num_rounds : int
        The number of rounds in the tournament (defaut is 4)
    rounds : list(Round)
        The registered round instances of the tournament
    players : list(int)
        The registered player instances id of the tournament
    game_type : str
        The game method used in the tournament
    description : str
        The tournament director's notes
    status : Status
        The current tournament status
    world : Wold
        The world instance where the original players instances can be found

    Getters & Setters
    -----------------
    num_rounds()
        Return num_rounds as int for comparisons
    num_rounds(v)
        Set num_rounds to int (because Curses return str from input fields)

    Public Methods
    --------------
    start_round()
        Start a new round
    set_results(game_index, score1, score2)
        Set the given results in the appropriate game and players instances

    add_player(player_id)
        Register the given player_id as a participant of the tournament

    current_round()
        Return the current round instance
    serialize()
        Serialize the content of this class for TinyDB exports

    Private Methods
    ---------------
    _reload_data()
        Reshape exported ENUMS and exorted list of objects when the class is feed with JSON data
    _has_right_players_num()
        Check if the tournament has the right number of players to start the tournament

    Static & Class Methods
    ----------------------
    get_overall_infos()
        Return informations about this specific tournament instance
    get_fields(cls)
        Return the fields requiered to input or edit any tournament instance
    get_fields_final_note(cls)
        Return the field required to input or edit the 'final note' of any tournament instance
    get_fields_input_scores(self)
        Return the fields required to input the round/games results

    select_tournament_load(world)
        Return tuples containing the available tournaments
        and the appropriate controller methods to call in order to 'open' them
    select_tournament_report(world, route)
        Return tuples containing the available tournaments
        and the appropriate controller methods to call to get the right report
    """

    labels = {
        "name": "Nom du tournoi",
        "place": "Lieu du tournoi",
        "place_short": "Lieu",
        "dates": "Date(s)",
        "start_date": "Date de début",
        "end_date": "Date de fin",
        "num_rounds": "Nombre de tours",
        "gtype": "Contrôle du temps",
        "list_rounds": "Tournées",  # unused
        "current_round": "Tournée actuelle",
        "desc": "Description",
        "num_players": "Nombre de joueurs",
        "list_players": "Joueurs",  # unused
        "table": "Table",
        "unstarted": "Pas commencé",
        "format_date": "[Jour/Mois/Année]",
        "format_gtype": "[Bullet, Blitz, Coup rapide]",
        "final_note": "[remarques générales du directeur du tournoi]",
        "input_score1": "Utilisez < ou > pour indiquer le gagnant",
        "input_score2": "         = en cas d'égalité",
        "games": "Matchs de ce round",
        "classement": "Classement",
    }

    def __init__(
        self,
        world,
        name,
        place,
        start_date,
        end_date,
        game_type,
        description="",
        num_rounds=4,
        rounds=None,
        players=None,
        status=Status.UNINITIALIZED,
    ):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.num_rounds = num_rounds
        self.rounds = rounds if rounds is not None else []
        self.players = players if players is not None else []
        self.game_type = game_type
        self.description = description
        self.status = status
        self._world = world

        if self.status != Status.UNINITIALIZED:
            self._reload_data()

    # --- GETTERS & SETTERS ---

    @property
    def num_rounds(self):
        return int(self._num_rounds)

    @num_rounds.setter
    def num_rounds(self, v):
        self._num_rounds = int(v)

    # === PUBLIC METHODS ===

    def start_round(self):
        """Initialize and start a new round in the current tournament instance.

        Raises
        ------
        WrongPlayersNumber
            if the number of players is odd or if there is not enough players
            to play all the tournament rounds with the swiss rules.
        IsNotReady
            if the tournament is not initialized yet or already closed.
        """

        if self.status == Status.UNINITIALIZED:
            raise IsNotReady()

        if self.status == Status.CLOSED or self.status == Status.CLOSING:
            raise IsComplete()

        if len(self.players) <= self.num_rounds:
            raise WrongPlayersNumber(
                f"Il faut au moins {self.num_rounds+1} joueurs "
                + f"pour faire un tournoi en {self.num_rounds} tours"
            )

        if self._has_right_players_num() is False:
            raise WrongPlayersNumber("Il faut un nombre pair de joueurs")

        if self.current_round() is not None:
            self.current_round().close()

        if len(self.rounds) >= self._num_rounds:
            self.status = Status.CLOSING
            raise IsComplete()

        round_index = len(self.rounds)
        new_round = Round(
            self._world, f"Round {round_index+1}", round_index, self.players
        )
        self.rounds.append(new_round)

    def set_results(self, game_index, score1, score2):
        """Set the game result to the appropriate game and players instances.

        Parameters
        ----------
        game_index : int
            the index of the games tuple entry to update.
        score1 : int
            the score of the first player (tuple order).
        score2 : int
            the score of the second player (tuple order).
        """

        if score1 + score2 != 1:
            raise ValueError("La somme des deux scores doit être de 1")

        game = self.current_round().games[game_index]  # persistent order
        game[0][1] = score1
        game[1][1] = score2

        player1 = self._world.get_actor(game[0][0])
        player1.add_to_score(score1)
        player1.set_played(game[1][0])

        player2 = self._world.get_actor(game[1][0])
        player2.add_to_score(score2)
        player2.set_played(game[0][0])

    # --- players ---

    def add_player(self, player_id):
        """Register a player to the tounement.

        Parameters
        ----------
        player_id : int
            the Player's instance ID to register as a participant of the tournament
        """

        if type(player_id) != str:
            raise TypeError("str UID required")

        self.players.append(player_id)

    # --- utils ---

    def current_round(self):
        """ Return the instance of the current round if any or None otherwise. """

        if len(self.rounds) == 0:
            return None
        else:
            return self.rounds[-1]

    def serialize(self):
        """ Serialize the content of the tournement instance for TinyDB exports. """

        data = {
            # "id": self.uid,
            "name": self.name,
            "place": self.place,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "num_rounds": self.num_rounds,
            "rounds": [json.loads(json.dumps(x.serialize())) for x in self.rounds],
            "players": self.players,
            "game_type": self.game_type,
            "description": self.description,
            "status": self.status,
        }

        return json.loads(json.dumps(data, cls=EnumEncoder))

    # === PRIVATE METHODS ===

    def _reload_data(self):
        """ Reshape exported ENUMS and exorted list of objects when the class is feed with JSON data. """

        self.rounds = [
            Round(self._world, **x, players_id=self.players) for x in self.rounds
        ]
        name, member = self.status["__enum__"].split(".")
        self.status = getattr(PUBLIC_ENUMS[name], member)

    def _has_right_players_num(self):
        """ Return True if the number of players is greater than 0 and multiple of 2 """

        if len(self.players) == 0 or len(self.players) % 2 == 1:
            return False
        return True

    # === STATIC & CLASS METHODS ===

    def get_overall_infos(self):
        """ Return informations about this specific tournament instance. """

        infos = {
            "name": f"{self.labels['name']}: {self.name}",
            "place": f"{self.labels['place_short']}: {self.place}",
            "dates": f"{self.labels['dates']}: du {self.start_date} au {self.end_date}",
            "num_rounds": f"{self.labels['num_rounds']}: {self.num_rounds}",
            "game_type": f"{self.labels['gtype']}: {self.game_type}",
            "desc": f"{self.labels['desc']}: {self.description}",
            "space": "",
            "num_players": f"{self.labels['num_players']}: {len(self.players)}",
        }

        if len(self.rounds) > 0:
            infos[
                "current_round"
            ] = f"{self.labels['current_round']}: {len(self.rounds)}/{self.num_rounds}"
        else:
            infos["current_round"] = f"{self.labels['unstarted']}"

        if self.status == Status.PLAYING:

            infos["space2"] = ""
            infos["games"] = f"{self.labels['games']}:"
            infos["space3"] = ""

            for i, game in enumerate(self.current_round().games):

                player1 = self._world.get_actor(game[0][0])
                player2 = self._world.get_actor(game[1][0])

                infos[f"game_details{i}"] = (
                    f"({player1.one_line(age=False, sex=False)}) vs "
                    + f"({player2.one_line(age=False, sex=False)})"
                )

        if self.status == Status.CLOSING or self.status == Status.CLOSED:

            infos["space2"] = ""
            infos["classement"] = f"{self.labels['classement']}:"
            infos["space3"] = ""

            for i, player in enumerate(
                sorted(
                    self._world.get_actors(self),
                    key=attrgetter("score", "elo"),
                    reverse=True,
                )
            ):
                infos[f"result{i}"] = player.one_line()

        return infos

    # --- Generate list for Curses forms ---

    @classmethod
    def get_fields(cls):
        """ Return the fields requiered to input or edit any tournament instance. """

        fields = [
            {
                "name": "name",
                "label": cls.labels["name"],
                "test": "value != ''",
                "errormsg": "Vous devez saisir un nom",
                "placeholder": None,
            },
            {
                "name": "place",
                "label": cls.labels["place"],
                "placeholder": None,
                "test": "value != ''",
                "errormsg": "Vous devez saisir un lieu",
            },
            {
                "name": "start_date",
                "label": cls.labels["start_date"] + " " + cls.labels["format_date"],
                "placeholder": datetime.datetime.now().strftime("%d/%m/%Y"),
                "test": "Validation.is_valid_date(value)",
                "errormsg": "Le format demandé est JJ/MM/YYYY",
            },
            {
                "name": "end_date",
                "label": cls.labels["end_date"] + " " + cls.labels["format_date"],
                "placeholder": datetime.datetime.now().strftime("%d/%m/%Y"),
                "test": "Validation.is_valid_date(value)",
                "errormsg": "Le format demandé est JJ/MM/YYYY",
            },
            {
                "name": "num_rounds",
                "label": cls.labels["num_rounds"],
                "placeholder": "4",
                "test": "Validation.is_valid_posint(value)",
                "errormsg": "Vous devez saisir un entier positif",
            },
            {
                "name": "game_type",
                "label": cls.labels["gtype"] + " " + cls.labels["format_gtype"],
                "placeholder": "Bullet",
                "test": "Validation.is_valid_gtype(value)",
                "errormsg": "Vous devez saisir l'une de ces options Bullet, Blitz, Coups rapides",
            },
            {
                "name": "description",
                "label": cls.labels["desc"],
                "placeholder": None,
                "test": None,
                "errormsg": None,
            },
        ]

        return fields

    @classmethod
    def get_fields_final_note(cls):
        """ Return the field required to input or edit the 'final note' of any tournament instance. """

        fields = [
            {
                "name": "description",
                "label": f"{cls.labels['desc']} {cls.labels['final_note']}",
                "placeholder": None,
                "test": None,
                "errormsg": None,
            },
        ]

        return fields

    def get_fields_input_scores(self):
        """ Return the fields required to input the round/games results. """

        fields = [
            {"label": f"{self.labels['input_score1']}"},
            {"label": f"{self.labels['input_score2']}"},
            {"label": ""},
        ]

        for i, game in enumerate(self.current_round().games):
            max_size = 30
            player1 = self._world.get_actor(game[0][0])
            player2 = self._world.get_actor(game[1][0])
            label = (
                f"{player1.get_fullname().ljust(max_size)[:max_size]}"
                + f"{player2.get_fullname().rjust(max_size)[:max_size]}"
            )
            fields.append(
                {
                    "name": f"game{i}",
                    "label": label,
                    "placeholder": None,
                    "test": "Validation.is_valid_score_symbol(value)",
                    "errormsg": "Indiquez le résultat à l'aide des symboles <, > ou =",
                    "size": 4,
                    "same_row": True,
                },
            )

        return fields

    # --- Generate list for Curses views ---

    @staticmethod
    def select_tournament_load(world):
        """Return tuples containing the available tournaments and
        the appropriate controller methods to call in order to 'open' it.

        Parameters
        ----------
        world : World
            the world instance containing all tournament's and player's instances
        """

        tournaments = world.tournaments
        for t in tournaments:
            logging.debug(t.serialize())
        if len(tournaments) > 0:
            retv = [(f"{t.name}", "open_tournament_current", t) for t in tournaments]
            return tuple(retv)
        else:
            return (("Aucun tournoi", "go_back"),)

    @staticmethod
    def select_tournament_report(world, route):
        """Return tuples containing the available tournaments and
        the appropriate controller methods to call to get the right report.

        Parameters
        ----------
        world : World
            the world instance containing all tournament's and player's instances.
        route : str
            the controller's method to join to the tournament instances.
        """

        if route == "actors":
            link = "open_report_tournament_actors"
        elif route == "rounds":
            link = "open_report_tournament_rounds"
        elif route == "matchs":
            link = "open_report_tournament_matchs"

        tournaments = world.tournaments
        if len(tournaments) > 0:
            retv = [(f"{t.name}", link, t) for t in tournaments]
            return tuple(retv)
        else:
            return (("Aucun tournoi", "go_back"),)


# === Tournament ERRORS ===


class WrongPlayersNumber(Exception):
    """Tournament Exception relative to the number of players.

    Should be returned when the tournament can't
    be started because of the number of players.
    """

    pass


class IsNotReady(Exception):
    """Tournament Exception relative to the tournament status.

    Should be returned when the tournament is either not initialized or closed."""

    pass


class IsComplete(Exception):
    """Tournament Exception relative to the tournament status.

    Should be returned when the tournament has played of the rounds."""

    pass


# === ENUMS serialization ===

PUBLIC_ENUMS = {"Status": Status}


class EnumEncoder(json.JSONEncoder):
    """ Convert the ENUMS to a serializable format """

    def default(self, obj):
        if type(obj) in PUBLIC_ENUMS.values():
            return {"__enum__": str(obj)}
        return json.JSONEncoder.default(self, obj)


def as_enum(d):
    """ Revert ENUMS back to their origina format """
    if "__enum__" in d:
        name, member = d["__enum__"].split(".")
        return getattr(PUBLIC_ENUMS[name], member)
    else:
        return d
