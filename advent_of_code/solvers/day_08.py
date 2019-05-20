#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Puzzle Solver for Advent of Code 2015 Day 8
Author: James Walker
Copyright: MIT license

Description (https://adventofcode.com/2015/day/8):
--- Day 8: Matchsticks ---

  Space on the sleigh is limited this year, and so Santa will be bringing his
  list as a digital copy. He needs to know how much space it will take up when
  stored.

  It is common in many programming languages to provide a way to escape special
  characters in strings. For example, C, JavaScript, Perl, Python, and even PHP
  handle special characters in very similar ways.

  However, it is important to realize the difference between the number of
  characters in the code representation of the string literal and the number of
  characters in the in-memory string itself.

  Disregarding the whitespace in the file, what is the number of characters of
  code for string literals minus the number of characters in memory for the
  values of the strings in total for the entire file?

  Answer: 1342

--- Day 8: Part Two ---

  Now, let's go the other way. In addition to finding the number of characters
  of code, you should now encode each code representation as a new string and
  find the number of characters of the new encoded representation, including
  the surrounding double quotes.

  For example:

    ""         encodes to "\"\"", an increase from 2 characters to 6.
    "abc"      encodes to "\"abc\"", an increase from 5 characters to 9.
    "aaa\"aaa" encodes to "\"aaa\\\"aaa\"", an increase from 10 characters
               to 16.
    "\x27"     encodes to "\"\\x27\"", an increase from 6 characters to 11.

  Your task is to find the total number of characters to represent the newly
  encoded strings minus the number of characters of code in each original
  string literal. For example, for the strings above, the total encoded length
  (6 + 9 + 16 + 11 = 42) minus the characters in the original code
  representation (23, just like in the first part of this puzzle) is
  42 - 23 = 19.
"""

# Standard Library Imports
import re

# Application-specific Imports
from advent_of_code.solvers import solver


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 8: Matchsticks

    Attributes:
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'Total characters of code minus total characters in memory: {0}',
            'Total decoded characters minus total characters of code:   {1}',
        ))

    @staticmethod
    def _count_encoded_chars(string_literal):
        """Calculates extra characters used to encode the string literal.

        Args:
            string_literal (str): String literal or raw encoded characters
        Returns:
            int: Total characters of code minus total characters in memory
        """
        escaped_backslash = r'\\'
        double_quote = '"'
        hex_char = r'(?:(?<!\\)(?:\\\\)*)\\x[a-f0-9][a-f0-9]'
        encoded_chars = len(string_literal)
        encoded_chars -= string_literal.count(escaped_backslash)
        encoded_chars -= string_literal.count(double_quote)
        encoded_chars -= 3 * len(re.findall(hex_char, string_literal))

        return encoded_chars

    def _calculate_encoded_diff(self, string_literals):
        """Calculates characters of code minus total characters in memory for
        each string in the given list.

        Args:
            string_literals (list): List of strings used for calculation input
        Returns:
            int: Total characters of code minus total characters in memory
        """
        num_chars_of_code = 0
        encoded_chars = 0
        for string_literal in string_literals:
            chars_of_code = len(string_literal)
            num_chars_of_code += chars_of_code
            encoded_chars += self._count_encoded_chars(string_literal)
        return num_chars_of_code - encoded_chars

    @staticmethod
    def _count_decoded_chars(string_literal):
        """Calculates extra characters used to encode the string literal.

        Args:
            string_literal (str): String literal or raw encoded characters
        Returns:
            int: Total characters of code minus total characters in memory
        """
        escaped_backslash = '\\'
        double_quote = '"'
        decoded_chars = len(string_literal) + 2  # For quoting
        decoded_chars += string_literal.count(escaped_backslash)
        decoded_chars += string_literal.count(double_quote)
        return decoded_chars

    def _calculate_decoded_diff(self, string_literals):
        """Calculates characters of code minus total characters in memory for
        each string in the given list.

        Args:
            string_literals (list): List of strings used for calculation input
        Returns:
            int: Total characters of code minus total characters in memory
        """
        num_chars_of_code = 0
        decoded_chars = 0
        for string_literal in string_literals:
            num_chars_of_code += len(string_literal)
            decoded_chars += self._count_decoded_chars(string_literal)
        return decoded_chars - num_chars_of_code

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        file_lines = self._puzzle_input.splitlines()
        # Part 1 of Day 8
        encoded_char_diff = self._calculate_encoded_diff(file_lines)

        # Part 2 of Day 8
        decoded_char_diff = self._calculate_decoded_diff(file_lines)

        return (encoded_char_diff, decoded_char_diff)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        test_cases = (
            solver.TestCase('""', 2 - 0, 6 - 2),
            solver.TestCase('"abc"', 5 - 3, 9 - 5),
            solver.TestCase(r'"aaa\"aaa"', 10 - 7, 16 - 10),
            solver.TestCase(r'"\x27"', 6 - 1, 11 - 6),
        )
        for test_case in test_cases:
            self._run_test_case(test_case)
