#! /usr/bin/env python3
# coding: utf-8

""" This module handles the menus """


class Menu:
    """This class provides the content of the various menus used to navigate into the application.

    Static methods
    --------------
    base()
        This is the main menu
    open_open_quit_menu()
        This menu offers to save before quitting
    save_n_load()
        This menu offers to load from or save to JSON file
    only_back()
        Simple menu with a unique "back" button

    tournament_initialize()
        Tournament main menu when the tournament is created but not started yet
    tournament_opened()
        Tournament main menu when playing the rounds
    tournament_finalize()
        Tournament main menu when all rounds are played but the final note is still to write
    tournament_closed()
        Tournament main menu when the tournament is closed

    reports_base()
        Reports menu when outside a tournament
    reports_tournament()
        Reports menu when inside a tournament

    actors_sortby(sortby="alpha")
        Menu used to sort users on various screens
    """

    @staticmethod
    def base():
        return (
            ("Créer un nouveau tournoi", "open_input_tournament_new"),
            ("Charger un tournoi", "open_select_tournament_load"),
            ("Rapports", "open_reports", "base"),
            ("Charger / Sauvegarder", "open_load_save"),
            ("Quitter", "open_open_quit_menu"),
        )

    @staticmethod
    def quit():
        return (
            ("Sauvegarder & quitter", "save_n_quit"),
            ("Quitter sans sauver", "quit"),
        )

    @staticmethod
    def save_n_load():
        return (
            ("Sauvegarder", "open_save"),  # R1
            ("Charger les données", "open_load"),
            ("<< RETOUR", "go_back"),
        )

    @staticmethod
    def only_back():
        return (("<< RETOUR", "go_back"),)

    # --- TOURNAMENT ---

    @staticmethod
    def tournament_initialize():
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
    def tournament_opened():
        return (
            ("Saisir les résultats du round", "open_input_round_results"),
            ("Modifier un acteur", "open_select_actor"),  # R1
            ("Rapports", "open_reports", "tournament"),  # R1
            ("Charger / Sauvegarder", "open_load_save"),
            ("Fermer le tournoi", "open_menu_base"),  # R1
        )

    @staticmethod
    def tournament_finalize():
        return (
            (
                "Saisir la note de fin de tournoi / Clore le tournoi",
                "open_input_final_note",
            ),
            ("Modifier un acteur", "open_select_actor"),  # R1
            ("Rapports", "open_reports", "tournament"),  # R1
            ("Charger / Sauvegarder", "open_load_save"),
            ("Fermer le tournoi", "open_menu_base"),  # R1
        )

    @staticmethod
    def tournament_closed():
        return (
            ("Modifier la note de fin de tournoi", "open_input_final_note"),
            ("Modifier un acteur", "open_select_actor"),  # R1
            ("Rapports", "open_reports", "tournament"),  # R1
            ("Charger / Sauvegarder", "open_load_save"),
            ("Fermer le tournoi", "open_menu_base"),  # R1
        )

    # --- REPORTS ---

    @staticmethod
    def reports_base():
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
    def reports_tournament():
        return (
            ("Tous les acteurs", "open_report_all_actors"),  # R3
            ("Tous les tournois", "open_report_all_tournament"),  # R3
            ("Tous les joueurs de ce tournoi", "open_report_tournament_actors"),
            ("Tous les tours de ce tournoi", "open_report_tournament_rounds"),
            ("Tous les matchs de ce tournoi", "open_report_tournament_matchs"),
            ("<< RETOUR", "go_back"),
        )

    # --- ACTORS ---

    @staticmethod
    def actors_sortby(sortby="alpha"):
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
