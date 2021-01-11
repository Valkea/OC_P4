#! /usr/bin/env python3
# coding: utf-8


""" This module handles the rounds & matchs of the tournaments
"""

import datetime

from model.player import Player


class Round:
    """This class handles the chess players

    Attributes
    ----------
    name : str
    start_time : datetime.datetime
        Automatically added when creating the instance
    close_time : datetime.datetime
        Automatically added when calling the close method
    games : list
        The game instances of this round
    round_index : int
        The current round number (used to determine the rules to pairs players)
    world : Wold
        The world instance where the original players instances can be found

    Getters & Setters
    -----------------
    start_time()
        Return the starting time of the Round as a str
    start_time(v)
        Convert various date inputs to a datetime.datetime object stored in _start_time.
    close_time()
        Return the closing time of the Round as a str
    close_time(v)
        Convert various date inputs to a datetime.datetime object stored in _close_time.

    Public Methods
    --------------
    close()
        Close the round by adding the current time to close_time
    gen_games(players_id)
        Generate the games from the given player's list
    one_line(ljustv=10)
        Return a complete presentation of the round in one line
    serialize()
        Serialize the content of this class for TinyDB exports

    Static & Class Methods
    ----------------------
    _get_games(players_id)
        Actually the pairing process takes place in here not in gen_games()
    _get_time()
        Return the current date as a datetime.datetime

    Static & Class Methods
    ----------------------
    convert_score_symbol(symbol)
        Convert the symbols <, > and = to (1,0), (0,1) and (.5,.5)
    list_rounds(tournament)
        Return tuples containing the provided tournament Rounds
    list_games(tournament, world)
        Return tuples containing the provided tournament Round/games
    """

    def __init__(
        self,
        world,
        name,
        round_index,
        players_id,
        games=None,
        start_time=None,
        close_time=None,
    ):
        self.name = name
        self.start_time = start_time if start_time is not None else self._get_time()
        self.close_time = close_time
        self.games = games if games is not None else []
        self.round_index = round_index
        self.world = world

        if start_time is None:
            self.gen_games(players_id)

    # === GETTERS & SETTERS ===

    @property
    def start_time(self):
        if self._start_time is None:
            return None
        return self._start_time.strftime("%d/%m/%Y %H:%M:%S")

    @start_time.setter
    def start_time(self, v):
        if type(v) is datetime.datetime or v is None:
            self._start_time = v
        else:
            self._start_time = datetime.datetime.strptime(v, "%m/%d/%Y %H:%M:%S")

    @property
    def close_time(self):
        if self._close_time is None:
            return None
        return self._close_time.strftime("%d/%m/%Y %H:%M:%S")

    @close_time.setter
    def close_time(self, v):
        if type(v) is datetime.datetime or v is None:
            self._close_time = v
        else:
            self._close_time = datetime.datetime.strptime(v, "%m/%d/%Y %H:%M:%S")

    # === PUBLIC METHODS ===

    def close(self):
        """ Close the round by adding the current time to close_time. """

        self.close_time = self._get_time()

    def gen_games(self, players_id):
        """" Generate the games from the given player's list. """

        paired_players = self._get_games(players_id)

        for p1, p2 in paired_players:
            self.games.append(([p1, 0], [p2, 0]))

    def one_line(self, ljustv=10):
        """Return a complete presentation of the round in one line.

        Parameters
        ----------
        ljustv : int(10)
            The minimum of space taken by the round name (ensure alignement)
        """

        if self.close_time is not None:
            return (
                f"{self.name.ljust(ljustv)} | "
                + f"Joué du {self.start_time} "
                + f"au {self.close_time}"
            )
        else:
            return f"{self.name.ljust(ljustv)} | " + f"Commencé le {self.start_time}"

    def serialize(self):
        """ Return a JSON representation of the Round instance """

        return {
            # "id": id(self),
            "name": self.name,
            "start_time": self.start_time,
            "close_time": self.close_time,
            # "games": [str(type(x)) for x in self.games],
            "games": self.games,
            "round_index": self.round_index,
        }

    # === PRIVATE METHODS ===

    def _get_games(self, players_id):
        """Actually the pairing process takes place in here not in gen_games().

        Parameters
        ----------
        players_id : list(str)
            The list of the uid attribute of the participants
        """

        sorted_players = Player.multisort(
            self.world.get_actors(), Player.get_sort_key("score")
        )

        pairs = []
        if self.round_index == 0:
            half = len(players_id) // 2
            part1 = [p.uid for p in sorted_players[:half]]
            part2 = [p.uid for p in sorted_players[half:]]
            for pair in zip(part1, part2):
                pairs.append(pair)
        else:
            drafted = []
            for i, player1 in enumerate(sorted_players):
                for player2 in sorted_players[i:]:

                    if (
                        player1.uid == player2.uid
                        or player1.uid in drafted
                        or player2.uid in drafted
                    ):
                        continue

                    if player1.has_played(player2.uid) is not True:
                        pairs.append((player1.uid, player2.uid))
                        drafted.extend([player1.uid, player2.uid])
                        break
        return pairs

    def _get_time(self):
        """ Return the current date as a datetime.datetime. """

        return datetime.datetime.now()

    # def __repr__(self):
    #    return f"Round('{self.name}', {self.start_time}, {self.close_time})"

    # === STATIC & CLASS METHODS ===

    @staticmethod
    def convert_score_symbol(symbol):
        """Convert the symbols <, > and = to (1,0), (0,1) and (.5,.5).

        Return
        ------
        tuple containing two value
        """

        if symbol == ">":
            return (0, 1)

        elif symbol == "<":
            return (1, 0)

        elif symbol == "=":
            return (0.5, 0.5)

    # --- Generate list for Curses views ---

    @staticmethod
    def list_rounds(tournament):
        """Return tuples containing the provided tournament Rounds.

        Parameters
        ----------
        tournament: Tournament
            The instance of the tournament
        """

        rounds = tournament.rounds
        if len(rounds) > 0:
            retv = [(f" {round.one_line()} ", None) for round in rounds]
            return tuple(retv)
        else:
            return (("Le tournoi n'est pas commencé", "go_back"),)

    @staticmethod
    def list_games(tournament, world):
        """Return tuples containing the provided tournament Round/games.

        Parameters
        ----------
        tournament: Tournament
            The instance of the tournament
        world : World
            the world instance containing all tournament's and player's instances
        """

        rounds = tournament.rounds
        if len(rounds) > 0:

            retv = []
            for r in rounds:

                retv.append(("", None))
                retv.append((f" {r.name} ", None))

                for i, game in enumerate(r.games):

                    player1 = world.get_actor(game[0][0])
                    player2 = world.get_actor(game[1][0])

                    score1 = game[0][1]
                    score2 = game[1][1]

                    retv.append(
                        (
                            f"({player1.one_line(age=False, sex=False, score=False, extra=f'PTS:{score1:3}')}) vs "
                            + f"({player2.one_line(age=False, sex=False, score=False, extra=f'PTS:{score2:3}')})",
                            None,
                        )
                    )

            return tuple(retv)
        else:
            return (("Le tournoi n'est pas commencé", "go_back"),)


# class Game:
#     """This class handles the games
#
#     Attributes
#     ----------
#     TODO
#
#     Methods
#     -------
#     get_tuple()
#         return the game as a tuple ([Player1, Score1],[Player2, Score2])
#     """
#
#     def __init__(self, player1, player2, score1=0, score2=0):
#         self.player1 = player1
#         self.player2 = player2
#
#         self.score1 = score1
#         self.score2 = score2
#
#     def setScore(self, score1, score2):
#         self.score1 = score1
#         self.score2 = score2
#
#     def __repr__(self):
#         return ([self.player1, self.score1], [self.player2, self.score2])
#
#     def serialize(self):
#         """ Return a JSON representation of the Game instance """
#         return {
#             "id": id(self),
#             "player1": id(self.player1),
#             "score1": self.score1,
#             "player2": id(self.player1),
#             "score2": self.score2,
#         }
