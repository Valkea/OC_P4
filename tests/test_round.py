#! /usr/bin/env python3
# coding: utf-8

"""
The purpose of this module is to test the Round class
"""

import datetime

from model.world import World
from model.round import Round
from model.player import Player
from model.tournament import Tournament, Status


class TestRound:
    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self):
        World.clear()
        self.T1 = Tournament(
            World, "Test1", "TestAre1", "01.01.2020", "02.01.2020", "bullet", ""
        )
        self.T2 = Tournament(
            World, "Test2", "TestAre1", "01.01.2021", "02.01.2021", "blitz", ""
        )
        self.P1 = Player("P1", "p", "1.1.1979", "M", 1380)
        self.P2 = Player("P2", "p", "1.1.1979", "M", 2120)

        World.add_tournament(self.T1)
        World.set_active_tournament(self.T1)

        self.R1 = Round(World, "Round1", 0, [self.P1.uid, self.P2.uid])

    # --- start_time ---

    def test_start_time_inside_format(self):
        assert type(self.R1._start_time) == datetime.datetime

    def test_start_time_outside_format(self):
        assert type(self.R1.start_time) == str

    def test_start_time_open(self):
        assert self.R1.start_time is not None

    # --- close_time ---

    def test_close_time_inside_format(self):
        self.R1.close()
        assert type(self.R1._close_time) == datetime.datetime

    def test_close_time_outside_format(self):
        self.R1.close()
        assert type(self.R1.close_time) == str

    def test_close_time_open(self):
        assert self.R1.close_time is None

    def test_close_time_closed(self):
        self.R1.close()
        assert self.R1.close_time is not None

    # --- oneline ---

    def test_one_line_format(self):
        assert type(self.R1.one_line()) == str

    def test_one_line_content(self):
        assert "Round1" in self.R1.one_line()
        assert self.R1.start_time in self.R1.one_line()

    # --- serialize ---

    def test_serialize_format(self):
        assert type(self.R1.serialize()) == dict

    # --- convert_score_symbol ---

    def test_convert_symbol_P1_win(self):
        assert Round.convert_score_symbol("<") == (1, 0)

    def test_convert_symbol_P2_win(self):
        assert Round.convert_score_symbol(">") == (0, 1)

    def test_convert_symbol_equal(self):
        assert Round.convert_score_symbol("=") == (0.5, 0.5)

    # --- list_rounds ---

    def test_list_rounds(self):
        assert len(Round.list_rounds(self.T1)) == 1  # Back button

    def test_list_rounds_round2(self):
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

        self.T1.status = Status.INITIALIZED

        self.T1.start_round()
        assert len(Round.list_rounds(self.T1)) == 1  # ROUND NAME x 1

        self.T1.start_round()
        assert len(Round.list_rounds(self.T1)) == 2  # ROUND NAME x 2

        self.T1.start_round()
        assert len(Round.list_rounds(self.T1)) == 3  # ROUND NAME x 3

        self.T1.start_round()
        assert len(Round.list_rounds(self.T1)) == 4  # ROUND NAME x 4

    # --- list_games ---

    def test_list_games(self):
        assert len(Round.list_games(self.T1, World)) == 1  # Back button

    def test_list_games_round2(self):
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

        self.T1.status = Status.INITIALIZED

        self.T1.start_round()
        assert (
            len(Round.list_games(self.T1, World)) == 6
        )  # (SPACE + ROUND NAME + GAMES) x 1

        self.T1.start_round()
        assert (
            len(Round.list_games(self.T1, World)) == 12
        )  # (SPACE + ROUND NAME + GAMES) x 2

        self.T1.start_round()
        assert (
            len(Round.list_games(self.T1, World)) == 18
        )  # (SPACE + ROUND NAME + GAMES) x 3

        self.T1.start_round()
        assert (
            len(Round.list_games(self.T1, World)) == 24
        )  # (SPACE + ROUND NAME + GAMES) x 4
