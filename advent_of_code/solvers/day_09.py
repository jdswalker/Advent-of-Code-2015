#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Puzzle Solver for Advent of Code 2015 Day 9
Author: James Walker
Copyright: MIT license

Description (https://adventofcode.com/2015/day/9):
--- Day 9: All in a Single Night ---

  Every year, Santa manages to deliver all of his presents in a single night.

  This year, however, he has some new locations to visit; his elves have
  provided him the distances between every pair of locations. He can start and
  end at any two (different) locations he wants, but he must visit each
  location exactly once. What is the shortest distance he can travel to achieve
  this?

  For example, given the following distances:
    London to Dublin = 464
    London to Belfast = 518
    Dublin to Belfast = 141

  The possible routes are therefore:
    Dublin -> London -> Belfast = 982
    London -> Dublin -> Belfast = 605
    London -> Belfast -> Dublin = 659
    Dublin -> Belfast -> London = 659
    Belfast -> Dublin -> London = 605
    Belfast -> London -> Dublin = 982

  The shortest of these is London -> Dublin -> Belfast = 605, and so the answer
  is 605 in this example.

  What is the distance of the shortest route?
    Answer: 207

--- Day 9: Part Two ---

  The next year, just to show off, Santa decides to take the route with the
  longest distance instead.

  He can still start and end at any two (different) locations he wants, and he
  still must visit each location exactly once.

  For example, given the distances above, the longest route would be 982 via
  (for example) Dublin -> London -> Belfast.

  What is the distance of the longest route?
    Answer: 804
"""

# Standard Library Imports
from itertools import permutations
import sys

# Application-specific Imports
from advent_of_code.solvers import solver


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 9: All in a Single Night

    Attributes:
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The distance for the shortest route is {0}',
            'The distance for the longest route is {1}',
        ))
        self._routes = None
        self._towns = set()

    @staticmethod
    def _get_route(town1, town2):
        """Returns the towns as a sorted tuple to use as a dictionary key

        Args:
            town1 (str): Name of the first town in the route
            town2 (str): Name of the second town in the route
        Returns:
            tuple: Sorted tuple of the town names
        """
        return (town1, town2) if town1 < town2 else (town2, town1)

    def _parse_route(self, line):
        """Splits and parses the string from a single line of input

        Args:
            line (str): Raw route information for the puzzle
        Returns:
            dict: Sorted pair of towns as the key for the route's distance
        """
        town1, _, town2, _, distance = line.split()
        self._towns.update({town1, town2})
        return {self._get_route(town1, town2): int(distance)}

    def _parse_input(self):
        """Parses lines of input into a dictionary of town routes

        Args: None
        Returns:
            dict: Pairs of towns as keys for a route distance value
        """
        routes = {}
        for line in self._puzzle_input.splitlines():
            if line:
                routes.update(self._parse_route(line))
        return routes

    def _get_cycle(self, fixed_point, sub_path):
        """Generates a directed cyclic path through every town

        Args:
            fixed_point (str): Starting point for the cycle
            sub_path (tuple): Towns that have not been visited yet
        Returns:
            tuple: Stores the path taken through every town
        """
        cycle = set()
        current_town = fixed_point
        for next_town in sub_path:
            cycle.add(self._get_route(current_town, next_town))
            current_town = next_town
        cycle.add(self._get_route(current_town, fixed_point))
        return tuple(sorted(cycle))

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        self._routes = self._parse_input()
        min_distance, max_distance = sys.maxsize, -1
        cycles = set()
        fixed_point = self._towns.pop()
        for sub_path in permutations(self._towns, len(self._towns)):
            cycle = self._get_cycle(fixed_point, sub_path)
            if cycle not in cycles:
                cycles.add(cycle)
                distances = sorted(self._routes[route] for route in cycle)
                # Part 1 of Day 9
                min_distance = min(min_distance, sum(distances[:-1]))
                # Part 2 of Day 9
                max_distance = max(max_distance, sum(distances[1:]))
        return (min_distance, max_distance)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        input1 = '\n'.join((
            'London to Dublin = 464',
            'London to Belfast = 518',
            'Dublin to Belfast = 141',
        ))
        test_cases = (solver.TestCase(input1, 605, 982),)
        for test_case in test_cases:
            self._run_test_case(test_case)
