#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Puzzle Solver for Advent of Code 2015 Day 5
Author: James Walker
Copyright: MIT license

Description (https://adventofcode.com/2015/day/5):
--- Day 5: Doesn't He Have Intern-Elves For This? ---

  Santa needs help figuring out which strings in his text file are naughty or
  nice.

  A nice string is one with all of the following properties:
    It contains at least three vowels (aeiou only), like aei, xazegov, or
      aeiouaeiouaeiou.
    It contains at least one letter that appears twice in a row, like xx,
      abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
    It does not contain the strings ab, cd, pq, or xy, even if they are part of
      one of the other requirements.

  For example:
    ugknbfddgicrmopn is nice because it has at least three vowels
      (u...i...o...), a double letter (...dd...), and none of the disallowed
      substrings.
    aaa is nice because it has at least three vowels and a double letter, even
      though the letters used by different rules overlap.
    jchzalrnumimnmhp is naughty because it has no double letter.
    haegwjzuvuyypxyu is naughty because it contains the string xy.
    dvszwmarrgswjxmb is naughty because it contains only one vowel.

  How many strings are nice?
    Answer: 258

--- Day 5: Part Two ---

  Realizing the error of his ways, Santa has switched to a better model of
  determining whether a string is naughty or nice. None of the old rules apply,
  as they are all clearly ridiculous. Now, a nice string is one with all of the
  following properties:

    It contains a pair of any two letters that appears at least twice in the
      string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not
      like aaa (aa, but it overlaps).
    It contains at least one letter which repeats with exactly one letter
      between them, like xyx, abcdefeghi (efe), or even aaa.

  For example:
    qjhvhtzxzqqjkmpb is nice because is has a pair that appears twice (qj) and
      a letter that repeats with exactly one letter between them (zxz).
    xxyxx is nice because it has a pair that appears twice and a letter that
      repeats with one between, even though the letters used by each rule
      overlap.
    uurcxstgmygtbstg is naughty because it has a pair (tg) but no repeat with a
      single letter between them.
    ieodomkazucvgmuy is naughty because it has a repeating letter with one
      between (odo), but no pair that appears twice.

  How many strings are nice under these new rules?
    Answer: 53
"""

# Standard Library Imports
import re

# Application-specific Imports
from advent_of_code.solvers import solver


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 5: Doesn't He Have Intern-Elves For This?

    Attributes
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
        vowels (RegexObject): Pattern for vowel characters
        double_char (RegexObject): Pattern for consecutive repeat characters
        naughty (RegexObject): Pattern for "naughty" character pairs
        double_pair (RegexObject): Pattern for repeated character pair
        triplet (RegexObject): Pattern for 3 character palindrome
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The text file had {0} nice strings using the original rules',
            'and it had {1} nice strings using the new rules.',
        ))
        self._vowels = re.compile('[aeiou]')
        self._double_char = re.compile(r'(\w)\1+')
        self._naughty = re.compile('ab|cd|pq|xy')
        self._double_pair = re.compile(r'(\w{2})\w*\1')
        self._triplet = re.compile(r'(\w)\w\1')

    def _is_nice_string_using_old_rules(self, string):
        """Checks if the string matches part 1 conditions for a "nice string"

        Args:
            string (str): Input to check conditions against
        Returns:
            bool: True if the input satisfies the "nice" conditions, else False
        """
        return (self._naughty.search(string) is None
                and len(self._vowels.findall(string)) > 2
                and self._double_char.search(string))

    def _is_nice_string_using_new_rules(self, string):
        """Checks if the string matches part 2 conditions for a "nice string"

        Args:
            string (str): Input to check conditions against
        Returns:
            bool: True if the input satisfies the "nice" conditions, else False
        """
        return (self._double_pair.search(string)
                and self._triplet.search(string))

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        old_nice_count = 0
        new_nice_count = 0
        for string in self._puzzle_input.splitlines():
            if not string:
                continue
            if self._is_nice_string_using_old_rules(string):
                old_nice_count += 1
            if self._is_nice_string_using_new_rules(string):
                new_nice_count += 1
        return (old_nice_count, new_nice_count)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        test_cases = (
            solver.TestCase('ugknbfddgicrmopn', 1, 0),
            solver.TestCase('aaa', 1, 0),
            solver.TestCase('jchzalrnumimnmhp', 0, 0),
            solver.TestCase('haegwjzuvuyypxyu', 0, 0),
            solver.TestCase('dvszwmarrgswjxmb', 0, 0),
            solver.TestCase('xyxy', 0, 1),
            solver.TestCase('aabcdefgaa', 0, 0),
            solver.TestCase('qjhvhtzxzqqjkmpb', 0, 1),
            solver.TestCase('xxyxx', 0, 1),
            solver.TestCase('uurcxstgmygtbstg', 0, 0),
            solver.TestCase('ieodomkazucvgmuy', 0, 0),
            solver.TestCase('aaccacc', 1, 1),
        )
        for test_case in test_cases:
            self._run_test_case(test_case)
