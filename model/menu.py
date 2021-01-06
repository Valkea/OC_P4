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
            ("Commencer le tournoi", "open_tournament_opened"),
            ("Rapports", "open_reports", "tournament"),  # R1
            ("Sauvegarder", "open_save"),  # R1
            ("Fermer le tournoi", "open_menu_base"),  # R1
        )

    def tournament_opened(self):
        return (
            ("Saisir les résultats du round", "open_tournament_finalize"),
            ("Modifier un acteur", "open_select_actor"),  # R1
            ("Rapports", "open_reports", "tournament"),  # R1
            ("Sauvegarder", "open_save"),  # R1
            ("Fermer le tournoi", "open_menu_base"),  # R1
        )

    def tournament_finalize(self):
        return (
            (
                "Saisir la note de fin de tournoi / Clore le tournoi",
                "open_tournament_closed",
            ),
            ("Modifier un acteur", "open_select_actor"),  # R1
            ("Rapports", "open_reports", "tournament"),  # R1
            ("Sauvegarder", "open_save"),  # R1
            ("Fermer le tournoi", "open_menu_base"),  # R1
        )

    def tournament_closed(self):
        return (
            ("Modifier un acteur", "open_select_actor"),  # R1
            ("Rapports", "open_reports", "tournament"),  # R1
            ("Fermer le tournoi", "open_menu_base"),  # R1
        )

    # --- Reports ---

    def reports_base(self):
        return (
            ("Tous les acteurs", "open_report_all_actors"),  # R3
            ("Tous les tournois", "open_report_all_tournament"),  # R3
            ("Tous les joueurs d'un tournoi", None),
            ("Tous les tours d'un tournoi", None),
            ("Tous les matchs d'un tournoi", None),
            ("<< RETOUR", "goback"),
        )

    def reports_tournament(self):
        return (
            ("Tous les acteurs", "open_report_all_actors"),  # R3
            ("Tous les tournois", "open_report_all_tournament"),  # R3
            ("Tous les joueurs de ce tournoi", None),
            ("Tous les tours de ce tournoi", None),
            ("Tous les matchs de ce tournoi", None),
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
            retv = [(f"{t.name}", "open_tournament_initialize", t) for t in tournaments]
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

    def list_all_actors(self, world):

        actors = world.get_all_actors()
        if len(actors) > 0:
            retv = [(f" {actor.oneline(30)} ", None, actor) for actor in actors]
            return tuple(retv)
        else:
            return (
                ("Aucun acteur", "goback"),
            )  # ("Créer un acteur", "open_input_actor_new"),)

    # ------------------------------------------------------------------------


#    def menu_base(self):
#        return (
#            ("Tournois", "open_tournois"),
#            ("Rapports", "open_rapports"),
#            ("Quitter", "quit"),
#        )
#
#    def menu_tournois(self):
#        return (
#            ("Créer un tournoi", "open_new_tournament"),
#            ("Liste de tous les tournois", "open_tournois_select"),
#            ("< Retour", "open_menu_base"),
#        )
#
#    def menu_tournoi_select_actions(self):
#        return (
#            ("Charger", None),
#            ("Editer", None),
#            ("Supprimer", None),
#            ("< Retour", "open_tournois_select"),
#        )
#
#    def menu_tournoi_base(self):
#        return (
#            ("Editer le tournoi", None),
#            ("Ajouter un acteur", "open_new_actor"),
#            (
#                "Gérer les acteurs",
#                "open_tournoi_actors",
#            ),
#            ("Rapports", "open_tournoi_rapport"),
#            ("Sauvegarder le tournoi", None),
#            ("Charger un autre tournoi", "open_tournois_select"),
#        )
#
#    def menu_tournoi_actor_select(self):
#        return (("< Retour", "open_tournois_infos"),)
#
#    def menu_tournoi_actor_manager(self):
#        return (
#            # ("Editer l'acteur", None),
#            ("Supprimer l'acteur", None),
#            ("< Retour", "open_tournoi_actors"),
#        )
#
#    def menu_tournoi_rapports(self):
#        return (
#            ("Liste de tous les joueurs de ce tournoi", None),
#            ("Liste de tous les tours de ce tournoi", None),
#            ("Liste de tous les matchs de ce tournoi", None),
#            ("Liste de tous les tournois", None),
#            ("Liste de tous les acteurs de tous les tournois", None),
#            ("Liste de tous les joueurs de tous les tournois", None),
#            ("< Retour", "open_tournois_infos"),
#        )
#
#    def menu_rapports(self):
#        return (
#            ("Liste de tous les joueurs d'un tournoi", None),
#            ("Liste de tous les tours d'un tournoi", None),
#            ("Liste de tous les matchs d'un tournoi", None),
#            ("Liste de tous les tournois", None),
#            ("Liste de tous les acteurs de tous les tournois", None),
#            ("Liste de tous les joueurs de tous les tournois", None),
#            ("< Retour", "open_menu_base"),
#        )
