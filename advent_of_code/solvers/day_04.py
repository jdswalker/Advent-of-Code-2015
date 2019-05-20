#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Puzzle Solver for Advent of Code 2015 Day 4
Author: James Walker
Copyright: MIT license

Description (https://adventofcode.com/2015/day/4):
--- Day 4: The Ideal Stocking Stuffer ---

  Santa needs help mining some AdventCoins (very similar to bitcoins) to use as
  gifts for all the economically forward-thinking little girls and boys.

  To do this, he needs to find MD5 hashes which, in hexadecimal, start with at
  least five zeroes. The input to the MD5 hash is some secret key (your puzzle
  input, given below) followed by a number in decimal. To mine AdventCoins, you
  must find Santa the lowest positive number (no leading zeroes: 1, 2, 3, ...)
  that produces such a hash.

  For example:
    If your secret key is abcdef, the answer is 609043, because the MD5 hash of
    abcdef609043 starts with five zeroes (000001dbbfa...), and it is the lowest
    such number to do so.
    If your secret key is pqrstuv, the lowest number it combines with to make
    an MD5 hash starting with five zeroes is 1048970; that is, the MD5 hash of
    pqrstuv1048970 looks like 000006136ef....

  Answer: 282749

--- Day 4: Part Two ---
  Now find one that starts with six zeroes.

  Answer: 9962624
"""

# Standard Library Imports
import hashlib

# Application-specific Imports
from advent_of_code.solvers import solver


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 4: The Ideal Stocking Stuffer

    Attributes
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The numbers that generate valid hashes with the secret keys',
            'are {0} and {1}',
        ))

    def _get_hash_number(self, prefix, start):
        """Searches for the first MD5 hash that matches the given prefix

        Args:
            prefix (str): String that the MD5 hex digest must begin with
            start (int): Number to begin searching for the next hash
        Returns:
            int: Number that produces an MD5 hash matching the given prefix
        """
        hash_num = 0 if start is None else start
        md5_hash = hashlib.md5(self._puzzle_input.encode('utf-8'))
        while True:
            hash_input = md5_hash.copy()
            hash_input.update(str(hash_num).encode('utf-8'))
            if hash_input.hexdigest().startswith(prefix):
                break
            hash_num += 1
        return hash_num

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        # Day 4: Part 1
        match1 = self._get_hash_number(prefix='00000', start=0)
        # Day 4: Part 2
        match2 = self._get_hash_number(prefix='000000', start=match1)
        return (match1, match2)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        test_cases = (
            solver.TestCase('abcdef', 609043, 6742839),
            solver.TestCase('pqrstuv', 1048970, 5714438),
        )
        for test_case in test_cases:
            self._run_test_case(test_case)
