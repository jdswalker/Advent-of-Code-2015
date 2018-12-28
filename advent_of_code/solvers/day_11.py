#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/11
Author: James Walker
Copyrighted 2018 under the MIT license:
  http://www.opensource.org/licenses/mit-license.php

--- Day 11: Corporate Policy ---

  Santa's previous password expired, and he needs help choosing a new one.

  To help him remember his new password after the old one expires, Santa has
  devised a method of coming up with a password based on the previous one.
  Corporate policy dictates that passwords must be exactly eight lowercase
  letters (for security reasons), so he finds his new password by incrementing
  his old password string repeatedly until it is valid.

  Incrementing is just like counting with numbers: xx, xy, xz, ya, yb, and so
  on. Increase the rightmost letter one step; if it was z, it wraps around to
  a, and repeat with the next letter to the left until one doesn't wrap around.

  Unfortunately for Santa, a new Security-Elf recently started, and he has
  imposed some additional password requirements:
	Passwords must include one increasing straight of at least three letters,
      like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd
      doesn't count.
    Passwords may not contain the letters i, o, or l, as these letters can be
      mistaken for other characters and are therefore confusing.
    Passwords must contain at least two different, non-overlapping pairs of
      letters, like aa, bb, or zz.

  For example:
	hijklmmn meets the first requirement (because it contains the straight hij)
	  but fails the second requirement requirement (because it contains i and
      l).
    abbceffg meets the third requirement (because it repeats bb and ff) but
	  fails the first requirement.
    abbcegjk fails the third requirement, because it only has one double letter
	  (bb).
    The next password after abcdefgh is abcdffaa.
    The next password after ghijklmn is ghjaabcc, because you eventually skip
	  all the passwords that start with ghi..., since i is not allowed.

  Given Santa's current password (your puzzle input), what should his next
  password be?

    Answer: vzbxxyzz

--- Day 10: Part Two ---

  Santa's password expired again. What's the next one?

    Answer: vzcaabcc
"""

# Application-specific Imports
from advent_of_code.solvers import solver


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 11: Corporate Policy

    Attributes
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'Santa\'s next password should be "{0}"',
            'Santa\'s next password after that should be "{1}"',
        ))

    @staticmethod
    def _has_increasing_straight(password):
        """

        Args:
            password (str):
        Returns:
            bool:
        """
        contains_straight = False
        for i in range(6):
            if password[i] + 2 == password[i + 1] + 1 == password[i + 2]:
                contains_straight = True
                break
        return contains_straight

    @staticmethod
    def _has_two_char_pairs(password):
        """

        Args:
            password (str):
        Returns:
            bool:
        """
        char_pairs = {
            password[i] for i in range(7)
            if password[i] == password[i + 1]
        }
        return len(char_pairs) >= 2

    @staticmethod
    def _has_ambiguous_char(password):
        """

        Args:
            password (str):
        Returns:
            bool:
        """
        has_bad_char = False
        for ambiguous_char in (ord('i'), ord('l'), ord('o')):
            if ambiguous_char in password:
                has_bad_char = True
                break
        return has_bad_char

    def _is_valid_new_password(self, password):
        """

        Args:
            password (str):
        Returns:
            bool:
        """
        has_straight = self._has_increasing_straight(password)
        has_char_pairs = self._has_two_char_pairs(password)
        return has_straight and has_char_pairs

    @staticmethod
    def _increment_password(password):
        """

        Args:
            password (str):
        Returns: None
        """
        force_turn_over = False
        for char in range(8):
            if force_turn_over:
                password[char] = ord('z')
            if password[char] in (ord('i'), ord('l'), ord('o')):
                force_turn_over = True
        for char in range(-1, -9, -1):
            if password[char] == ord('z'):
                password[char] = ord('a')
            else:
                password[char] += 1
                break

    def _get_next_password(self, old_password):
        """

        Args:
            old_password (str):
        Returns:
            str:
        """
        password = [ord(char) for char in old_password]
        self._increment_password(password)
        while not self._is_valid_new_password(password):
            self._increment_password(password)
        return ''.join((chr(position) for position in password))

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        new_password1 = self._get_next_password(self.puzzle_input)
        new_password2 = self._get_next_password(new_password1)
        return (new_password1, new_password2)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        input1 = 'hijklmmn'
        input2 = 'abbceffg'
        input3 = 'abbcegjk'
        input4 = 'abcdefgh'
        input5 = 'ghijklmn'
        self._run_test_case(solver.TestCase(input1, 'hjaaabcc', 'hjaabbcd'))
        self._run_test_case(solver.TestCase(input2, 'abbcefgg', 'abbcffgh'))
        self._run_test_case(solver.TestCase(input3, 'abbcffgh', 'abbcfghh'))
        self._run_test_case(solver.TestCase(input4, 'abcdffaa', 'abcdffbb'))
        self._run_test_case(solver.TestCase(input5, 'ghjaabcc', 'ghjbbcdd'))
