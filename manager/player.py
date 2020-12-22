#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to handle the players of the tournaments
"""


class Player:
    def __init__(self, family_name, first_name, birthdate, sex, elo):
        self.family_name = family_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.sex = sex
        self.elo = elo
