#! /usr/bin/env python3
# coding: utf-8


""" This module handles the rounds & matchs of the tournaments
"""

import datetime
import json
from operator import attrgetter


class Round:
    """This class handles the chess players

    Attributes
    ----------
    name : str
    start_time : DateTime
        automatically added when creating the instance
    close_time : DateTime
        automatically added when calling the close method
    games : list
        the game instances of this round

    Methods
    -------
    close()
        close the current round
    toJSON()
        convert the current instance to a JSON dictionnary
    """

    def __init__(self, name, round_index, players):
        self.name = name
        self.start_time = self._get_time()
        self.close_time = None
        self.games = []
        self.index = round_index

        self.gen_games(players)

    def close(self):
        """ D """

        self.close_time = self._get_time()

    # ----------------------

    def gen_games(self, players):
        """ D """

        sorted_players = self._sort_players(players)
        # print("SORTED:", sorted_players)
        print("\n")
        for p in sorted_players:  # TODO TMP
            print(p)

        paired_players = self._get_pairs(sorted_players)
        # print("PAIRED:", paired_players)
        for p1, p2 in paired_players:
            self.games.append(([p1, 0], [p2, 0]))

    def _sort_players(self, players):
        """ D """

        if self.index == 0:
            # print("TEST SORT:", players)
            return sorted(players, key=attrgetter("elo"), reverse=True)
        else:
            return sorted(players, key=attrgetter("score", "elo"), reverse=True)

    def _get_pairs(self, players):
        """ D """

        # print("TEST PAIRS:", players)
        pairs = []
        if self.index == 0:
            half = len(players) // 2
            part1 = players[:half]
            part2 = players[half:]
            for pair in zip(part1, part2):
                pairs.append(pair)
        else:
            for i in range(0, len(players), 2):
                pairs.append((players[i], players[i + 1]))
                # TODO vérifier que les joueurs ne se sont pas déjà rencontrés

        return pairs

    def is_closed(self):
        """ D """

        return self.close_time is not None

    # ----------------------

    def toJSON(self):
        """ Return a JSON representation of the Round instance """

        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __repr__(self):
        return f"Round('{self.name}', {self.start_time}, {self.close_time})"

    def _get_time(self):
        return datetime.datetime.now()


# class Game:
#     """This class handles the games
#
#     Attributes
#     ----------
#     TODO
#
#     Methods
#     -------
#     get_tuple()
#         return the game as a tuple ([Player1, Score1],[Player2, Score2])
#     """
#
#     def __init__(self, player1, player2, score1=0, score2=0):
#         self.player_info1 = [player1, score1]
#         self.player_info2 = [player2, score2]
#
#     def get_tuple(self):
#         return (self.player_info1, self.player_info2)
#
#     def __repr__(self):
#         return str(self.get_tuple())
