#! /usr/bin/env python3
# coding: utf-8

""" This module handles the tournaments
"""

import datetime

from model.player import Player
from model.round import Round


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
    set_date( str )
        insert a date using 'DD/MM/YYYY' format 'into the dates list
    set_dates( list(str) )
        insert several dates using 'DD/MM/YYYY' format 'into the dates list
    """

    def __init__(self, name, place, dates, game_type, description="", num_rounds=4):
        self.name = name
        self.place = place
        self.dates = dates
        self.num_rounds = num_rounds
        self.rounds = []
        self.players = []
        self.game_type = game_type
        self.description = description

    def set_date(self, date):

        self.dates.append(datetime.datetime.strptime(date, "%d/%m/%Y"))

    def set_dates(self, dates):
        for date in dates:
            self.set_date(date)

    def set_game_type(self, type):
        if type == "bullet" or type == "blitz" or type == "coup rapide":
            self.game_type = type
        else:
            raise ValueError(
                "Les contrôles de temps doivent être 'bullet',"
                "'blitz' ou 'coup rapide'"
            )

    # -----------------------------------
    def set_result(self, index, score1, score2):

        if score1 + score2 != 1:
            raise ValueError("La somme des deux scores doit être de 1")

        game = self.current_round().games[
            index
        ]  # TODO sont ils vraiment dans cet ordre ?
        game[0][1] = score1
        game[1][1] = score2  # TODO class game pour game.set_score(score1, score2) ?

        player1 = game[0][0]
        player2 = game[1][0]

        player1.add_to_score(score1)
        player2.add_to_score(score2)

    def is_complete(self):
        print("is close:", len(self.rounds), self.num_rounds)
        if self.current_round().is_closed() is not True:
            return False
        return len(self.rounds) == self.num_rounds

    # -----------------------------------

    # --- Game --- #

    #     def current_round(self):
    #         if len(self.rounds) == 0:
    #             return None
    #
    #         return self.rounds[-1]
    #
    #     def start_round(self):
    #         new_round = Round("Round {current_round+1}", round_index)
    #         self.rounds.append(new_round)
    #
    #     def close_round(self):
    #         pass
    #
    #
    #     def get_games(self):
    #
    #         round_index = len(self.rounds)
    #
    #
    #         return new_round.get_games()
    #
    #     def get_pairs(self):
    #         round_index = len(self.rounds)
    #
    #         if( round_index == 0 ):
    #             half = len(sorted_players)//2
    #             sorted_players = self.players.sort() # by elo
    #             part1 = sorted_players[:half]
    #             part2 = sorted_players[half:]
    #
    #             for i in range(half):
    #                 new_game = Game(part1[i], part2[i])
    #         else:
    #             sorted_players = self.players.sort() # by score & elo
    #

    #     def sorted_by_elo(self, layers):
    #         pass
    #
    #     def sorted_by_score(self):
    #         return self.players.sort()
    #
    #     def get_round1_games(self):
    #         pass
    #
    #     def get_round_games(self):
    #         pass

    # --- Rounds --- #

    def start_round(self):
        round_index = len(self.rounds)
        new_round = Round(f"Round{round_index+1}", round_index, self.players)
        self.rounds.append(new_round)

    def current_round(self):
        if len(self.rounds) == 0:
            return
        else:
            return self.rounds[-1]

    def close_round(self):
        self.current_round.close()

    # --- Players --- #
    def add_player(self, player):
        if type(player) is not Player:
            raise TypeError("Player instance expected")

        self.players.append(player)
