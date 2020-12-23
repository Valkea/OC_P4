#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to simulate a chess tournament managment tool
"""
from manager.tournament import Tournament
from manager.player import Player
from manager.round import Round, Match


def main():

    # t01 = Tournament("Tournoi 01", "Caen", ["20/12/2020","21/12/2020"], "bullet")

    p01 = Player("Emmanuel", "Letremble", "07/02/1979", "M", 1111)
    p02 = Player("Maxime", "Marie", "24/03/1984", "M", 1800)
    print(p02)
    print(p02.toJSON())
    print(p01.toJSON())

    # r01 = Round("Round 1")
    # r01.close()
    # print(r01)


if __name__ == "__main__":
    main()
