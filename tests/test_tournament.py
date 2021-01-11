#! /usr/bin/env python3
# coding: utf-8

"""
The purpose of this module is to test the Tournament class
"""

import pytest

from model.world import World
from model.round import Round
from model.player import Player
from model.tournament import (
    Tournament,
    Status,
    IsComplete,
    IsNotReady,
)


class TestTournament:
    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self):
        World.clear()

        self.T1 = Tournament(
            World, "Test1", "TestAre1", "01.01.2020", "02.01.2020", "bullet", ""
        )
        World.add_tournament(self.T1)
        World.set_active_tournament(self.T1)

        self.P1 = Player("P1", "p", "1.1.1979", "M", 1380)
        self.P2 = Player("P2", "p", "1.1.1979", "M", 2120)
        self.P3 = Player("P3", "p", "1.1.1979", "M", 1612)
        self.P4 = Player("P4", "p", "1.1.1979", "M", 999)
        self.P5 = Player("P5", "p", "1.1.1979", "M", 1720)
        self.P6 = Player("P6", "p", "1.1.1979", "M", 2000)
        self.P7 = Player("P7", "p", "1.1.1979", "M", 230)
        self.P8 = Player("P8", "p", "1.1.1979", "M", 3000)

        World.add_actor(self.P1, self.T1)
        World.add_actor(self.P2, self.T1)
        World.add_actor(self.P3, self.T1)
        World.add_actor(self.P4, self.T1)
        World.add_actor(self.P5, self.T1)
        World.add_actor(self.P6, self.T1)
        World.add_actor(self.P7, self.T1)
        World.add_actor(self.P8, self.T1)

    def test_full_algo(self):

        self.T1.status = Status.INITIALIZED

        self.T1.start_round()
        assert self.T1.current_round().name == "Round 1"
        self.T1.set_results(0, *Round.convert_score_symbol("<"))
        self.T1.set_results(1, *Round.convert_score_symbol("<"))
        self.T1.set_results(2, *Round.convert_score_symbol("="))
        self.T1.set_results(3, *Round.convert_score_symbol(">"))
        self.T1.current_round().close()

        self.T1.start_round()
        assert self.T1.current_round().name == "Round 2"
        self.T1.set_results(0, *Round.convert_score_symbol("<"))
        self.T1.set_results(1, *Round.convert_score_symbol(">"))
        self.T1.set_results(2, *Round.convert_score_symbol(">"))
        self.T1.set_results(3, *Round.convert_score_symbol(">"))
        self.T1.current_round().close()

        self.T1.start_round()
        assert self.T1.current_round().name == "Round 3"
        self.T1.set_results(0, *Round.convert_score_symbol(">"))
        self.T1.set_results(1, *Round.convert_score_symbol("<"))
        self.T1.set_results(2, *Round.convert_score_symbol("="))
        self.T1.set_results(3, *Round.convert_score_symbol("="))
        self.T1.current_round().close()

        self.T1.start_round()
        assert self.T1.current_round().name == "Round 4"
        self.T1.set_results(0, *Round.convert_score_symbol(">"))
        self.T1.set_results(1, *Round.convert_score_symbol("<"))
        self.T1.set_results(2, *Round.convert_score_symbol("="))
        self.T1.set_results(3, *Round.convert_score_symbol("<"))
        self.T1.current_round().close()

        with pytest.raises(IsComplete):
            self.T1.start_round()

        results = self.T1.get_overall_infos()

        assert results["result0"] == self.P8.one_line()
        assert results["result1"] == self.P2.one_line()
        assert results["result2"] == self.P6.one_line()
        assert results["result3"] == self.P5.one_line()
        assert results["result4"] == self.P7.one_line()
        assert results["result5"] == self.P1.one_line()
        assert results["result6"] == self.P4.one_line()
        assert results["result7"] == self.P3.one_line()

        assert self.P8.score == 3
        assert self.P2.score == 3
        assert self.P6.score == 2.5
        assert self.P5.score == 2
        assert self.P7.score == 2
        assert self.P1.score == 1.5
        assert self.P4.score == 1.5
        assert self.P3.score == 0.5

    # --- start_round ---

    def test_start_round_UNINITIALIZED(self):
        self.T1.status = Status.UNINITIALIZED
        with pytest.raises(IsNotReady):
            self.T1.start_round()

    def test_start_round_INITIALIZED(self):
        self.T1.status = Status.INITIALIZED
        assert len(self.T1.rounds) == 0
        self.T1.start_round()
        assert len(self.T1.rounds) == 1

    def test_start_round_PLAYING(self):
        self.T1.status = Status.PLAYING
        assert len(self.T1.rounds) == 0
        self.T1.start_round()
        assert len(self.T1.rounds) == 1

    def test_start_round_CLOSING(self):
        self.T1.status = Status.CLOSING
        with pytest.raises(IsComplete):
            self.T1.start_round()

    def test_start_round_CLOSED(self):
        self.T1.status = Status.CLOSED
        with pytest.raises(IsComplete):
            self.T1.start_round()

    # --- set_results ---

    def test_set_results(self):
        self.T1.status = Status.INITIALIZED
        self.T1.start_round()

        current_round = self.T1.current_round()
        game_index = 0
        game = current_round.games[game_index]

        p1_id = game[0][0]
        p2_id = game[1][0]

        p1 = World.get_actor(p1_id)
        p2 = World.get_actor(p2_id)

        assert game[0][1] == 0
        assert game[1][1] == 0
        assert p1.score == 0
        assert p2.score == 0
        assert p1.has_played(p2_id) is False
        assert p2.has_played(p1_id) is False

        self.T1.set_results(game_index, 1, 0)

        assert game[0][1] == 1
        assert game[1][1] == 0
        assert p1.score == 1
        assert p2.score == 0
        assert p1.has_played(p2_id) is True
        assert p2.has_played(p1_id) is True

    # --- add players ---

    def test_add_players(self):
        assert len(self.T1.players) == 8  # From setup_method
        P = Player("PX", "p", "1.1.1979", "M", 3000)
        self.T1.add_player(P.uid)
        assert len(self.T1.players) == 9

    # --- current_round ---

    def test_current_round(self):
        self.T1.status = Status.INITIALIZED

        self.T1.start_round()
        assert self.T1.rounds[-1] == self.T1.current_round()
        self.T1.start_round()
        assert self.T1.rounds[-1] == self.T1.current_round()

    # --- serialize ---

    def test_serialize_format(self):
        assert type(self.T1.serialize()) == dict

    # --- get_overall_infos ---

    def test_get_overall_infos_format(self):
        assert type(self.T1.get_overall_infos()) == dict

    # --- get_fields ---

    def test_get_fields(self):
        assert type(self.T1.get_fields()) == list

    def test_get_fields_final_note(self):
        assert type(self.T1.get_fields_final_note()) == list

    def test_get_fields_input_scores(self):
        self.T1.status = Status.INITIALIZED

        self.T1.start_round()
        assert type(self.T1.get_fields_input_scores()) == list

    def test_select_tournament_load(self):
        t = self.T1.select_tournament_load(World)
        assert type(t) == tuple
        assert type(t[0][2]) == Tournament

    def test_select_tournament_select(self):
        t = self.T1.select_tournament_report(World, "actors")
        assert type(t) == tuple
        assert type(t[0][2]) == Tournament

    # TODO ?
