#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/14
Author: James Walker
Copyrighted 2018 under the MIT license:
  http://www.opensource.org/licenses/mit-license.php

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


FlightStats = namedtuple('FlightStats', 'flight_speed flight_time rest_time')


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 14: Knights of the Dinner Tables

    Attributes
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The fastest reindeer travelled {0} km after 2503 seconds.',
            'The winning reindeer had {1} points after 2503 seconds.',
        ))

    def _parse_input(self):
        """

        Args: None
        Returns:
            dict:
        """
        parser = re.compile(r'(\w+)\D+(\d+)\D+(\d+)\D+(\d+)')
        reindeer = {}
        for line in self.puzzle_input.splitlines():
            instruction = parser.match(line)
            if not instruction:
                continue
            name = instruction.group(1)
            flight_speed = int(instruction.group(2))
            flight_time = int(instruction.group(3))
            rest_time = int(instruction.group(4))
            reindeer[name] = FlightStats(flight_speed, flight_time, rest_time)
        return reindeer

    @staticmethod
    def _get_fly_distance(reindeer, race_time):
        """

        Args:
            reindeer
            race_time
        Returns:
            int:
        """
        flight_interval = reindeer.flight_time + reindeer.rest_time
        num_intervals = int(race_time / flight_interval)
        time_remaining = race_time - (num_intervals * flight_interval)
        total_flight_time = reindeer.flight_time * num_intervals
        if time_remaining < reindeer.flight_time:
            total_flight_time += time_remaining
        else:
            total_flight_time += reindeer.flight_time
        return total_flight_time * reindeer.flight_speed

    def _get_reindeer_distances(self, reindeer, race_time):
        """

        Args:
            reindeer
            race_time
        Returns:
            tuple:
        """
        winning_distance = 0
        distances = {}
        for name in reindeer:
            distances[name] = self._get_fly_distance(reindeer[name], race_time)
            if winning_distance < distances[name]:
                winning_distance = distances[name]
        return (distances, winning_distance)

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        race_time = 2503
        reindeer = self._parse_input()
        race_points = {name: 0 for name in reindeer}
        farthest_distance = 0
        for partial_time in range(1, race_time + 1):
            distances, farthest_distance = self._get_reindeer_distances(
                reindeer,
                partial_time,
            )
            for name in reindeer:
                if distances[name] == farthest_distance:
                    race_points[name] += 1

        return (farthest_distance, max(race_points.values()))

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        test_input = '\n'.join(((
            'Comet can fly 14 km/s for 10 seconds'
            ', but then must rest for 127 seconds.'
        ), (
            'Dancer can fly 16 km/s for 11 seconds'
            ', but then must rest for 162 seconds.'
        )))
        self._run_test_case(solver.TestCase(test_input, 2660, 1564))
