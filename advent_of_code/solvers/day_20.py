#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/20
Author: James Walker
Copyright: MIT license

--- Day 20: Infinite Elves and Infinite Houses ---

  To keep the Elves busy, Santa has them deliver some presents by hand,
  door-to-door. He sends them down a street with infinite houses numbered
  sequentially: 1, 2, 3, 4, 5, and so on.

  Each Elf is assigned a number, too, and delivers presents to houses based on
  that number:
    The first Elf (number 1) delivers presents to every house:
        1, 2, 3, 4, 5, ....
    The second Elf (number 2) delivers presents to every second house:
        2, 4, 6, 8, 10, ....
    Elf number 3 delivers presents to every third house:
        3, 6, 9, 12, 15, ....

  There are infinitely many Elves, numbered starting with 1. Each Elf delivers
  presents equal to ten times his or her number at each house. So, the first
  nine houses on the street end up like this:
    House 1 got 10 presents.
    House 2 got 30 presents.
    House 3 got 40 presents.
    House 4 got 70 presents.
    House 5 got 60 presents.
    House 6 got 120 presents.
    House 7 got 80 presents.
    House 8 got 150 presents.
    House 9 got 130 presents.

    The first house gets 10 presents: it is visited only by Elf 1, which
    delivers 1 * 10 = 10 presents. The fourth house gets 70 presents, because
    it is visited by Elves 1, 2, and 4, for a total of 10 + 20 + 40 = 70
    presents.

  What is the lowest house number of the house to get at least as many presents
  as the number in your puzzle input?

    Answer: 665280

--- Day 20: Part Two ---

  The Elves decide they don't want to visit an infinite number of houses.
  Instead, each Elf will stop after delivering presents to 50 houses. To make
  up for it, they decide to deliver presents equal to eleven times their number
  at each house.

  With these changes, what is the new lowest house number of the house to get
  at least as many presents as the number in your puzzle input?

    Answer: 705600
"""

# Standard Library Imports
import math

# Application-specific Imports
from advent_of_code.solvers import solver


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 20: Infinite Elves and Infinite Houses

    Attributes:
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The first house number with at least as many presents is {0}.',
            'The second house number with at least as many presents is {1}',
        ))

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        min_presents = int(self.puzzle_input.strip())
        min_house_num = None
        alt_num = None
        house_num = 0
        while alt_num is None:
            # house_num += 2
            house_num += 2
            divisors = tuple(
                i for i in range(1, int(math.sqrt(house_num)) + 1)
                if house_num % i == 0
            )
            divisors += tuple(
                int(house_num / divisor) for divisor in divisors
                if house_num != divisor ** 2
            )
            if min_house_num is None:
                num_house_presents = 10 * sum(divisors)
            if alt_num is None:
                alt_num_presents = 11 * sum(
                    divisor for divisor in divisors
                    if house_num / divisor <= 50
                )
            if min_house_num is None and num_house_presents >= min_presents:
                min_house_num = house_num
            if alt_num is None and alt_num_presents >= min_presents:
                alt_num = house_num
        return (min_house_num, alt_num)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        test_input1 = '60'
        test_input2 = '120'
        test_input3 = '150'
        self._run_test_case(solver.TestCase(test_input1, 4, 4))
        self._run_test_case(solver.TestCase(test_input2, 6, 6))
        self._run_test_case(solver.TestCase(test_input3, 8, 8))
