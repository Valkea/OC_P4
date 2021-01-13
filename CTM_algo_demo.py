#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to simulate a chess tournament managment tool
"""

import argparse

from model.world import World
from model.tournament import Status, IsComplete
from model.player import Player
from model.round import Round
from model.tournament import Tournament

from utils import FakePlayer, get_fake_score_from_elo

FAKE_INPUTS = True


def sepa(space=True):
    if space:
        print()
    print("*" * 50)
    if space:
        print()


def main():

    global FAKE_INPUTS

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--inputs",
        action="store_true",
        help="Request to self-inputs names and results",
    )

    args = parser.parse_args()
    FAKE_INPUTS = not args.inputs

    # === Initialize Tournament with INPUTS ===
    t01 = Tournament(
        World, "Tournoi de test", "Caen", "20/12/2020", "21/12/2020", "bullet"
    )
    World.add_tournament(t01)
    World.set_active_tournament(t01)

    # === Initialize Players with INPUTS ===
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

            # === Start a new Round ===
            t01.start_round()

            sepa()
            print(f"----{t01.current_round().name}----")
            for k, info in t01.get_overall_infos().items():
                print(info)
            print("-" * 50, end="\n\n")

            games = t01.current_round().games

            # print("GAMES: ", games)
            # time.sleep(3)

            # === INPUT Round 1 results ===
            for i, g in enumerate(games):
                player1 = World.get_actor(g[0][0])
                player2 = World.get_actor(g[1][0])

                player_name1 = player1.get_fullname()
                player_name2 = player2.get_fullname()

                print(
                    f"Veuillez saisir les scores pour le match {player_name1} vs {player_name2}"
                )

                if FAKE_INPUTS:
                    score_symbol = get_fake_score_from_elo(
                        player1.elo, player2.elo, True
                    )
                    # score1 = fake_score[0]
                    # score2 = fake_score[1]
                else:
                    score_symbol = input(
                        f"{player_name1}  vs {player_name2} [ < | > | = ] :"
                    )
                    # score1 = input(f"Score pour {player_name1} :")
                    # score2 = input(f"Score pour {player_name2} :")

                # if score1 + score2 != 1:
                # print("La somme des deux scores doit être de 1")
                # continue

                print(f"Résultat: {player_name1} {score_symbol} {player_name2}")

                score1, score2 = Round.convert_score_symbol(score_symbol)

                t01.set_results(i, score1, score2)
                print(f"{player_name1} +{score1} | {player_name2} +{score2}\n")

            print("Tous les scores de match ont été saisi")
            t01.current_round().close()

            sepa()
    except IsComplete:
        desc = input("Veuillez saisir la note du directeur de tournoi : ")
        t01.description = desc

    sepa()
    for k, info in t01.get_overall_infos().items():
        print(info)


if __name__ == "__main__":
    main()
