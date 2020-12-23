#! /usr/bin/env python3
# coding: utf-8


""" The purpose of this module is to handle the rounds & matchs of the tournaments
"""


class Round:
    def __init__(self, name, start_time):
        self.name = name
        self.start_time = start_time
        self.close_time = None
        self.matchs = []


class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
