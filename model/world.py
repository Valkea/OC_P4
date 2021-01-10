#! /usr/bin/env python3
# coding: utf-8

""" This module handles the tournaments
"""

from model.player import Player
from model.tournament import Tournament
import logging


class World:
    """ D """

    actors = {}
    tournaments = []
    active_tournament = None

    @classmethod
    def load(cls, tournaments, actors):
        cls.actors = {}
        cls.tournaments = []
        cls.active_tournament = None

        for actor in actors:
            cls.actors[actor["uid"]] = Player(**actor)

        for tournament in tournaments:
            # tournament = json.loads(tournament, object_hook=as_enum)
            new_tournament = Tournament(cls, **tournament)
            cls.set_active_tournament(new_tournament)
            cls.tournaments.append(new_tournament)

    # --- Tournament ---

    @classmethod
    def add_tournament(
        cls, name, place, start_date, end_date, gtype, desc="", rounds=4
    ):
        """ D """
        tournament = Tournament(
            cls,
            name,
            place,
            start_date,
            end_date,
            gtype,
            desc,
            rounds,
        )

        cls.tournaments.append(tournament)

        return tournament

    @classmethod
    def set_active_tournament(cls, tournament):
        """ D """
        cls.active_tournament = tournament

    @classmethod
    def get_active_tournament(cls):
        """ D """
        return cls.active_tournament

    # --- Actors ---

    @classmethod
    def add_actor(cls, actor, tournament=None):
        """Add a player to the current tournament instance

        Parameters
        ----------
        actor : Player
            the Player instance to register as a participant of the tournament
        """

        if type(actor) is not Player:
            raise TypeError("Player instance expected")

        if tournament is None:
            tournament = cls.get_active_tournament()

        cls.actors[actor.uid] = actor
        tournament.add_player(actor.uid)

        return id(actor)

    @classmethod
    def get_actor(cls, actor_id):
        """ D """

        return cls.actors.get(actor_id)

    @classmethod
    def get_actors(cls, tournament=None):
        """ D """

        if tournament is None:
            tournament = cls.get_active_tournament()

        logging.debug(f"GET_ACTORS: {tournament}")

        actors_id = tournament.players

        return [v for k, v in cls.actors.items() if k in actors_id]

    @classmethod
    def get_all_actors(cls):
        """ D """

        return [v for k, v in cls.actors.items()]
