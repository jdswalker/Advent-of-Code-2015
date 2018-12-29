#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/4
Author: James Walker
Copyright: MIT license

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
import re

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

    def _get_valid_hash_number(self, prefix, hash_num=0):
        """Searches for the first MD5 hash that matches the given prefix

        Args:
            prefix (str):
            hash_num (int): The number to begin searching for the next hash
        Returns:
            int: The number that produces an MD5 hash with the prefix
        """
        md5_hash = hashlib.md5(self._puzzle_input.encode('utf-8'))
        hash_prefix = re.compile(prefix)
        while True:
            hash_input = md5_hash.copy()
            hash_input.update(str(hash_num).encode('utf-8'))
            if not hash_prefix.match(hash_input.hexdigest()):
                hash_num += 1
            else:
                break
        return hash_num

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        valid_hash = '000000'
        # Day 4: Part 1
        hash_5_match = self._get_valid_hash_number(valid_hash[:5])
        # Day 4: Part 2
        hash_6_match = self._get_valid_hash_number(valid_hash, hash_5_match)
        return (hash_5_match, hash_6_match)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        self._run_test_case(solver.TestCase('abcdef', 609043, 6742839))
        self._run_test_case(solver.TestCase('pqrstuv', 1048970, 5714438))
