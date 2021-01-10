#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to simulate a chess tournament managment tool
"""

# import time
from operator import attrgetter

from model.world import World
from model.tournament import Status, IsComplete
from model.player import Player

# from manager.round import Round
from utils import FakePlayer, get_fake_score

FAKE_INPUTS = True


def main():

    # ## Initialize Tournament with INPUTS ###
    t01 = World.add_tournament(
        "Tournoi 01", "Caen", "20/12/2020", "21/12/2020", "bullet"
    )
    World.set_active_tournament(t01)

    # ## Initialize Players with INPUTS ###
    num_players = 8
    fakeInputs = FakePlayer()
    fakePlayers = fakeInputs.gen(num_players)

    for i, p in enumerate(fakePlayers):
        print(f"\nVeuillez saisir les informations du joueur #{i+1}\n")

        if FAKE_INPUTS:
            family_name = p["familyname"]
            print(f"Nom de famille : {p['familyname']}")

            first_name = p["firstname"]
            print(f"Prénom : {p['firstname']}")

            birthdate = p["birthdate"]
            print(f"Date de naissance [JJ/MM/AAAA] : {p['birthdate']}")

            sex = p["sex"]
            print(f"Sexe [M / F] : {p['sex']}")

            elo = p["elo"]
            print(f"Elo [>0] : {p['elo']}")

            # time.sleep(1)
        else:
            family_name = input("Nom de famille : ")
            first_name = input("Prénom : ")
            birthdate = input("Date de naissance [JJ/MM/AAAA] : ")
            sex = input("Sexe [M / F] : ")
            elo = input("Elo [>0] : ")

        p = Player(family_name, first_name, birthdate, sex, elo)
        # t01.add_player(p)
        World.add_actor(p)

        t01.status = Status.INITIALIZED

    try:
        while True:
            # ## Get Round 1 Games ###
            t01.start_round()

            print(f"----{t01.current_round().name}----")

            games = t01.current_round().games

            # print("GAMES: ", games)
            # time.sleep(3)
            # ## INPUT Round 1 results ###
            for i, g in enumerate(games):
                player1 = World.get_actor(g[0][0])
                player2 = World.get_actor(g[1][0])

                player_name1 = player1.get_fullname()
                player_name2 = player2.get_fullname()

                print(
                    f"Veuillez saisir les scores pour le match {player_name1} vs {player_name2}"
                )

                if FAKE_INPUTS:
                    fake_score = get_fake_score()
                    score1 = fake_score[0]
                    score2 = fake_score[1]
                else:
                    score1 = input(f"Score pour {player_name1} :")
                    score2 = input(f"Score pour {player_name2} :")

                if score1 + score2 != 1:
                    print("La somme des deux scores doit être de 1")
                    continue

                t01.set_results(i, score1, score2)
                print(f"{player_name1} +{score1} | {player_name2} +{score2}\n")

            print("Tous les scores de match ont été saisi")
            t01.current_round().close()

    except IsComplete:
        desc = input("Veuillez saisir la note du directeur de tournoi : ")
        t01.description = desc

    for player in sorted(
        World.get_actors(t01), key=attrgetter("score", "elo"), reverse=True
    ):
        print(player)


if __name__ == "__main__":
    main()
