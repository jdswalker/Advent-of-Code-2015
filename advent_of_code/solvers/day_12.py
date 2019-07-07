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
    def _get_sum(document):
        """Sums all numeric fields from the JSON input

        Args:
            document (mixed): Object parsed from the JSON input
        Returns:
            int: Sum of numbers from the JSON input
        """
        if isinstance(document, int):
            total = document
        elif isinstance(document, list):
            total = sum(Solver._get_sum(value) for value in document)
        elif isinstance(document, dict):
            total = Solver._get_sum([val for val in document.values()])
        else:
            total = 0
        return total

    @staticmethod
    def _get_correct_sum(document):
        """Sums all numeric fields from the JSON input ignoring objects that
        contain the word "red"

        Args:
            document (mixed): Object parsed from the JSON input
        Returns:
            int: Sum of numbers from the JSON input excluding ignored objects
        """
        if isinstance(document, int):
            total = document
        elif isinstance(document, list):
            total = sum(Solver._get_correct_sum(val) for val in document)
        elif isinstance(document, dict) and "red" not in document.values():
            total = Solver._get_correct_sum([val for val in document.values()])
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
        return self._get_sum(document), self._get_correct_sum(document)

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
        test_cases = (
            solver.TestCase(input01, 6, 6),
            solver.TestCase(input02, 6, 6),
            solver.TestCase(input03, 3, 3),
            solver.TestCase(input04, 3, 3),
            solver.TestCase(input05, 0, 0),
            solver.TestCase(input06, 0, 0),
            solver.TestCase(input07, 0, 0),
            solver.TestCase(input08, 0, 0),
            solver.TestCase(input09, 6, 4),
            solver.TestCase(input10, 15, 0),
            solver.TestCase(input11, 6, 6),
        )
        for test_case in test_cases:
            self._run_test_case(test_case)
