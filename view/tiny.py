#! /usr/bin/env python3
# coding: utf-8

""" The purpose of this module is to handle the TinyDB IO """

from tinydb import TinyDB
import logging
import json

# from controller.iofiles import PUBLIC_ENUMS, EnumEncoder, as_enum, to_json, from_json
# from controller.iofiles import to_json, from_json


class TinyDBView:
    """ D """

    def __init__(self):
        logging.info("< Open Tiny View")

        self.db = TinyDB("tournoi.json")
        self.tournaments_table = self.db.table("tournaments")
        self.players_table = self.db.table("players")
        self.rounds_table = self.db.table("rounds")
        self.games_table = self.db.table("games")

    def save_all(self, world):
        """ D """

        d_tournaments = []
        d_players = []
        d_rounds = []

        for i, _tournament in enumerate(world.tournaments):
            # save tournaments avec des ID pour les players
            d_tournaments.append(_tournament.toJSON())

            for _round in _tournament.rounds:
                # save rounds
                d_rounds.append(_round.toJSON())
                for _game in _round.games:
                    # save games
                    pass
            for _player in _tournament.players:
                # save players
                d_players.append(_player.toJSON())
                for game in _player.games:
                    # save games REF
                    pass

            self.write_tournaments(d_tournaments)
            self.write_players(d_players)
            self.write_rounds(d_rounds)

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

    def write_rounds(self, serialized_data):
        """ D """

        logging.debug(f"WRITE_ROUNDS {serialized_data} {type(serialized_data)}")

        self.rounds_table.truncate()  # clear the table
        self.rounds_table.insert_multiple(serialized_data)

    def load_rounds(self):
        """ D """
        return self.rounds_table.all()
