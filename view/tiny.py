#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to handle the TinyDB IO """

from tinydb import TinyDB
import json
import logging

from model.world import World


class TinyDbView:
    """ D """

    @classmethod
    def open_file(cls):

        cls.db = TinyDB("tournament.json")
        cls.tournaments_table = cls.db.table("tournaments")
        cls.players_table = cls.db.table("players")

    @classmethod
    def save_all(cls):
        """ D """

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
        """ D """

        logging.debug(f"WRITE_TOURNAMENTS: {serialized_data} {type(serialized_data)}")

        cls.tournaments_table.truncate()  # clear the table
        cls.tournaments_table.insert_multiple(serialized_data)

    @classmethod
    def write_players(cls, serialized_players):
        """ D """

        logging.debug(f"WRITE_ALL_PLAYERS: {serialized_players}")

        cls.players_table.truncate()  # clear the table
        cls.players_table.insert_multiple(serialized_players)

    @classmethod
    def load_all(cls):

        cls.open_file()

        tournaments = cls.load_tournaments()
        players = cls.load_players()

        for t in tournaments:
            logging.debug(f"LOAD ALL: {t}")

        return tournaments, players

    @classmethod
    def load_tournaments(cls):
        """ D """
        return cls.tournaments_table.all()

    @classmethod
    def load_players(cls):
        """ D """
        return cls.players_table.all()
