#! /usr/bin/env python3
# coding: utf-8

""" This module handles the tournaments
"""

import datetime


class Tournament:
    """This class handles the tournaments

    Attributes
    ----------
    name : str
    place : str
    dates : list(Datetime)
    num_rounds : int (default is 4)
    rounds : list(Round)
    players : list(Player)
    game_type : str
    description : str

    Methods
    -------
    set_date( str )
        insert a date using 'DD/MM/YYYY' format 'into the dates list
    set_dates( list(str) )
        insert several dates using 'DD/MM/YYYY' format 'into the dates list


    """

    def __init__(self, name, place, dates, game_type, description, num_rounds=4):
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
