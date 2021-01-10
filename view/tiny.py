#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to handle the TinyDB IO """

import json
import logging

from tinydb import TinyDB

from model.world import World


class TinyDbView:
    """This class provide various methods to save & load the app data.

    Class Methods
    -------------
    open_file()
        Open / Reload the tournament.json file
    save_all()
        Save the tournaments and players' data from the World instance
    write_tournaments(, serialized_data)
        Write the provided serialized data in the tournaments_table
    write_players(, serialized_players)
        Write the provided serialized data in the players_table
    load_all()
        Return the tournaments and players dictionaries from the file
    load_tournaments()
        Return the serialized content of the tournaments_table
    load_players()
        Return the serialized content of the players_table
    """

    @classmethod
    def open_file(cls):
        """ Open / Reload the tournament.json file. """

        cls.db = TinyDB("tournament.json")
        cls.tournaments_table = cls.db.table("tournaments")
        cls.players_table = cls.db.table("players")

    @classmethod
    def save_all(cls):
        """ Save the tournaments and players' data from the World instance. """

        cls.open_file()

        d_tournaments = []
        d_players = []

        for i, _tournament in enumerate(World.tournaments):
            d_tournaments.append(json.loads(json.dumps(_tournament.serialize())))

        for i, _actor in enumerate(World.get_all_actors()):
            d_players.append(json.loads(json.dumps(_actor.serialize())))

        cls.write_tournaments(d_tournaments)
        cls.write_players(d_players)

    @classmethod
    def write_tournaments(cls, serialized_data):
        """ Write the provided serialized data in the tournaments_table. """

        logging.debug(f"WRITE_TOURNAMENTS: {serialized_data} {type(serialized_data)}")

        cls.tournaments_table.truncate()  # clear the table
        cls.tournaments_table.insert_multiple(serialized_data)

    @classmethod
    def write_players(cls, serialized_players):
        """ Write the provided serialized data in the players_table. """

        logging.debug(f"WRITE_ALL_PLAYERS: {serialized_players}")

        cls.players_table.truncate()  # clear the table
        cls.players_table.insert_multiple(serialized_players)

    @classmethod
    def load_all(cls):
        """ Return the tournaments and players dictionaries from the file. """

        cls.open_file()

        tournaments = cls.load_tournaments()
        players = cls.load_players()

        return tournaments, players

    @classmethod
    def load_tournaments(cls):
        """ Return the serialized content of the tournaments_table. """

        return cls.tournaments_table.all()

    @classmethod
    def load_players(cls):
        """ Return the serialized content of the players_table. """

        return cls.players_table.all()
