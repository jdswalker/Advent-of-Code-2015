#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Puzzle Solver for Advent of Code 2015 Day 13
Author: James Walker
Copyright: MIT license

Description (https://adventofcode.com/2015/day/13):
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
import sys

# Application-specific Imports
from advent_of_code.solvers import solver


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 13: Knights of the Dinner Tables

    Attributes:
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
    def _get_seat_pair(guest1, guest2):
        """Returns an alphabetically ordered tuple of the guests' names

        Args:
            guest1 (str): Name of first guest in seat pair
            guest2 (str): Name of second guest in seat pair
        Returns:
            tuple: Alphabetically ordered pair of guest names
        """
        return (guest1, guest2) if guest1 < guest2 else (guest2, guest1)

    def _parse_input(self):
        """Parses lines of input into seat pair preferences

        Args: None
        Returns:
            tuple: List of attendees and dict of seat pair preferences
        """
        attendees, seat_pairs = set(), {}
        for line in self.puzzle_input.splitlines():
            if not line:
                continue
            tokens = line.split()
            seat_pair = self._get_seat_pair(tokens[0], tokens[-1][:-1])
            if seat_pair not in seat_pairs:
                seat_pairs[seat_pair] = 0
                attendees.update(seat_pair)
            if tokens[2] == 'gain':
                seat_pairs[seat_pair] += int(tokens[3])  # Happiness
            else:
                seat_pairs[seat_pair] -= int(tokens[3])
        return attendees, seat_pairs

    def _get_seating_plan(self, first_guest, other_guests):
        """Creates a tuple of seat pairs as a seating arrangement for the table

        Args:
            first_guest (str): First guest assigned a seat around the table
            other_guests (list): Remaining guests to assign seats
        Returns:
            tuple: Seating arrangement for the given permutation of guests
        """
        arrangement = set()
        current_guest = first_guest
        for next_guest in other_guests:
            arrangement.add(self._get_seat_pair(current_guest, next_guest))
            current_guest = next_guest
        arrangement.add(self._get_seat_pair(current_guest, first_guest))
        return tuple(sorted(arrangement))

    def _get_max_happiness(self, attendees, seat_pairs):
        """Permutes seating plans to calculate happiness and returns max value

        Args:
            attendees (list): Names of guests attending the party
            seat_pairs (dict): Seat pair keys mapped to happiness values
        Returns:
            int: Maximum happiness for a seating plan with the given guests
        """
        happiness = -sys.maxsize
        seating_plans = set()
        first_guest = attendees.pop()
        for other_guests in permutations(attendees, len(attendees)):
            seating = self._get_seating_plan(first_guest, other_guests)
            if seating not in seating_plans:
                seating_plans.add(seating)
                happiness = max(happiness, sum(seat_pairs[i] for i in seating))
        return happiness

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        attendees, seat_pairs = self._parse_input()
        max_happiness1 = self._get_max_happiness(attendees.copy(), seat_pairs)
        yourself = ''
        for attendee in attendees:
            seat_pairs[(yourself, attendee)] = 0
        attendees.add(yourself)
        max_happiness2 = self._get_max_happiness(attendees.copy(), seat_pairs)
        return (max_happiness1, max_happiness2)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        input1 = (
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
        )
        input2 = input1[0:2] + input1[3:5] + input1[6:8]
        input3 = (input1[0], input1[1].replace('Carol', 'Bob'))
        test_cases = (
            solver.TestCase('\n'.join(input1), 330, 286),
            solver.TestCase('\n'.join(input2), 49, 190),
            solver.TestCase('\n'.join(input3), -25, -25),
        )
        for test_case in test_cases:
            self._run_test_case(test_case)
