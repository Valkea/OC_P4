#! /usr/bin/env python3
# coding: utf-8

""" This module handles the menu model """


class Menu:
    """ This class provides the content of the various menus used to navigate into the application. """

    @staticmethod
    def base(self):
        return (
            ("Créer un nouveau tournoi", "open_input_tournament_new"),
            ("Charger un tournoi", "open_select_tournament_load"),
            ("Rapports", "open_reports", "base"),
            ("Charger / Sauvegarder", "open_load_save"),
            ("Quitter", "quit_menu"),
        )

    @staticmethod
    def quit_menu(self):
        return (
            ("Sauvegarder & quitter", "save_n_quit"),
            ("Quitter sans sauver", "quit"),
        )

    @staticmethod
    def save_n_load(self):
        return (
            ("Sauvegarder", "open_save"),  # R1
            ("Charger les données", "open_load"),
            ("<< RETOUR", "go_back"),
        )

    # --- Tournament ---

    @staticmethod
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

    @staticmethod
    def tournament_opened(self):
        return (
            ("Saisir les résultats du round", "input_round_results"),
            ("Modifier un acteur", "open_select_actor"),  # R1
            ("Rapports", "open_reports", "tournament"),  # R1
            ("Charger / Sauvegarder", "open_load_save"),
            ("Fermer le tournoi", "open_menu_base"),  # R1
        )

    @staticmethod
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

    @staticmethod
    def tournament_closed(self):
        return (
            ("Modifier la note de fin de tournoi", "input_final_note"),
            ("Modifier un acteur", "open_select_actor"),  # R1
            ("Rapports", "open_reports", "tournament"),  # R1
            ("Charger / Sauvegarder", "open_load_save"),
            ("Fermer le tournoi", "open_menu_base"),  # R1
        )

    # --- Reports ---

    @staticmethod
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
            ("<< RETOUR", "go_back"),
        )

    @staticmethod
    def reports_tournament(self):
        return (
            ("Tous les acteurs", "open_report_all_actors"),  # R3
            ("Tous les tournois", "open_report_all_tournament"),  # R3
            ("Tous les joueurs de ce tournoi", "open_report_tournament_actors"),
            ("Tous les tours de ce tournoi", "open_report_tournament_rounds"),
            ("Tous les matchs de ce tournoi", "open_report_tournament_matchs"),
            ("<< RETOUR", "go_back"),
        )

    # --- Actors ---

    @staticmethod
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

        retv.append(("<< RETOUR", "go_back"))

        return tuple(retv)

    # --- Solo buttons ---

    @staticmethod
    def only_back(self):
        return (("<< RETOUR", "go_back"),)
