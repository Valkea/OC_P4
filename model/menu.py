#! /usr/bin/env python3
# coding: utf-8

""" This module handles the menu model
"""

from model.world import World
from model.player import Player
import logging


class Menu:
    """ TODO """

    def __init__(self):
        pass

    def base(self):
        return (
            ("Créer un nouveau tournoi", "open_input_tournament_new"),
            ("Charger un tournoi", "open_select_tournament_load"),
            ("Rapports", "open_reports", "base"),
            ("Charger / Sauvegarder", "open_load_save"),
            ("Quitter", "quit_confirm"),
        )

    def quit_confirm(self):
        return (
            ("Sauvegarder & quitter", "save_quit"),
            ("Quitter sans sauver", "quit"),
        )

    def iofile(self):
        return (
            ("Sauvegarder", "open_save"),  # R1
            ("Charger les données", "open_load"),
            ("<< RETOUR", "goback"),
        )

    # --- Tournament ---

    def tournament_initialize(self):
        return (
            ("Ajouter un joueur au tournoi", "open_input_actor_new"),
            ("Modifier un acteur", "open_select_actor"),
            ("Modifier le tournoi", "open_input_tournament_edit"),
            ("Commencer le tournoi", "start_new_round"),
            ("Rapports", "open_reports", "tournament"),  # R1
            ("Charger / Sauvegarder", "open_load_save"),
            ("Fermer le tournoi", "open_menu_base"),  # R1
        )

    def tournament_opened(self):
        return (
            ("Saisir les résultats du round", "input_round_results"),
            ("Modifier un acteur", "open_select_actor"),  # R1
            ("Rapports", "open_reports", "tournament"),  # R1
            ("Charger / Sauvegarder", "open_load_save"),
            ("Fermer le tournoi", "open_menu_base"),  # R1
        )

    def tournament_finalize(self):
        return (
            (
                "Saisir la note de fin de tournoi / Clore le tournoi",
                "input_final_note",
            ),
            ("Modifier un acteur", "open_select_actor"),  # R1
            ("Rapports", "open_reports", "tournament"),  # R1
            ("Charger / Sauvegarder", "open_load_save"),
            ("Fermer le tournoi", "open_menu_base"),  # R1
        )

    def tournament_closed(self):
        return (
            ("Modifier la note de fin de tournoi", "input_final_note"),
            ("Modifier un acteur", "open_select_actor"),  # R1
            ("Rapports", "open_reports", "tournament"),  # R1
            ("Charger / Sauvegarder", "open_load_save"),
            ("Fermer le tournoi", "open_menu_base"),  # R1
        )

    # --- Reports ---

    def reports_base(self):
        return (
            ("Tous les acteurs", "open_report_all_actors"),  # R3
            ("Tous les tournois", "open_report_all_tournament"),  # R3
            (
                "Tous les joueurs d'un tournoi",
                "open_select_tournament_report",
                "actors",
            ),
            ("Tous les tours d'un tournoi", "open_select_tournament_report", "rounds"),
            ("Tous les matchs d'un tournoi", "open_select_tournament_report", "matchs"),
            ("<< RETOUR", "goback"),
        )

    def reports_tournament(self):
        return (
            ("Tous les acteurs", "open_report_all_actors"),  # R3
            ("Tous les tournois", "open_report_all_tournament"),  # R3
            ("Tous les joueurs de ce tournoi", "open_report_tournament_actors"),
            ("Tous les tours de ce tournoi", "open_report_tournament_rounds"),
            ("Tous les matchs de ce tournoi", "open_report_tournament_matchs"),
            ("<< RETOUR", "goback"),
        )

    # --- Actors ---

    def actors_sortby(self, sortby="alpha"):
        retv = []
        if sortby != "alpha":
            retv.append(
                ("Tri par ordre alphabétique", "open_menu_actor_sortby", "alpha")
            )

        if sortby != "elo":
            retv.append(("Tri par classement ELO", "open_menu_actor_sortby", "elo"))

        if sortby != "age":
            retv.append(("Tri par age", "open_menu_actor_sortby", "age"))

        if sortby != "sex":
            retv.append(("Tri par sexe", "open_menu_actor_sortby", "sex"))

        if sortby != "score":
            retv.append(("Tri par score", "open_menu_actor_sortby", "score"))

        retv.append(("<< RETOUR", "goback"))

        return tuple(retv)

    # --- Solo buttons ---

    def only_back(self):
        return (("<< RETOUR", "goback"),)

    # --- Dynamic menus ---

    def select_tournament_load(self):

        tournaments = World.tournaments
        logging.debug(f"SELECT TOURNAMENT LOAD: {tournaments}")
        for t in tournaments:
            logging.debug(t.toJSON())
        if len(tournaments) > 0:
            retv = [(f"{t.name}", "open_tournament_current", t) for t in tournaments]
            return tuple(retv)
        else:
            return (
                ("Aucun tournoi", "goback"),
            )  # ("Créer un tournoi", "open_input_tournament_new"),)

    def select_tournament_report(self, route):

        if route == "actors":
            link = "open_report_tournament_actors"
        elif route == "rounds":
            link = "open_report_tournament_rounds"
        elif route == "matchs":
            link = "open_report_tournament_matchs"

        tournaments = World.tournaments
        if len(tournaments) > 0:
            retv = [(f"{t.name}", link, t) for t in tournaments]
            return tuple(retv)
        else:
            return (
                ("Aucun tournoi", "goback"),
            )  # ("Créer un tournoi", "open_input_tournament_new"),)

    def select_actor(self, sortby):

        sortTuple = Player.sortKey(sortby)
        logging.debug(f"DEBUG SORT {sortby} {sortTuple}")
        actors = sorted(World.get_actors(), key=sortTuple[0], reverse=sortTuple[1])

        if len(actors) > 0:
            retv = [
                (f" {actor.oneline()} ", "open_input_actor_edit", actor)
                for actor in actors
            ]
            return tuple(retv)
        else:
            return (
                ("Aucun acteur", "goback"),
            )  # ("Créer un acteur", "open_input_actor_new"),)

    def list_actors(self, tournament, sortby):

        sortTuple = Player.sortKey(sortby)
        actors = sorted(
            World.get_actors(tournament), key=sortTuple[0], reverse=sortTuple[1]
        )

        if len(actors) > 0:
            retv = [(f" {actor.oneline()} ", None) for actor in actors]
            return tuple(retv)
        else:
            return (("Aucun acteur", "goback"),)

    def list_all_actors(self, sortby):

        sortTuple = Player.sortKey(sortby)
        actors = sorted(World.get_all_actors(), key=sortTuple[0], reverse=sortTuple[1])

        if len(actors) > 0:
            retv = [(f" {actor.oneline()} ", None) for actor in actors]
            return tuple(retv)
        else:
            return (("Aucun acteur", "goback"),)

    def list_rounds(self, tournament):

        rounds = tournament.rounds
        if len(rounds) > 0:
            retv = [(f" {round.oneline()} ", None) for round in rounds]
            return tuple(retv)
        else:
            return (("Le tournoi n'est pas commencé", "goback"),)

    def list_games(self, tournament):

        rounds = tournament.rounds
        if len(rounds) > 0:

            retv = []
            for r in rounds:

                retv.append(("", None))
                retv.append((f" {r.name} ", None))

                for i, game in enumerate(r.games):

                    player1 = World.get_actor(game[0][0])
                    player2 = World.get_actor(game[1][0])

                    score1 = game[0][1]
                    score2 = game[1][1]

                    retv.append(
                        (
                            f"({player1.oneline(age=False, sex=False, score=False, extra=f'PtS:{score1:3}')}) vs "
                            + f"({player2.oneline(age=False, sex=False, score=False, extra=f'PTs:{score2:3}')})",
                            None,
                        )
                    )

            return tuple(retv)
        else:
            return (("Le tournoi n'est pas commencé", "goback"),)
