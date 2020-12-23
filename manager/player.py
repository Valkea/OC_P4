#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to handle the players of the tournaments
"""

import json


class Player:
    def __init__(self, family_name, first_name, birthdate, sex, elo):
        self.family_name = family_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.sex = sex
        self.elo = elo

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __repr__(self):
        return (
            f"Player({self.family_name}, {self.first_name}, "
            f"{self.birthdate}, {self.sex}, {self.elo})"
        )
