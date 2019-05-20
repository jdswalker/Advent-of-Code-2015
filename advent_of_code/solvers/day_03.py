#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/3
Author: James Walker
Copyright: MIT license

--- Day 3: Perfectly Spherical Houses in a Vacuum ---

  Santa is delivering presents to an infinite two-dimensional grid of houses.

  He begins by delivering a present to the house at his starting location, and
  then an elf at the North Pole calls him via radio and tells him where to move
  next. Moves are always exactly one house to the north (^), south (v),
  east (>), or west (<). After each move, he delivers another present to the
  house at his new location.

  However, the elf back at the north pole has had a little too much eggnog, and
  so his directions are a little off, and Santa ends up visiting some houses
  more than once.

  For example:
    > delivers presents to 2 houses: one at the starting location, and one to
      the east.
    ^>v< delivers presents to 4 houses in a square, including twice to the
      house at his starting/ending location.
    ^v^v^v^v^v delivers a bunch of presents to some very lucky children at only
      2 houses.

  How many houses receive at least one present?
    Answer: 2565

--- Day 3: Part Two ---

  The next year, to speed up the process, Santa creates a robot version of
  himself, Robo-Santa, to deliver presents with him.

  Santa and Robo-Santa start at the same location (delivering two presents to
  the same starting house), then take turns moving based on instructions from
  the elf, who is eggnoggedly reading from the same script as the previous
  year.

  For example:
    ^v delivers presents to 3 houses, because Santa goes north, and then
      Robo-Santa goes south.
    ^>v< now delivers presents to 3 houses, and Santa and Robo-Santa end up
      back where they started.
    ^v^v^v^v^v now delivers presents to 11 houses, with Santa going one
      direction and Robo-Santa going the other.

  This year, how many houses receive at least one present?
    Answer: 2639
"""

# Standard Library Imports
from collections import namedtuple

# Application-specific Imports
from advent_of_code.solvers import solver


# Stores Santa's location as x and y coorindates
Location = namedtuple('Location', 'x y')


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 3: Perfectly Spherical Houses in a Vacuum

    Attributes
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
        moves (dict): Relative coordinates for each move instruction
        santa (Location): Stores coordinates for Santa's location
        robo_santa (Location): Stores coordinates for Robo-Santa's location
        house_tracker (dict): Stores counts of location visits by Santa
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The first year, Santa drops off presents at {0} houses.',
            'The second year, presents are dropped off at {1} houses.',
        ))
        self._moves = {
            '^': Location(1, 0),
            '>': Location(0, 1),
            'v': Location(-1, 0),
            '<': Location(0, -1),
        }
        self._santa = None
        self._robo_santa = None
        self._house_tracker = None

    def _check_if_visited(self, location):
        """Checks if a house has been visited and updates the house tracker

        Args:
            location (Location): A tuple with Santa's x and y coorindates
        Returns: None
        """
        if location not in self._house_tracker:
            self._house_tracker[location] = 0
        self._house_tracker[location] += 1

    def _get_next_location(self, location, move):
        """Updates the coordinate position of one of the two Santa's

        Args:
            location (Location): A tuple with Santa's x and y coorindates
            move (str): A single move from the puzzle input
        Returns:
            Location: A tuple with Santa's new x and y coorindates
        """
        next_location = None
        if move in self._moves:
            new_x = location.x + self._moves[move].x
            new_y = location.y + self._moves[move].y
            next_location = Location(new_x, new_y)
        return next_location

    def _update_position(self, location, move_santa=True):
        """Updates the coordinate position of one of the two Santa's

        Args:
            location (Location): A tuple with Santa's x and y coorindates
            move_santa (bool): Update Santa if True, else update Robot Santa
        Returns: None
        """
        if move_santa:
            self._santa = location
        else:
            self._robo_santa = location

    def _solve_puzzle_part_one(self):
        """Solves one part of the current Advent of Code 2015 puzzle

        Args: None
        Returns:
            int: Number of houses visited by the real Santa
        """
        self._reset_puzzle()
        self._house_tracker[self._santa] = 1
        for move in self._puzzle_input:
            location = self._get_next_location(self._santa, move)
            if location is not None:
                self._update_position(location)
                self._check_if_visited(location)
        return len(self._house_tracker)

    def _solve_puzzle_part_two(self):
        """Solves one part of the current Advent of Code 2015 puzzle

        Args: None
        Returns:
            int: Number of houses visited by both Santas
        """
        self._reset_puzzle()
        self._house_tracker[self._santa] = 1
        self._check_if_visited(self._robo_santa)
        move_santa = True
        for move in self._puzzle_input:
            location = None
            if move_santa:
                location = self._get_next_location(self._santa, move)
            else:
                location = self._get_next_location(self._robo_santa, move)
            if location is not None:
                self._update_position(location, move_santa)
                move_santa = not move_santa
                self._check_if_visited(location)
        return len(self._house_tracker)

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        part_one_answer = self._solve_puzzle_part_one()
        part_two_answer = self._solve_puzzle_part_two()
        return (part_one_answer, part_two_answer)

    def _reset_puzzle(self):
        """Reinitializes Santa's position and the house coordinate tracker

        Args: None
        Returns: None
        """
        self._santa = Location(0, 0)
        self._robo_santa = Location(0, 0)
        self._house_tracker = {}

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        test_cases = (
            solver.TestCase('>', 2, 2),
            solver.TestCase('^v', 2, 3),
            solver.TestCase('^>v<', 4, 3),
            solver.TestCase('^v^v^v^v^v', 2, 11),
        )
        for test_case in test_cases:
            self._run_test_case(test_case)
