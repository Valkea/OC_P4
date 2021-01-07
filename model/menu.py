#! /usr/bin/env python3
# coding: utf-8

""" This module handles the menu model
"""


class Menu:
    """ TODO """

    def __init__(self):
        pass

    def base(self):
        return (
            ("Créer un nouveau tournoi", "open_input_tournament_new"),
            ("Charger un tournoi", "open_select_tournament_load"),
            ("Rapports", "open_reports", "base"),
            ("Quitter", "quit"),
        )

    # --- Tournament ---

    def tournament_initialize(self):
        return (
            ("Ajouter un joueur au tournoi", "open_input_actor_new"),
            ("Modifier un acteur", "open_select_actor"),
            ("Modifier le tournoi", "open_input_tournament_edit"),
            ("Commencer le tournoi", "start_new_round"),
            ("Rapports", "open_reports", "tournament"),  # R1
            ("Sauvegarder", "open_save"),  # R1
            ("Fermer le tournoi", "open_menu_base"),  # R1
        )

    def tournament_opened(self):
        return (
            ("Saisir les résultats du round", "input_round_results"),
            ("Modifier un acteur", "open_select_actor"),  # R1
            ("Rapports", "open_reports", "tournament"),  # R1
            ("Sauvegarder", "open_save"),  # R1
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
            ("Sauvegarder", "open_save"),  # R1
            ("Fermer le tournoi", "open_menu_base"),  # R1
        )

    def tournament_closed(self):
        return (
            ("Modifier la note de fin de tournoi", "input_final_note"),
            ("Modifier un acteur", "open_select_actor"),  # R1
            ("Rapports", "open_reports", "tournament"),  # R1
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

    def actors_alpha(self):
        return (
            ("Tri par ordre alphabétique", "open_menu_actor_order", "alpha"),
            ("<< RETOUR", "goback"),
        )

    def actors_elo(self):
        return (
            ("Tri par classement ELO", "open_menu_actor_order", "elo"),
            ("<< RETOUR", "goback"),
        )

    # --- Solo buttons ---

    def only_back(self):
        return (("<< RETOUR", "goback"),)

    # --- Dynamic menus ---

    def select_tournament_load(self, world):

        tournaments = world.tournaments
        if len(tournaments) > 0:
            retv = [(f"{t.name}", "open_tournament_current", t) for t in tournaments]
            return tuple(retv)
        else:
            return (
                ("Aucun tournoi", "goback"),
            )  # ("Créer un tournoi", "open_input_tournament_new"),)

    def select_tournament_report(self, world, route):

        if route == "actors":
            link = "open_report_tournament_actors"
        elif route == "rounds":
            link = "open_report_tournament_rounds"
        elif route == "matchs":
            link = "open_report_tournament_matchs"

        tournaments = world.tournaments
        if len(tournaments) > 0:
            retv = [(f"{t.name}", link, t) for t in tournaments]
            return tuple(retv)
        else:
            return (
                ("Aucun tournoi", "goback"),
            )  # ("Créer un tournoi", "open_input_tournament_new"),)

    def select_actor(self, world):

        tournament = world.get_active_tournament()
        actors = tournament.get_actors()
        if len(actors) > 0:
            retv = [
                (f" {actor.oneline(30)} ", "open_input_actor_edit", actor)
                for actor in actors
            ]
            return tuple(retv)
        else:
            return (
                ("Aucun acteur", "goback"),
            )  # ("Créer un acteur", "open_input_actor_new"),)

    def list_actors(self, tournament):

        actors = tournament.get_actors()
        if len(actors) > 0:
            retv = [(f" {actor.oneline(30)} ", None) for actor in actors]
            return tuple(retv)
        else:
            return (("Aucun acteur", "goback"),)

    def list_all_actors(self, world):

        actors = world.get_all_actors()
        if len(actors) > 0:
            retv = [(f" {actor.oneline(30)} ", None) for actor in actors]
            return tuple(retv)
        else:
            return (("Aucun acteur", "goback"),)

    def list_rounds(self, tournament):

        rounds = tournament.rounds
        if len(rounds) > 0:
            retv = [(f" {round.oneline(10)} ", None) for round in rounds]
            return tuple(retv)
        else:
            return (("Le tournoi n'est pas commencé", "goback"),)
