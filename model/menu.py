#! /usr/bin/env python3
# coding: utf-8

""" This module handles the menu labels & actions
"""


class Menu:
    """ TODO """

    def __init__(self):
        pass

    def menu_base(self):
        return (
            ("Tournoi", "open_tournoi"),
            ("Rapports", "open_rapports"),
            ("Quitter", "quit"),
        )

    def menu_tournoi(self):
        return (
            ("Créer un tournoi", None),
            ("Liste de tous les tournois", "open_tournoi_list"),
            ("< Retour", "open_menu_base"),
        )

    def menu_tournoi_list(self):
        return (
            ("Tournoi 01", "open_tournoi_choix"),
            ("Tournoi 02", "open_tournoi_choix"),
            ("Tournoi 03", "open_tournoi_choix"),
            ("Tournoi 04", "open_tournoi_choix"),
            ("Tournoi 05", "open_tournoi_choix"),
            ("< Retour", "open_tournoi"),
        )

    def menu_tournoi_choix(self):
        return (
            ("Charger", None),
            ("Editer", None),
            ("Supprimer", None),
            ("< Retour", "open_tournoi_list"),
        )

    def menu_rapports(self):
        return (
            ("Liste de tous les acteurs de tous les tournois", None),
            ("Liste de tous les joueurs de tous les tournois", None),
            ("Liste de tous les tours d'un tournoi", None),
            ("Liste de tous les matchs d'un tournoi", None),
            ("< Retour", "open_menu_base"),
        )
