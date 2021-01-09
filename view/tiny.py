#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to handle the TinyDB IO """

from tinydb import TinyDB
import json
import logging

from model.world import World


class TinyDBView:
    """ D """

    def __init__(self):
        logging.info("< Open Tiny View")

        self.db = TinyDB("tournoi.json")
        self.tournaments_table = self.db.table("tournaments")
        self.players_table = self.db.table("players")

    def save_all(self):
        """ D """

        d_tournaments = []
        d_players = []

        for i, _tournament in enumerate(World.tournaments):
            d_tournaments.append(json.loads(json.dumps(_tournament.toJSON())))

        for i, _actor in enumerate(World.get_all_actors()):
            d_players.append(json.loads(json.dumps(_actor.toJSON())))

        self.write_tournaments(d_tournaments)
        self.write_players(d_players)

    def load_all(self):

        tournaments = self.load_tournaments()
        players = self.load_players()

        return tournaments, players

    def write_tournaments(self, serialized_data):
        """ D """

        logging.debug(f"WRITE_TOURNAMENTS: {serialized_data} {type(serialized_data)}")

        self.tournaments_table.truncate()  # clear the table
        self.tournaments_table.insert_multiple(serialized_data)

    def load_tournaments(self):
        """ D """
        return self.tournaments_table.all()

    def write_players(self, serialized_players):
        """ D """

        logging.debug(f"WRITE_ALL_PLAYERS: {serialized_players}")

        self.players_table.truncate()  # clear the table
        self.players_table.insert_multiple(serialized_players)

    def load_players(self):
        """ D """
        return self.players_table.all()
