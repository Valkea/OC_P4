#! /usr/bin/env python3
# coding: utf-8

""" This module handles the app world """

from model.player import Player
from model.tournament import Tournament
import logging


class World:
    """This ROOT class offer several methods to register and search for tournaments and actors.

    All the apps' data are stored here and accessible from here.
    All methods are classmethods, so we can access the content using World.method() World.attribute

    Attributes
    ----------

    actors : dict('UID', Player)
        The list of all actors
    tournaments : list(Tournament)
        The list of all tournaments
    active_tournament : Tournament
        The currently active tournament instance

    Public Methods
    --------------
    load(tournaments, actors)
        Replace the class attributes with the provided ones
    add_tournament(name, place, start_date, end_date, gtype, desc="", rounds=4)
        Register a new tournament instance
    set_active_tournament(tournament)
        Set the currently active tournament instance
    get_active_tournament()
        Get the currently active tournament instance or None

    add_actor(actor, tournament=None)
        Register a new actor to the provided Tournament instance (or the currently active)
    get_actor(actor_id)
        Get an actor instance by providing it's UID
    get_actors(tournament=None)
        Get all the actors instances of the provided Tournament instance (or the currently active)
    get_all_actors()
        Get all the actors instances
    """

    actors = {}
    tournaments = []
    active_tournament = None

    @classmethod
    def load(cls, tournaments, actors):
        """Replace the class attributes with the provided ones.

        Parameters
        ----------
        tournaments : list(dict)
            list of tournaments arguments dictionaries
        actors : list(dict)
            list of players arguments dictionaries
        """

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
    def add_tournament(cls, tournament):
        """Register a new tournament instance.

        Properties
        ----------
        tournament : Tournament
            The tournament instance to register
        """

        cls.tournaments.append(tournament)

        return tournament

    @classmethod
    def set_active_tournament(cls, tournament):
        """Set the currently active tournament instance.

        Properties
        ----------
        tournament : Tournament
            The tournament instance to set as the currently active one
        """

        cls.active_tournament = tournament

    @classmethod
    def get_active_tournament(cls):
        """ Get the currently active tournament instance or None. """

        return cls.active_tournament

    # --- Actors ---

    @classmethod
    def add_actor(cls, actor, tournament=None):
        """Register a new actor to the provided Tournament instance (or the currently active)

        Parameters
        ----------
        actor : Player
            the Player instance to register as a participant of the tournament
        tournament : Tournament
            The tournament instance to set as the currently active one
            If None, the currently active one is used
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
        """Get an actor instance by providing it's UID

        Parameters
        ----------
        actor_id : Player
            the requested Player's instance UID
        """

        return cls.actors.get(actor_id)

    @classmethod
    def get_actors(cls, tournament=None):
        """Get all the actors instances of the provided Tournament instance (or the currently active)

        Parameters
        ----------
        tournament : Tournament
            The tournament instance used to search the actors
            If None, the currently active one is used
        """

        if tournament is None:
            tournament = cls.get_active_tournament()

        logging.debug(f"GET_ACTORS: {tournament}")

        actors_id = tournament.players

        return [v for k, v in cls.actors.items() if k in actors_id]

    @classmethod
    def get_all_actors(cls):
        """ Get all the actors instances """

        return [v for k, v in cls.actors.items()]
