#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/12
Author: James Walker
Copyright: MIT license

--- Day 12: JSAbacusFramework.io ---

  Santa's Accounting-Elves need help balancing the books after a recent order.
  Unfortunately, their accounting software uses a peculiar storage format.
  That's where you come in.

  They have a JSON document which contains a variety of things: arrays
  ([1,2,3]), objects ({"a":1, "b":2}), numbers, and strings. Your first job is
  to simply find all of the numbers throughout the document and add them
  together.

  For example:
    [1,2,3] and {"a":2,"b":4} both have a sum of 6.
    [[[3]]] and {"a":{"b":4},"c":-1} both have a sum of 3.
    {"a":[-1,1]} and [-1,{"a":1}] both have a sum of 0.
    [] and {} both have a sum of 0.

  You will not encounter any strings containing numbers.

  What is the sum of all numbers in the document?

    Answer: 191164

--- Day 12: Part Two ---

  Uh oh - the Accounting-Elves have realized that they double-counted
  everything red. Ignore any object (and all of its children) which has any
  property with the value "red". Do this only for objects ({...}), not arrays
  ([...]).

  For example:
    [1,2,3] still has a sum of 6.
    [1,{"c":"red","b":2},3] now has a sum of 4, because the middle object is
        ignored.
    {"d":"red","e":[1,2,3,4],"f":5} now has a sum of 0, because the entire
        structure is ignored.
    [1,"red",5] has a sum of 6, because "red" in an array has no effect.

  What is the sum of all numbers in the document without double-counting?

    Answer: 87842
"""

# Standard Library Imports
import json

# Application-specific Imports
from advent_of_code.solvers import solver


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 12: JSAbacusFramework.io

    Attributes
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The sum of all numbers in the document is {0}',
            'The sum using the correct numbers in the document is {1}',
        ))

    def _sum_all_numbers(self, document):
        """Runs a series of inputs and compares against expected outputs

        Args:
            document
        Returns:
            int:
        """
        if isinstance(document, int):
            num_sum = document
        elif isinstance(document, list):
            num_sum = sum((self._sum_all_numbers(value) for value in document))
        elif isinstance(document, dict):
            num_sum = self._sum_all_numbers(list(document.values()))
        else:
            num_sum = 0
        return num_sum

    def _sum_corrected_nums(self, document):
        """Runs a series of inputs and compares against expected outputs

        Args:
            document
        Returns:
            int:
        """
        if isinstance(document, int):
            num_sum = document
        elif isinstance(document, list):
            num_sum = sum(self._sum_corrected_nums(val) for val in document)
        elif isinstance(document, dict):
            if "red" not in list(document.values()):
                num_sum = self._sum_corrected_nums(list(document.values()))
            else:
                num_sum = 0
        else:
            num_sum = 0
        return num_sum

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        document = json.loads(self.puzzle_input)
        return (
            self._sum_all_numbers(document),
            self._sum_corrected_nums(document),
        )

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        input01 = '[1,2,3]'
        input02 = '{"a":2,"b":4}'
        input03 = '[[[3]]]'
        input04 = '{"a":{"b":4},"c":-1}'
        input05 = '{"a":[-1,1]}'
        input06 = '[-1,{"a":1}]'
        input07 = '[]'
        input08 = '{}'
        input09 = '[1,{"c":"red","b":2},3]'
        input10 = '{"d":"red","e":[1,2,3,4],"f":5}'
        input11 = '[1,"red",5]'
        self._run_test_case(solver.TestCase(input01, 6, 6))
        self._run_test_case(solver.TestCase(input02, 6, 6))
        self._run_test_case(solver.TestCase(input03, 3, 3))
        self._run_test_case(solver.TestCase(input04, 3, 3))
        self._run_test_case(solver.TestCase(input05, 0, 0))
        self._run_test_case(solver.TestCase(input06, 0, 0))
        self._run_test_case(solver.TestCase(input07, 0, 0))
        self._run_test_case(solver.TestCase(input08, 0, 0))
        self._run_test_case(solver.TestCase(input09, 6, 4))
        self._run_test_case(solver.TestCase(input10, 15, 0))
        self._run_test_case(solver.TestCase(input11, 6, 6))
