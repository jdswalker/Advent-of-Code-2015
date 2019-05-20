#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015
Author: James Walker
Copyright: MIT license

Defines a base class that is inherited by each of the Advent of Code solvers.
"""

# Standard Library Imports
from collections import namedtuple
import os
import sys


# Stores expected input/output for test cases run on the solver
TestCase = namedtuple('TestCase', 'input expected1 expected2')


class AdventOfCodeSolver(object):
    """Base class for Advent of Code Solvers that handle each problem

    Attributes:
        file_name (str): The name of the file storing the puzzle input
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, file_name=None):
        self._file_name = file_name
        self._puzzle_input = None
        self._puzzle_title = self.__doc__.splitlines()[0]
        self._solved_output = None

    @property
    def puzzle_title(self):
        """Read-only property that returns the puzzle day and title as a string

        Args: None
        Returns:
            str: the day and title of the puzzle from the class docstring
        """
        return self._puzzle_title

    @property
    def puzzle_input(self):
        """@property gets the puzzle input stored by the solver

        Args: None
        Returns:
            str: the puzzle input currently stored by the solver
        """
        return self._puzzle_input

    def _load_puzzle_file(self):
        """Reads the puzzle input as a single string from a file

        Args: None
        Returns: None
        """
        file_path = os.path.realpath(self._file_name)
        try:
            with open(file_path, mode='r') as puzzle_file:
                self._puzzle_input = puzzle_file.read().rstrip()
        except IOError as error:
            msg = 'ERROR: Failed to read the puzzle input from file "{name}"'
            sys.exit('\n'.join((msg.format(name=self._file_name), str(error))))

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        raise NotImplementedError()

    def get_puzzle_solution(self, alt_input=None):
        """Reads the puzzle input from a file unless an alternative is provided

        Args:
            alt_input (list): A list of instructions to use as the puzzle input
        Returns:
            str: A string formatted with the solutions to the puzzle
        """
        if alt_input is None:
            self._load_puzzle_file()
        else:
            self._puzzle_input = alt_input
        answer1, answer2 = self._solve_puzzle_parts()
        return self._solved_output.format(str(answer1), str(answer2))

    def _run_test_case(self, test_case):
        """Runs the solver with test case input and compares against output

        Args:
            test_case (TestCase): A namedtuple with input and expected outputs
        Returns: None
        """
        correct_output = self._solved_output.format(
            test_case.expected1,
            test_case.expected2,
        )
        test_output = self.get_puzzle_solution(test_case.input)
        if correct_output == test_output:
            print('Test passed for input {0}'.format(test_case.input))
        else:
            print('Test failed for input {0}'.format(test_case.input))
            print('Correct output:\n{0}\n'.format(correct_output))
            print('Test output:\n{0}\n'.format(test_output))

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        raise NotImplementedError()
