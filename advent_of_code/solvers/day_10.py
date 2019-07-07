#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Puzzle Solver for Advent of Code 2015 Day 10
Author: James Walker
Copyright: MIT license

Description (https://adventofcode.com/2015/day/10):
--- Day 10: Elves Look, Elves Say ---

  Today, the Elves are playing a game called look-and-say. They take turns
  making sequences by reading aloud the previous sequence and using that
  reading as the next sequence. For example, 211 is read as "one two, two
  ones", which becomes 1221 (1 2, 2 1s).

  Look-and-say sequences are generated iteratively, using the previous value as
  input for the next step. For each step, take the previous value, and replace
  each run of digits (like 111) with the number of digits (3) followed by the
  digit itself (1).

  For example:
    1 becomes 11 (1 copy of digit 1).
    11 becomes 21 (2 copies of digit 1).
    21 becomes 1211 (one 2 followed by one 1).
    1211 becomes 111221 (one 1, one 2, and two 1s).
    111221 becomes 312211 (three 1s, two 2s, and one 1).

  Starting with the digits in your puzzle input, apply this process 40 times.
  What is the length of the result?
    Answer: 360154

--- Day 10: Part Two ---

  Now, starting again with the digits in your puzzle input, apply this process
  50 times. What is the length of the new result?
    Answer: 5103798
"""

# Standard Library Imports
import re

# Application-specific Imports
from advent_of_code.solvers import solver


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 10: Elves Look, Elves Say

    Attributes:
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The length of the output after 40 iterations is {0}',
            'The length of the output after 50 iterations is {1}',
        ))

    @staticmethod
    def _look_and_say(parser, sequence):
        """Creates a sequence from playing "look-and-say" on the given sequence

        Args:
            parser (Patter): Compiled regex for grouping repeated digits
            sequence (str): Number sequence to "look-and-say"
        Returns:
            str: New number sequence generated from playing "look-and-say"
        """
        new_sequence = []
        for match in parser.finditer(sequence):
            number_group = match.group()
            new_sequence.append(str(len(number_group)))
            new_sequence.append(number_group[0])
        return ''.join(new_sequence)

    def _apply_look_and_say(self, sequence, count):
        """Iteratively creates "look-and-say" sequences from the given sequence

        Args:
            sequence (str): Initial sequence for "look-and-say" game
            count (int): Number of times to play "look-and-say"
        Returns:
            str: Final number sequence after playing "look-and-say" count times
        """
        group_numbers = ('|'.join(str(num) + '+' for num in range(0, 10)))
        parser = re.compile(group_numbers)
        output = sequence
        for _ in range(count):
            output = self._look_and_say(parser, output)
        return output

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        iteration_40 = self._apply_look_and_say(self.puzzle_input, count=40)
        iteration_50 = self._apply_look_and_say(iteration_40, count=10)
        return (len(iteration_40), len(iteration_50))

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        test_cases = (
            solver.TestCase('1', 82350, 1166642),
            solver.TestCase('2', 95798, 1355550),
            solver.TestCase('3', 95798, 1355550),
            solver.TestCase('11', 107312, 1520986),
            solver.TestCase('111', 149642, 2121256),
        )
        for test_case in test_cases:
            self._run_test_case(test_case)
