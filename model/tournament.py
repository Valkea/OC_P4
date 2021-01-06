#! /usr/bin/env python3
# coding: utf-8

""" This module handles the tournaments
"""

import datetime
import logging

from model.player import Player
from model.round import Round


class World:
    """ D """

    def __init__(self):
        self.tournaments = []
        self.active_tournament = None

    def add_tournament(self, name, place, dates, gtype, desc="", rounds=4):
        """ D """
        tournament = Tournament(
            name,
            place,
            dates,
            gtype,
            desc,
            rounds,
        )

        self.tournaments.append(tournament)

        return tournament

    def set_active_tournament(self, tournament):
        self.active_tournament = tournament

    def get_active_tournament(self):
        return self.active_tournament


class Tournament:
    """This class handles the tournaments

    Attributes
    ----------
    name : str
        the tournament's name
    place : str
        the place where the tournament takes place
    dates : list(Datetime)
        the dates when the tournament takes place
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

    Methods
    -------
    start_round()
        TODO
    current_round()
        TODO

    set_date( str )
        insert a date using 'DD/MM/YYYY' format 'into the dates list
    set_dates( list(str) )
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
        "desc": "Description",
        "num_players": "Nombre de joueurs",
        "list_players": "Joueurs",  # TODO unused
        "unstarted": "Pas commencé",
        "format_date": "[Jour/Mois/Année]",
        "format_gtype": "[Bullet, Blitz, Coup rapide]",
    }

    def __init__(self, name, place, dates, game_type, description="", num_rounds=4):
        logging.debug(
            f"SELF:1>{name}< 2>{place}< 3>{dates}< 4>{num_rounds}< 5>{game_type}< 6>{description}<"
        )
        self.name = name
        self.place = place
        self.dates = dates
        self.num_rounds = num_rounds
        self.rounds = []
        self.players = []
        self.game_type = game_type
        self.description = description

    # -----------------------------------

    def set_result(self, game_index, score1, score2):
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

        game = self.current_round().games[
            game_index
        ]  # TODO sont ils vraiment dans cet ordre ?
        game[0][1] = score1
        game[1][1] = score2  # TODO class game pour game.set_score(score1, score2) ?

        player1 = game[0][0]
        player2 = game[1][0]

        # player1.add_to_score(score1)
        # player2.add_to_score(score2)

        player1.add_game(game[1])
        player2.add_game(game[0])

    def is_complete(self):
        """ Return True if self.rounds has been played """

        if self.current_round().is_closed() is not True:
            return False
        return len(self.rounds) == self.num_rounds

    # --- Rounds --- #

    def start_round(self):
        """ Initialize and start a new round in the current tournament instance """

        round_index = len(self.rounds)
        new_round = Round(f"Round{round_index+1}", round_index, self.players)
        self.rounds.append(new_round)

    def current_round(self):
        """ Return the instance of the current round if any or None otherwise """

        if len(self.rounds) == 0:
            return None
        else:
            return self.rounds[-1]

    def close_round(self):
        """ Make all actions required to close the current round of the tournament """

        self.current_round.close()

    # --- Players --- #
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

    def set_date(self, date):
        """ D """

        self.dates.append(datetime.datetime.strptime(date, "%d/%m/%Y"))

    def set_dates(self, dates):
        """ D """

        for date in dates:
            self.set_date(date)

    def set_game_type(self, type):
        """ D """

        if type == "bullet" or type == "blitz" or type == "coup rapide":
            self.game_type = type
        else:
            raise ValueError(
                "Les contrôles de temps doivent être 'bullet',"
                "'blitz' ou 'coup rapide'"
            )

    def get_actors(self):
        """ D """
        return self.players

    def get_overall_infos(self):
        """ D """
        infos = {
            "name": f"{self.labels['name']}: {self.name}",
            "place": f"{self.labels['place_short']}: {self.place}",
            "dates": f"{self.labels['dates']}: {' - '.join(self.dates)}",
            "num_rounds": f"{self.labels['num_rounds']}: {self.num_rounds}",
            "game_type": f"{self.labels['gtype']}: {self.game_type}",
            "desc": f"{self.labels['desc']}: {self.description}",
            "num_players": f"{self.labels['num_players']}: {len(self.players)}",
        }

        if len(self.rounds) > 0:
            infos[
                "current_round"
            ] = f"{self.current_round().name}: {len(self.rounds)}/{self.num_rounds}"
        else:
            infos["current_round"] = f"{self.labels['unstarted']}"

        if self.current_round() is not None:
            logging.critical(f"Coucou {type(self.current_round())}")
            for i, game in enumerate(self.current_round().get_current_games()):
                infos[f"game{i}"] = (
                    f"Table {i+1} : {game[0][0].fullname()} "
                    f"[{game[0][0].elo}] vs {game[1][0].fullname() [{game[1][0].elo}]}"
                )

        return infos

    @classmethod
    def get_fields_new(cls):
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
                "name": "rounds",
                "label": cls.labels["num_rounds"],
                "placeholder": "4",
                "test": "Validation.is_valid_posint(value)",
                "errormsg": "Vous devez saisir un entier positif",
            },
            {
                "name": "gtype",
                "label": cls.labels["gtype"] + " " + cls.labels["format_gtype"],
                "placeholder": "Bullet",
                "test": "Validation.is_valid_gtype(value)",
                "errormsg": "Vous devez saisir l'une de ces options Bullet, Blitz, Coups rapides",
            },
            {
                "name": "desc",
                "label": cls.labels["desc"],
                "placeholder": None,
                "test": None,
                "errormsg": None,
            },
        ]

        return fields
