#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/17
Author: James Walker
Copyrighted 2018 under the MIT license:
  http://www.opensource.org/licenses/mit-license.php

--- Day 17: No Such Thing as Too Much ---

  The elves bought too much eggnog again - 150 liters this time. To fit it all
  into your refrigerator, you'll need to move it into smaller containers. You
  take an inventory of the capacities of the available containers.

  For example, suppose you have containers of size 20, 15, 10, 5, and 5 liters.
  If you need to store 25 liters, there are four ways to do it:
    15 and 10
    20 and 5 (the first 5)
    20 and 5 (the second 5)
    15, 5, and 5

  Filling all containers entirely, how many different combinations of
  containers can exactly fit all 150 liters of eggnog?

    Answer: 1304

--- Day 17: Part Two ---

  While playing with all the containers in the kitchen, another load of eggnog
  arrives! The shipping and receiving department is requesting as many
  containers as you can spare.

  Find the minimum number of containers that can exactly fit all 150 liters of
  eggnog. How many different ways can you fill that number of containers and
  still hold exactly 150 litres?

  In the example above, the minimum number of containers was two. There were
  three ways to use that many containers, and so the answer there would be 3.

    Answer: 18
"""

# Standard Library Imports
from itertools import combinations

# Application-specific Imports
from advent_of_code.solvers import solver


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 17: No Such Thing as Too Much

    Attributes
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The number of 150 litre container combinations is {0}.',
            'The number of 150 litre fewest container combinations is {1}.',
        ))

    @staticmethod
    def _get_150_litre_combos(cups, min_length_combos=False):
        """

        Args:
            cups (list):
            min_length_combos (bool):
        Returns:
            list:
        """
        cup_combos = []
        for length in range(1, len(cups) + 1):
            cup_combos.extend((
                tuple(combo) for combo in combinations(cups, length)
                if sum(combo) == 150
            ))
            if min_length_combos and cup_combos:
                break
        return cup_combos

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        cups = [int(cup) for cup in self.puzzle_input.splitlines()]
        count_all_combos = len(self._get_150_litre_combos(cups, False))
        count_min_length_combos = len(self._get_150_litre_combos(cups, True))
        return (count_all_combos, count_min_length_combos)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        test_input = '\n'.join(('120', '90', '60', '30', '30'))
        self._run_test_case(solver.TestCase(test_input, 4, 3))
