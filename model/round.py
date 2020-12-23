#! /usr/bin/env python3
# coding: utf-8


""" This module handles the rounds & matchs of the tournaments
"""

import datetime
import json


class Round:
    """This class handles the chess players

    Attributes
    ----------
    name : str
    start_time : DateTime
        automatically added when creating the instance
    close_time : DateTime
        automatically added when calling the close method
    matchs : list
        the match instances of this round

    Methods
    -------
    close()
        close the current round
    toJSON()
        convert the current instance to a JSON dictionnary
    """

    def __init__(self, name):
        self.name = name
        self.start_time = self._get_time()
        self.close_time = None
        self.matchs = []

    def close(self):
        self.close_time = self._get_time()

    # def is_closed(self):
    #    return self.close_time is not None

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __repr__(self):
        return f"Round('{self.name}', {self.start_time}, {self.close_time})"

    def _get_time(self):
        return datetime.datetime.now()


class Match:
    """This class handles the matches

    Attributes
    ----------
    player1 : list
        automatically added when creating the instance
    close_time : DateTime
        automatically added when calling the close method
    matchs : list
        the match instances of this round

    Methods
    -------
    get_tuple()
        return the match as a tuple ([Player1, Score1],[Player2, Score2])
    """
    def __init__(self, player1, player2, score1=0, score2=0):
        self.player_info1 = [player1, score1]
        self.player_info2 = [player2, score2]

    def get_tuple(self):
        return (self.player_info1, self.player_info2)

    def __repr__(self):
        return str(self.get_tuple())
