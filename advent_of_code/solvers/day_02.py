#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Puzzle Solver for Advent of Code 2015 Day 2
Author: James Walker
Copyright: MIT license

Description (https://adventofcode.com/2015/day/2):
--- Day 2: I Was Told There Would Be No Math ---

  The elves are running low on wrapping paper, and so they need to submit an
  order for more. They have a list of the dimensions (length l, width w, and
  height h) of each present, and only want to order exactly as much as they
  need.

  Fortunately, every present is a box (a perfect right rectangular prism),
  which makes calculating the required wrapping paper for each gift a little
  easier: find the surface area of the box, which is 2*l*w + 2*w*h + 2*h*l.
  The elves also need a little extra paper for each present: the area of the
  smallest side.

  For example:
    A present with dimensions 2x3x4 requires
      2*6 + 2*12 + 2*8 = 52 square feet of wrapping paper plus 6 square feet of
      slack, for a total of 58 square feet.
    A present with dimensions 1x1x10 requires
      2*1 + 2*10 + 2*10 = 42 square feet of wrapping paper plus 1 square foot
      of slack, for a total of 43 square feet.

  All numbers in the elves' list are in feet. How many total square feet of
  wrapping paper should they order?
    Answer: 1,586,300

--- Day 2: Part Two ---

  The elves are also running low on ribbon. Ribbon is all the same width, so
  they only have to worry about the length they need to order, which they would
  again like to be exact.

  The ribbon required to wrap a present is the shortest distance around its
  sides, or the smallest perimeter of any one face. Each present also requires
  a bow made out of ribbon as well; the feet of ribbon required for the perfect
  bow is equal to the cubic feet of volume of the present. Don't ask how they
  tie the bow, though; they'll never tell.

  For example:
    A present with dimensions 2x3x4 requires
      2+2+3+3 = 10 feet of ribbon to wrap the present plus 2*3*4 = 24 feet of
      ribbon for the bow, for a total of 34 feet.
    A present with dimensions 1x1x10 requires
      1+1+1+1 = 4 feet of ribbon to wrap the present plus 1*1*10 = 10 feet of
      ribbon for the bow, for a total of 14 feet.

  How many total feet of ribbon should they order?
    Answer: 3,737,498
"""

# Standard Library Imports
from collections import namedtuple

# Application-specific Imports
from advent_of_code.solvers import solver


# Stores the dimensions of a present
Present = namedtuple('Present', 'length width height')


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 2: I Was Told There Would Be No Math

    Attributes
        file_name (str): The name of the file storing the puzzle input
        puzzle_title (str): Name of the Advent of Code puzzle
        puzzle_input (list): A list of instructions for solving the puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The elves should order {0} feet of wrapping paper',
            'and {1} feet of ribbon.',
        ))

    @staticmethod
    def _calculate_square_footage(present):
        """Calculates the square footage of wrapping paper for the present

        Args:
            present (Present): A namedtuple with the dimensions of the present
        Returns:
            int: The square footage needed to wrap the present
        """
        surface_areas = (
            present.length * present.width,
            present.width * present.height,
            present.height * present.length,
        )
        return 2 * sum(surface_areas) + min(surface_areas)

    @staticmethod
    def _calculate_ribbon_length(present):
        """Calculates the length of ribbon needed to tie around a present

        Args:
            present (Present): A namedtuple with the dimensions of the present
        Returns:
            int: The length of ribbon needed to tie around the present
        """
        perimeter_length = 2 * (sum(present) - max(present))
        bow_length = present.length * present.width * present.height
        return perimeter_length + bow_length

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        wrapping_paper_area = 0
        ribbon_length = 0
        for numbers in self._puzzle_input.splitlines():
            length, width, height = (int(feet) for feet in numbers.split('x'))
            present = Present(length, width, height)
            # Day 2 - Part 1
            wrapping_paper_area += self._calculate_square_footage(present)
            # Day 2 - Part 2
            ribbon_length += self._calculate_ribbon_length(present)
        return (wrapping_paper_area, ribbon_length)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        test_cases = (
            solver.TestCase('2x3x4', 58, 34),
            solver.TestCase('1x1x10', 43, 14),
        )
        for test_case in test_cases:
            self._run_test_case(test_case)
