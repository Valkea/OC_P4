#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to handle the tournaments
"""


class Tournament:
    """ The purpose of this class is handle the tournament processes """

    def __init__(self, name, place, dates, game_type, description, num_rounds=4):
        self.name = name
        self.place = place
        self.dates = dates
        self.num_rounds = num_rounds
        self.rounds = []
        self.players = []
        self.game_type = game_type
        self.description = description
