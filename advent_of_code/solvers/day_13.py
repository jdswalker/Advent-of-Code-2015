#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/13
Author: James Walker
Copyright: MIT license

--- Day 13: Knights of the Dinner Table ---

  In years past, the holiday feast with your family hasn't gone so well. Not
  everyone gets along! This year, you resolve, will be different. You're going
  to find the optimal seating arrangement and avoid all those awkward
  conversations.

  You start by writing up a list of everyone invited and the amount their
  happiness would increase or decrease if they were to find themselves sitting
  next to each other person. You have a circular table that will be just big
  enough to fit everyone comfortably, and so each person will have exactly two
  neighbors.

  For example, suppose you have only four attendees planned, and you calculate
  their potential happiness as follows:
    Alice would gain 54 happiness units by sitting next to Bob.
    Alice would lose 79 happiness units by sitting next to Carol.
    Alice would lose 2 happiness units by sitting next to David.
    Bob would gain 83 happiness units by sitting next to Alice.
    Bob would lose 7 happiness units by sitting next to Carol.
    Bob would lose 63 happiness units by sitting next to David.
    Carol would lose 62 happiness units by sitting next to Alice.
    Carol would gain 60 happiness units by sitting next to Bob.
    Carol would gain 55 happiness units by sitting next to David.
    David would gain 46 happiness units by sitting next to Alice.
    David would lose 7 happiness units by sitting next to Bob.
    David would gain 41 happiness units by sitting next to Carol.

  Then, if you seat Alice next to David, Alice would lose 2 happiness units
  (because David talks so much), but David would gain 46 happiness units
  (because Alice is such a good listener), for a total change of 44.

  If you continue around the table, you could then seat Bob next to Alice (Bob
  gains 83, Alice gains 54). Finally, seat Carol, who sits next to Bob (Carol
  gains 60, Bob loses 7) and David (Carol gains 55, David gains 41). The
  arrangement looks like this:

         +41 +46
    +55   David    -2
    Carol       Alice
    +60    Bob    +54
         -7  +83

  After trying every other seating arrangement in this hypothetical scenario,
  you find that this one is the most optimal, with a total change in happiness
  of 330.

  What is the total change in happiness for the optimal seating arrangement of
  the actual guest list?

    Answer: 618

--- Day 13: Part Two ---

  In all the commotion, you realize that you forgot to seat yourself. At this
  point, you're pretty apathetic toward the whole thing, and your happiness
  wouldn't really go up or down regardless of who you sit next to. You assume
  everyone else would be just as ambivalent about sitting next to you, too.

  So, add yourself to the list, and give all happiness relationships that
  involve you a score of 0.

  What is the total change in happiness for the optimal seating arrangement
  that actually includes yourself?

    Answer: 601
"""

# Standard Library Imports
from itertools import permutations
import re
import sys

# Application-specific Imports
from advent_of_code.solvers import solver


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 13: Knights of the Dinner Tables

    Attributes
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The total change in happiness for the first arrangement is {0}',
            'The total change in happiness for the second arrangement is {1}',
        ))

    @staticmethod
    def _get_seat_pair(seat1, seat2):
        """

        Args:
            seat1
            seat2
        Returns:
            tuple:
        """
        return (seat1, seat2) if seat1 < seat2 else (seat2, seat1)

    @staticmethod
    def _parse_happiness(pairing):
        """

        Args:
            pairing
        Returns:
            int:
        """
        happiness = int(pairing.group(3))
        return happiness if pairing.group(2) != 'lose' else -1 * happiness

    def _parse_input(self):
        """

        Args: None
        Returns:
            tuple:
        """
        attendees = set()
        seat_pairs = {}
        seat_pair_pattern = (
            r'(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+)'
        )
        parser = re.compile(seat_pair_pattern)
        for line in self.puzzle_input.splitlines():
            pairing = parser.match(line)
            if pairing:
                seat1, seat2 = pairing.group(1), pairing.group(4)
                happiness = self._parse_happiness(pairing)
                seat_pair = self._get_seat_pair(seat1, seat2)
                if seat_pair not in seat_pairs:
                    seat_pairs[seat_pair] = 0
                    attendees.add(seat_pair[0])
                    attendees.add(seat_pair[1])
                seat_pairs[seat_pair] += happiness
        return (attendees, seat_pairs)

    def _get_seating_plan(self, first_seat, other_seats):
        """

        Args:
            first_seat
            other_seats
        Returns:
            tuple:
        """
        arrangement = set()
        current_seat = first_seat
        for next_seat in other_seats:
            arrangement.add(self._get_seat_pair(current_seat, next_seat))
            current_seat = next_seat
        arrangement.add(self._get_seat_pair(current_seat, first_seat))
        return tuple(sorted(arrangement))

    def _get_max_happiness(self, attendees, seat_pairs):
        """

        Args:
            attendees
            seat_pairs
        Returns:
            int:
        """
        max_happiness = -sys.maxsize
        seating_plans = set()
        first_seat = attendees.pop()
        for other_seats in permutations(attendees, len(attendees)):
            arrangement = self._get_seating_plan(first_seat, other_seats)
            if arrangement not in seating_plans:
                seating_plans.add(arrangement)
                happiness_sum = sum(seat_pairs[pair] for pair in arrangement)
                max_happiness = max(max_happiness, happiness_sum)
        return max_happiness

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        attendees, seat_pairs = self._parse_input()
        max_happiness1 = self._get_max_happiness(attendees.copy(), seat_pairs)
        mr_nobody = ''
        for attendee in attendees:
            seat_pairs[self._get_seat_pair(mr_nobody, attendee)] = 0
        attendees.add(mr_nobody)
        max_happiness2 = self._get_max_happiness(attendees.copy(), seat_pairs)
        return (max_happiness1, max_happiness2)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        preferences = '\n'.join((
            'Alice would gain 54 happiness units by sitting next to Bob.',
            'Alice would lose 79 happiness units by sitting next to Carol.',
            'Alice would lose 2 happiness units by sitting next to David.',
            'Bob would gain 83 happiness units by sitting next to Alice.',
            'Bob would lose 7 happiness units by sitting next to Carol.',
            'Bob would lose 63 happiness units by sitting next to David.',
            'Carol would lose 62 happiness units by sitting next to Alice.',
            'Carol would gain 60 happiness units by sitting next to Bob.',
            'Carol would gain 55 happiness units by sitting next to David.',
            'David would gain 46 happiness units by sitting next to Alice.',
            'David would lose 7 happiness units by sitting next to Bob.',
            'David would gain 41 happiness units by sitting next to Carol.',
        ))
        self._run_test_case(solver.TestCase(preferences, 330, 286))
