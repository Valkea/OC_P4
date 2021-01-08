#! /usr/bin/env python3
# coding: utf-8

""" This module handles the tournaments
"""

import datetime
from enum import Enum
from operator import attrgetter

from model.player import Player
from model.round import Round


class World:
    """ D """

    def __init__(self):
        self.tournaments = []
        self.active_tournament = None

    def add_tournament(
        self, name, place, start_date, end_date, gtype, desc="", rounds=4
    ):
        """ D """
        tournament = Tournament(
            name,
            place,
            start_date,
            end_date,
            gtype,
            desc,
            rounds,
        )

        self.tournaments.append(tournament)

        return tournament

    def set_active_tournament(self, tournament):
        """ D """
        self.active_tournament = tournament

    def get_active_tournament(self):
        """ D """
        return self.active_tournament

    def get_all_actors(self):
        """ D """
        all_actors = set()
        for tournament in self.tournaments:
            all_actors.union(tournament.get_actors())
            all_actors = all_actors.union(tournament.get_actors())
        return list(all_actors)


class Tournament:
    """This class handles the tournaments

    Attributes
    ----------
    name : str
        the tournament's name
    place : str
        the place where the tournament takes place
    start_date : str
        the stating date of the tournament
    end_date : str
        the ending date of the tournament
    num_rounds : int
        the number of rounds in the tournament (defaut is 4)
    rounds : list(Round)
        the registered round instances of the tournament
    players : list(Player)
        the registered player instances of the tournament
    game_type : str
        the game method used in the tournament
    description : str
        the tournament director's notes
    status : str
        the current tournament status

    Methods
    -------
    start_round()
        TODO
    current_round()
        TODO

    #set_date( str )
        insert a date using 'DD/MM/YYYY' format 'into the dates list
    #set_dates( list(str) )
        insert several dates using 'DD/MM/YYYY' format 'into the dates list
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
        "list_rounds": "Tournées",  # TODO unused
        "current_round": "Tournée actuelle",
        "desc": "Description",
        "num_players": "Nombre de joueurs",
        "list_players": "Joueurs",  # TODO unused
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
        self, name, place, start_date, end_date, game_type, description="", num_rounds=4
    ):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.num_rounds = num_rounds
        self.rounds = []
        self.players = []
        self.game_type = game_type
        self.description = description
        self.status = Status.UNINITIALIZED

    @property
    def num_rounds(self):
        return int(self._num_rounds)

    @num_rounds.setter
    def num_rounds(self, v):
        self._num_rounds = int(v)

    # -----------------------------------

    def set_results(self, game_index, score1, score2):
        """Set the game result to the appropriate Game in the current Round,
            And update the Player's score

        Parameters
        ----------
        game_index : int
            the index of the Game instance to update
        score1 : int
            the score of the first player (tuple order)
        score2 : int
            the score of the second player (tuple order)
        """

        if score1 + score2 != 1:
            raise ValueError("La somme des deux scores doit être de 1")

        game = self.current_round().games[game_index]  # persistent order
        game[0][1] = score1
        game[1][1] = score2  # TODO class game pour game.set_score(score1, score2) ?

        player1 = game[0][0]
        player1.add_game(game[1])

        player2 = game[1][0]
        player2.add_game(game[0])

    # --- Rounds --- #

    def start_round(self):
        """ Initialize and start a new round in the current tournament instance """

        if self.status == Status.UNINITIALIZED or self.status == Status.CLOSED:
            raise IsNotReady()

        if len(self.players) <= self.num_rounds:
            raise WrongPlayersNumber(
                f"Il faut au moins {self.num_rounds+1} joueurs "
                + f"pour faire un tournoi en {self.num_rounds} tours"
            )

        if self.has_player_pairs() is False:
            raise WrongPlayersNumber("Il faut un nombre pair de joueurs")

        if self.current_round() is not None:
            self.current_round().close()

        if len(self.rounds) >= self._num_rounds:
            self.status = Status.CLOSING
            raise IsComplete()

        round_index = len(self.rounds)
        new_round = Round(f"Round {round_index+1}", round_index, self.players)
        self.rounds.append(new_round)

    def current_round(self):
        """ Return the instance of the current round if any or None otherwise """

        if len(self.rounds) == 0:
            return None
        else:
            return self.rounds[-1]

    def has_player_pairs(self):
        """ Return True is the number of players is greater than 0 and multiple of 2 """

        if len(self.players) == 0 or len(self.players) % 2 == 1:
            return False
        return True

    def add_player(self, player):
        """Add a player to the current tournament instance

        Parameters
        ----------
        player : Player
            the Player instance to register as a participant of the tournament
        """

        if type(player) is not Player:
            raise TypeError("Player instance expected")

        self.players.append(player)

    # --- Properties GET & SET ----------

    def get_actors(self):
        """ D """
        return self.players

    def get_overall_infos(self):
        """ D """
        infos = {
            "name": f"{self.labels['name']}: {self.name}",
            "place": f"{self.labels['place_short']}: {self.place}",
            # "start_date": f"{self.labels['start_date']}: {self.start_date}",
            # "end_date": f"{self.labels['end_date']}: {self.end_date}",
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

        # if self.current_round() is not None:
        if self.status == Status.PLAYING:

            infos["space2"] = ""
            infos["games"] = f"{self.labels['games']}:"
            infos["space3"] = ""

            for i, game in enumerate(self.current_round().games):

                player1 = game[0][0]
                player2 = game[1][0]

                # infos[f"game_space{i}"] = ""
                # infos[f"game{i}"] = f"{self.labels['table']} #{i+1}"
                infos[f"game_details{i}"] = (
                    f"({player1.oneline(age=False, sex=False)}) vs "
                    + f"({player2.oneline(age=False, sex=False)})"
                )

        if self.status == Status.CLOSING or self.status == Status.CLOSED:

            infos["space2"] = ""
            infos["classement"] = f"{self.labels['classement']}:"
            infos["space3"] = ""

            for i, player in enumerate(
                sorted(self.players, key=attrgetter("score", "elo"), reverse=True)
            ):
                infos[f"result{i}"] = player.oneline()

        return infos

    @classmethod
    def get_fields(cls):
        """ D """

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
        """ D """

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
        """ D """

        fields = [
            {"label": f"{self.labels['input_score1']}"},
            {"label": f"{self.labels['input_score2']}"},
            {"label": ""},
        ]

        for i, game in enumerate(self.current_round().games):
            max_size = 30
            label = (
                f"{game[0][0].getFullname().ljust(max_size)[:max_size]}"
                + f"{game[1][0].getFullname().rjust(max_size)[:max_size]}"
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


class WrongPlayersNumber(Exception):
    """Tournament Exception relative to the number of players.

    Should be returned when the tournament can't
    be started because of the number of players.
    """

    pass


class IsNotReady(Exception):
    """Tournament Exception relative to the tournament status.

    Should be returned when the tournament is either not initialized or closed."""


class IsComplete(Exception):
    """Tournament Exception relative to the tournament status.

    Should be returned when the tournament has played of the rounds."""


class Status(Enum):
    """Enum reflecting the current tournament status"""

    UNINITIALIZED = 0
    INITIALIZED = 1
    PLAYING = 2
    CLOSING = 3
    CLOSED = 4
