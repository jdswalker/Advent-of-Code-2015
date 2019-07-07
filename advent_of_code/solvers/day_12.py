#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Puzzle Solver for Advent of Code 2015 Day 12
Author: James Walker
Copyright: MIT license

Description (https://adventofcode.com/2015/day/12):
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


# Equivalent to <class 'dict_values'>
DICT_VALUES = type({}.values())


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 12: JSAbacusFramework.io

    Attributes:
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

    @staticmethod
    def _get_sum(document, item=None):
        """Recursively sums all numeric fields from the JSON input

        Args:
            document (mixed): JSON parsed into int, list, dict, and/or str
            item (mixed): Dicts storing this value will be ignored (optional)
        Returns:
            int: Sum of numbers from the JSON input excluding ignored objects
        """
        if isinstance(document, int):
            total = document
        elif isinstance(document, (list, DICT_VALUES)):
            total = sum(Solver._get_sum(val, item) for val in document)
        elif isinstance(document, dict) and item not in document.values():
            total = Solver._get_sum(document.values(), item)
        else:
            total = 0
        return total

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        document = json.loads(self.puzzle_input)
        return self._get_sum(document), self._get_sum(document, "red")

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        test_cases = (
            solver.TestCase('[1,2,3]', 6, 6),
            solver.TestCase('{"a":2,"b":4}', 6, 6),
            solver.TestCase('[[[3]]]', 3, 3),
            solver.TestCase('{"a":{"b":4},"c":-1}', 3, 3),
            solver.TestCase('{"a":[-1,1]}', 0, 0),
            solver.TestCase('[-1,{"a":1}]', 0, 0),
            solver.TestCase('[]', 0, 0),
            solver.TestCase('{}', 0, 0),
            solver.TestCase('[1,{"c":"red","b":2},3]', 6, 4),
            solver.TestCase('{"d":"red","e":[1,2,3,4],"f":5}', 15, 0),
            solver.TestCase('[1,"red",5]', 6, 6),
            solver.TestCase('["a", {"red":1}]', 1, 1), # "red" keys are ok
        )
        for test_case in test_cases:
            self._run_test_case(test_case)
