#! /usr/bin/env python3
# coding: utf-8

""" This module handles the menu model
"""

import logging


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
            ("Créer un tournoi", "open_new_tournament"),
            ("Liste de tous les tournois", "open_tournois_select"),
            ("< Retour", "open_menu_base"),
        )

    def menu_tournois_select(self, world):
        # world.add_tournament("Tournoi 01", "Caen", ["20/12/2020", "21/12/2020"], "bullet")
        logging.debug(f"menu_tournois_select: {world}")

        back_btn = ("< Retour", "open_tournois")
        tournaments = world.tournaments
        if len(tournaments) > 0:
            retv = [(f"{t.name}", "open_tournoi_actions") for t in tournaments]
            retv.append(back_btn)
            return tuple(retv)
        else:
            return (
                ("Aucun tournoi", back_btn[1]),
                back_btn,
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
