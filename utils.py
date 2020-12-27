#! /usr/bin/env python3
# coding: utf-8

""" This module provides functions to fake the tournament content
"""

import random
import datetime


def get_fake_score_from_elo(elo1, elo2):

    score1 = elo1 + random.randint(0, 500)
    score2 = elo2 + random.randint(0, 500)

    print(f"{score1}/{elo1} && {score2}/{elo2}")

    if score1 > score2:
        return [1, 0]
    elif score1 < score2:
        return [0, 1]
    else:
        return [0.5, 0.5]


def get_fake_score():

    scores = [[1, 0], [0, 1], [0.5, 0.5]]
    return random.choice(scores)


class FakePlayer:

    firstnames_M = [
        "Albert",
        "Bernard",
        "Charles",
        "Donald",
        "Emile",
        "Fred",
        "Greg",
        "Hector",
        "Isidore",
        "James",
        "Karl",
        "Laurent",
        "Marcel",
        "Nathan",
        "Olivier",
        "Paul",
        "Quentin",
        "Robert",
        "Stephane",
        "Thomas",
        "Ulysse",
        "Valentin",
        "William",
        "Xavier",
        "Yvan",
        "Zachary",
    ]

    firstnames_F = [
        "Alice",
        "Béatrice",
        "Catherine",
        "Denise",
        "Emile",
        "Fany",
        "Géraldine",
        "Henriette",
        "Iris",
        "Joséphine",
        "Katia",
        "Laurence",
        "Maude",
        "Nadia",
        "Oliane",
        "Pauline",
        "Quamar",
        "Rose",
        "Stephanie",
        "Tania",
        "Ursula",
        "Valérie",
        "Winny",
        "Xena",
        "Ysalis",
        "Zoé",
    ]

    familynames = [
        "Le belier",
        "La truelle",
        "De montout",
        "Xavier",
        "Flambard",
        "Ferdinand",
        "Galette",
        "Olivier",
        "Du moulin",
        "Basseterre",
        "Skywalker",
        "Marie",
        "Lucarne",
        "Oldman",
        "Bricoo",
        "Paulin",
        "Du carré",
    ]

    def __init__(self):
        pass

    def randdate(self):
        start_date = datetime.date(1950, 1, 1)
        end_date = datetime.date(2010, 1, 1)

        delta = end_date - start_date
        delta_days = delta.days
        random_number_of_days = random.randrange(delta_days)

        return start_date + datetime.timedelta(days=random_number_of_days)

    def gen(self, number):
        r_list = []

        for i in range(number):
            player = {}
            player["sex"] = "F" if random.random() < 0.5 else "M"
            if player["sex"] == "F":
                player["firstname"] = random.choice(self.firstnames_F)
            else:
                player["firstname"] = random.choice(self.firstnames_M)
            player["familyname"] = random.choice(self.familynames)
            player["birthdate"] = self.randdate().strftime("%d/%m/%Y")
            player["elo"] = random.randrange(1000, 2800)
            r_list.append(player)

        return r_list


# test  = fakePlayer()
# print(test.gen(4))
