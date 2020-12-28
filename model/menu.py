#! /usr/bin/env python3
# coding: utf-8

""" This module handles the menu model
"""


class Menu:
    """ TODO """

    def __init__(self):
        pass

    def menu_base(self):
        return (
            ("Tournois", "open_tournois"),
            ("Rapports", "open_rapports"),
            ("Quitter", "quit"),
        )

    def menu_tournois(self):
        return (
            ("Créer un tournoi", None),
            ("Liste de tous les tournois", "open_tournois_select"),
            ("< Retour", "open_menu_base"),
        )

    def menu_tournois_select(self):
        return (
            ("Tournoi 01", "open_tournoi_actions"),
            ("Tournoi 02", "open_tournoi_actions"),
            ("Tournoi 03", "open_tournoi_actions"),
            ("Tournoi 04", "open_tournoi_actions"),
            ("Tournoi 05", "open_tournoi_actions"),
            ("< Retour", "open_tournois"),
        )

    def menu_tournoi_actions(self):
        return (
            ("Charger", None),
            ("Editer", None),
            ("Supprimer", None),
            ("< Retour", "open_tournois_select"),
        )

    def menu_rapports(self):
        return (
            ("Liste de tous les acteurs de tous les tournois", None),
            ("Liste de tous les joueurs de tous les tournois", None),
            ("Liste de tous les tours d'un tournoi", None),
            ("Liste de tous les matchs d'un tournoi", None),
            ("< Retour", "open_menu_base"),
        )
