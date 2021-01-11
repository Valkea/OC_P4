#! /usr/bin/env python3
# coding: utf-8

"""
The purpose of this module is to test the Player class
"""

import pytest
import datetime

from model.world import World
from model.round import Round
from model.player import Player
from model.tournament import Tournament


class TestPlayer:
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
        self.P1 = Player("Name1", "Nickname1", "1.1.1979", "Homme", 1380)
        self.P2 = Player("Name2", "Nickname2", "1.1.1979", "F", 2120)

        World.add_tournament(self.T1)
        World.set_active_tournament(self.T1)

        self.R1 = Round(World, "Round1", 0, [self.P1.uid, self.P2.uid])

    # --- birthdate ---

    def test_birthdate_inside_format(self):
        assert type(self.P1._birthdate) == datetime.datetime

    def test_birthdate_outside_format(self):
        assert type(self.P1.birthdate) == str

    def test_birtdate_input_format_valid(self):
        BD = "1.1.2020"
        self.P1.birthdate = BD
        assert self.P1.birthdate == "01/01/2020"

    def test_birtdate_input_format_invalid(self):
        BD = "1.1.20"
        with pytest.raises(SyntaxError):
            self.P1.birthdate = BD

    def test_birtdate_input_format_capture(self):
        BD = "1.2.3000"
        self.P1.birthdate = BD
        assert self.P1._birthdate.day == 1
        assert self.P1._birthdate.month == 2
        assert self.P1._birthdate.year == 3000

    # --- add_to_score ---

    def test_add_to_score(self):
        assert self.P1.score == 0
        self.P1.add_to_score(1)
        assert self.P1.score == 1
        self.P1.add_to_score(0.5)
        assert self.P1.score == 1.5
        self.P1.add_to_score(0)
        assert self.P1.score == 1.5

    def test_add_to_score_error(self):
        assert self.P1.score == 0
        with pytest.raises(ValueError):
            self.P1.add_to_score(3)

    # --- set_played ---

    def test_set_played(self):
        uid = "XX00XX"
        self.P1.set_played(uid)
        assert uid in self.P1.played_actors
        assert uid[:-1] not in self.P1.played_actors

    # --- has played ---

    def has_played(self):
        uid = "XX00XX"
        self.P1.set_played(uid)
        assert self.P1.has_played(uid) is True
        assert self.P1.has_played(uid[:-1]) is False

    # --- one_line ---

    def test_one_line_format(self):
        assert type(self.P1.one_line()) == str

    def test_one_line_content(self):
        oneline = self.P1.one_line()
        assert "Name1" in oneline
        assert "Nickname1" in oneline
        assert "1380" in oneline
        assert "H" in oneline

    # --- serialize ---

    def test_serialize_format(self):
        assert type(self.P1.serialize()) == dict

    # TODO ?
