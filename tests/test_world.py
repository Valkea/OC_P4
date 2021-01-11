#! /usr/bin/env python3
# coding: utf-8

"""
The purpose of this module is to test the Round class
"""

import pytest

from model.world import World, NoActiveTournamentError, UnregisteredTournamentError
from model.player import Player
from model.tournament import Tournament


class TestWorld:
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

    # --- add tournament ---

    def test_add_tournament_valid(self):
        assert len(World.tournaments) == 0
        World.add_tournament(self.T1)
        assert len(World.tournaments) == 1

    def test_add_tournament_not_valid(self):
        assert len(World.tournaments) == 0
        with pytest.raises(TypeError):
            World.add_tournament("Invalid Tournament")
        assert len(World.tournaments) == 0

    # --- set active tournament ---

    def test_set_active_tournament_valid(self):
        World.add_tournament(self.T1)
        World.set_active_tournament(self.T1)
        assert World.active_tournament == self.T1

    def test_set_active_tournament_not_valid(self):
        with pytest.raises(TypeError):
            World.set_active_tournament("Invalid Tournament")
        assert World.active_tournament is None

    def test_set_active_unregistered_tournament(self):
        with pytest.raises(UnregisteredTournamentError):
            World.set_active_tournament(self.T1)
        assert World.active_tournament is None

    # --- get active tournament ---

    def test_get_active_tournament_valid(self):
        World.add_tournament(self.T1)
        World.set_active_tournament(self.T1)
        assert World.get_active_tournament() == self.T1

    # --- add actors ---

    def test_add_actor_valid_with_T_param(self):
        assert len(World.actors) == 0
        World.add_actor(self.P1, self.T1)
        assert len(World.actors) == 1

    def test_add_actor_valid_with_T_active(self):
        World.add_tournament(self.T1)
        World.set_active_tournament(self.T1)
        assert len(World.actors) == 0
        World.add_actor(self.P1)
        assert len(World.actors) == 1

    def test_add_actor_without_T_param_or_T_active(self):
        assert len(World.actors) == 0
        with pytest.raises(NoActiveTournamentError):
            World.add_actor(self.P1)
        assert len(World.actors) == 0

    def test_add_actor_unvalid(self):
        assert len(World.actors) == 0
        with pytest.raises(TypeError):
            World.add_actor("Invalid actor")
        assert len(World.actors) == 0

    def test_add_actors_in_serpate_tournaments(self):

        World.add_tournament(self.T1)
        World.add_tournament(self.T2)

        assert len(World.actors) == 0
        assert len(World.get_actors(self.T1)) == 0
        assert len(World.get_actors(self.T2)) == 0

        World.add_actor(self.P1, self.T1)
        World.add_actor(self.P2, self.T2)

        assert len(World.actors) == 2
        assert len(World.get_actors(self.T1)) == 1
        assert len(World.get_actors(self.T2)) == 1

    # --- get actors ---

    def test_get_actor_valid(self):
        World.add_actor(self.P1, self.T1)
        assert World.get_actor(self.P1.uid) == self.P1

    def test_get_actor_unvalid(self):
        World.add_actor(self.P1, self.T1)
        assert World.get_actor(self.P2.uid) != self.P1

    def test_get_actor_unvalid_param(self):
        World.add_actor(self.P1, self.T1)
        with pytest.raises(TypeError):
            World.get_actor(36)

    # --- get tournament actors ---

    def test_get_actors_valid(self):
        World.add_tournament(self.T1)
        World.set_active_tournament(self.T1)
        assert len(World.actors) == 0

        World.add_actor(self.P1)
        World.add_actor(self.P2)
        assert len(World.actors) == 2

        actors = World.get_actors(self.T1)
        assert len(actors) == 2
        assert actors[0] == self.P1
        assert actors[1] == self.P2

    def test_get_actors_valid_no_T_param_but_T_active(self):
        World.add_tournament(self.T1)
        World.set_active_tournament(self.T1)
        assert len(World.actors) == 0

        World.add_actor(self.P1)
        World.add_actor(self.P2)
        assert len(World.actors) == 2

        actors = World.get_actors()
        assert len(actors) == 2
        assert actors[0] == self.P1
        assert actors[1] == self.P2

    def test_get_actors_valid_no_T_param_and_no_T_active(self):
        World.add_tournament(self.T1)
        assert len(World.actors) == 0

        World.add_actor(self.P1, self.T1)
        World.add_actor(self.P2, self.T1)
        assert len(World.actors) == 2

        with pytest.raises(NoActiveTournamentError):
            World.get_actors()

    # --- get all actors ---

    def test_get_all_actors_valid(self):
        World.add_tournament(self.T1)
        World.add_tournament(self.T2)
        assert len(World.actors) == 0
        assert len(World.get_actors(self.T1)) == 0
        assert len(World.get_actors(self.T2)) == 0
        assert len(World.get_all_actors()) == 0

        World.add_actor(self.P1, self.T1)
        World.add_actor(self.P2, self.T2)

        assert len(World.actors) == 2
        assert len(World.get_actors(self.T1)) == 1
        assert len(World.get_actors(self.T2)) == 1
        assert len(World.get_all_actors()) == 2

        actors = World.get_all_actors()
        assert actors[0] == self.P1
        assert actors[1] == self.P2


class TestRound:
    @classmethod
    def setup_class(cls):
        # P1 = Player("P1", "p", "1.1.1979", "M", 1380)
        # P2 = Player("P2", "p", "1.1.1979", "M", 2120)
        # P3 = Player("P3", "p", "1.1.1979", "M", 1612)
        # P4 = Player("P4", "p", "1.1.1979", "M", 999)
        # P5 = Player("P5", "p", "1.1.1979", "M", 1720)
        # P6 = Player("P6", "p", "1.1.1979", "M", 2000)
        # P7 = Player("P7", "p", "1.1.1979", "M", 230)
        # P8 = Player("P8", "p", "1.1.1979", "M", 3000)

        # t01 = Tournament(World, "Tournament Test 01", "TestAre", "01.01.2020", "02.01.2020", "bullet", "")
        # World.set_active_tournament(t01)

        # World.add_actor(P1)
        # World.add_actor(P2)
        # World.add_actor(P3)
        # World.add_actor(P4)
        # World.add_actor(P5)
        # World.add_actor(P6)
        # World.add_actor(P7)
        # World.add_actor(P8)

        # players_id = [p.uid for p in World.get_actors(t01)]

        # cls.round1 = Round(World, "fake_name", 0, players_id)
        pass

    @classmethod
    def teardown_class(cls):
        pass

    # --- Incoming Getters & Setters ---

    def test_name(self):
        self.name = "fake-name"
        assert self.name == "fake-name"
