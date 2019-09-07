#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Puzzle Solver for Advent of Code 2015 Day 14
Author: James Walker
Copyright: MIT license

Description (https://adventofcode.com/2015/day/14):
--- Day 14: Reindeer Olympics ---

  This year is the Reindeer Olympics! Reindeer can fly at high speeds, but must
  rest occasionally to recover their energy. Santa would like to know which of
  his reindeer is fastest, and so he has them race.

  Reindeer can only either be flying (always at their top speed) or resting
  (not moving at all), and always spend whole seconds in either state.

  For example, suppose you have the following Reindeer:
    Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
    Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.

    After one second, Comet has gone 14 km, while Dancer has gone 16 km. After
    ten seconds, Comet has gone 140 km, while Dancer has gone 160 km. On the
    eleventh second, Comet begins resting (staying at 140 km), and Dancer
    continues on for a total distance of 176 km. On the 12th second, both
    reindeer are resting. They continue to rest until the 138th second, when
    Comet flies for another ten seconds. On the 174th second, Dancer flies for
    another 11 seconds.

  In this example, after the 1000th second, both reindeer are resting, and
  Comet is in the lead at 1120 km (poor Dancer has only gotten 1056 km by that
  point). So, in this situation, Comet would win (if the race ended at 1000
  seconds).

  Given the descriptions of each reindeer (in your puzzle input), after exactly
  2503 seconds, what distance has the winning reindeer traveled?
    Answer: 2696

--- Day 14: Part Two ---

  Seeing how reindeer move in bursts, Santa decides he's not pleased with the
  old scoring system.

  Instead, at the end of each second, he awards one point to the reindeer
  currently in the lead. (If there are multiple reindeer tied for the lead,
  they each get one point.) He keeps the traditional 2503 second time limit, of
  course, as doing otherwise would be entirely ridiculous.

  Given the example reindeer from above, after the first second, Dancer is in
  the lead and gets one point. He stays in the lead until several seconds into
  Comet's second burst: after the 140th second, Comet pulls into the lead and
  gets his first point. Of course, since Dancer had been in the lead for the
  139 seconds before that, he has accumulated 139 points by the 140th second.

  After the 1000th second, Dancer has accumulated 689 points, while poor Comet,
  our old champion, only has 312. So, with the new scoring system, Dancer would
  win (if the race ended at 1000 seconds).

  Again given the descriptions of each reindeer (in your puzzle input), after
  exactly 2503 seconds, how many points does the winning reindeer have?
    Answer: 1084
"""

# Standard Library Imports
from collections import namedtuple
import re

# Application-specific Imports
from advent_of_code.solvers import solver


# Namedtuple for storing reindeer flight metadata
Reindeer = namedtuple('Reindeer', 'flight_speed flight_time rest_time')


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 14: Knights of the Dinner Tables

    Attributes:
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
        time_limit (int): Maximum number of seconds for the race (i.e., 2503)
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The fastest reindeer travelled {0} km after 2503 seconds.',
            'The winning reindeer had {1} points after 2503 seconds.',
        ))

    @property
    def time_limit(self):
        """Return the time limit for counting race points

        Args: None
        Returns:
            int: Total number of seconds for the reindeer race
        """
        return 2503

    def _parse_input(self):
        """Parses reindeer names and flight metadata from the puzzle input

        Args: None
        Returns:
            dict: Maps names to Reindeer namedtuples storing flight stats
        """
        parser = re.compile(r'(\w+)\D+(\d+)\D+(\d+)\D+(\d+)')
        reindeer = {}
        for line in self.puzzle_input.splitlines():
            instruction = parser.match(line)
            if not instruction:
                continue
            name, speed, flight, rest = instruction.groups()
            reindeer[name] = Reindeer(int(speed), int(flight), int(rest))
        return reindeer

    @staticmethod
    def _get_distance(reindeer, race_time):
        """Calculates the current distance traveled by the reindeer in the race

        Args:
            reindeer (Reindeer): Namedtuple storing reindeer flight metadata
            race_time (int): Number of seconds since the race started
        Returns:
            int: Current distance traveled by the reindeer in the race
        """
        interval = reindeer.flight_time + reindeer.rest_time
        cycles = race_time // interval
        flight_time = min(reindeer.flight_time, race_time - interval * cycles)
        total_flying_time = reindeer.flight_time * cycles + flight_time
        return total_flying_time * reindeer.flight_speed

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        reindeer = self._parse_input()
        race_points = {name: 0 for name in reindeer}
        max_distance = 0
        for time_elapsed in range(1, self.time_limit + 1):
            distances = {
                name: Solver._get_distance(reindeer[name], time_elapsed)
                for name in reindeer
            }
            max_distance = max(distances.values())
            race_points.update({
                name: race_points[name] + 1
                for name in race_points if distances[name] == max_distance
            })
        return max_distance, max(race_points.values())

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        line = (
            '{reindeer} can fly {speed} km/s for {time} seconds'
            ', but then must rest for {rest} seconds.'
        )
        inputs = (
            line.format(reindeer='Comet', speed=14, time=10, rest=127),
            line.format(reindeer='Dancer', speed=16, time=11, rest=162),
            line.format(reindeer='Vixen', speed=18, time=12, rest=207),
            line.format(reindeer='Prancer', speed=20, time=13, rest=264),
        )
        test_cases = (
            solver.TestCase('\n'.join(inputs[:1]), 2660, 2503),
            solver.TestCase('\n'.join(inputs[:2]), 2660, 1564),
            solver.TestCase('\n'.join(inputs[:3]), 2660, 1101),
            solver.TestCase('\n'.join(inputs), 2660, 994),
            solver.TestCase('\n'.join(inputs[1:]), 2640, 1201),
            solver.TestCase('\n'.join(inputs[2:]), 2592, 1517),
            solver.TestCase('\n'.join(inputs[3:]), 2540, 2503),
        )
        for test_case in test_cases:
            self._run_test_case(test_case)
