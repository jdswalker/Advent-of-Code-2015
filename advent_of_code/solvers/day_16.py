#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Puzzle Solver for Advent of Code 2015 Day 16
Author: James Walker
Copyright: MIT license

Description (https://adventofcode.com/2015/day/16):
--- Day 16: Aunt Sue ---

  Your Aunt Sue has given you a wonderful gift, and you'd like to send her a
  thank you card. However, there's a small problem: she signed it "From, Aunt
  Sue".

  You have 500 Aunts named "Sue". So, to avoid sending the card to the wrong
  person, you need to figure out which Aunt Sue (which you conveniently number
  1 to 500, for sanity) gave you the gift. You open the present and, as luck
  would have it, good ol' Aunt Sue got you a My First Crime Scene Analysis
  Machine! Just what you wanted. Or needed, as the case may be.

  The My First Crime Scene Analysis Machine (MFCSAM for short) can detect a few
  specific compounds in a given sample, as well as how many distinct kinds of
  those compounds there are. According to the instructions, these are what the
  MFCSAM can detect:
    children, by human DNA age analysis.
    cats. It doesn't differentiate individual breeds.
    Several seemingly random breeds of dog: samoyeds, pomeranians, akitas, and
      vizslas.
    goldfish. No other kinds of fish.
    trees, all in one group.
    cars, presumably by exhaust or gasoline or something.
    perfumes, which is handy, since many of your Aunts Sue wear a few kinds.

  In fact, many of your Aunts Sue have many of these. You put the wrapping from
  the gift into the MFCSAM. It beeps inquisitively at you a few times and then
  prints out a message on ticker tape:
    children: 3
    cats: 7
    samoyeds: 2
    pomeranians: 3
    akitas: 0
    vizslas: 0
    goldfish: 5
    trees: 3
    cars: 2
    perfumes: 1

  You make a list of the things you can remember about each Aunt Sue. Things
  missing from your list aren't zero - you simply don't remember the value.

  What is the number of the Sue that got you the gift?
    Answer: 213

--- Day 16: Part Two ---

  As you're about to send the thank you note, something in the MFCSAM's
  instructions catches your eye. Apparently, it has an outdated
  retroencabulator, and so the output from the machine isn't exact values; some
  of them indicate ranges.

  In particular, the cats and trees readings indicates that there are greater
  than that many (due to the unpredictable nuclear decay of cat dander and tree
  pollen), while the pomeranians and goldfish readings indicate that there are
  fewer than that many (due to the modial interaction of magnetoreluctance).

  What is the number of the real Aunt Sue?
    Answer: 323
"""

# Application-specific Imports
from advent_of_code.solvers import solver


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 16: Aunt Sue

    Attributes:
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
        mfcsam (dict): Output from My First Crime Scene Analysis Machine
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'Aunt {0} was thought to have given the gift initially.',
            'Aunt {1} was the one that actually sent the gift.',
        ))
        self._mfcsam = {
            'children': 3,
            'cats': 7,
            'samoyeds': 2,
            'pomeranians': 3,
            'akitas': 0,
            'vizslas': 0,
            'goldfish': 5,
            'trees': 3,
            'cars': 2,
            'perfumes': 1,
        }

    def _parse_input(self):
        """Parses input to map memories of each Aunt Sue into a dictionary

        Args: None
        Returns:
            dict: Memories as a dict mapped to each Aunt Sue as a key
        """
        aunts = {}
        for details in self.puzzle_input.replace(':', ',').splitlines():
            sue, key1, val1, key2, val2, key3, val3 = details.split(', ')
            aunts[sue] = {key1: int(val1), key2: int(val2), key3: int(val3)}
        return aunts

    @staticmethod
    def _get_aunts_with_detail_eq(aunts, detail, target):
        """Get aunts without the detail or with a value equal to the target

        Args:
            aunts (dict): Stores remembered details about each Aunt Sue
            detail (str): Name of a detail from memory (e.g., cats)
            target (int): Exact detail value for the correct Aunt Sue
        Returns:
            dict: Aunts without the detail or with a detail value == target
        """
        return {
            aunt: memory for aunt, memory in aunts.items()
            if detail not in memory or memory[detail] == target
        }

    @staticmethod
    def _get_aunts_with_detail_lt(aunts, detail, target):
        """Get aunts without the detail or with a value less than the target

        Args:
            aunts (dict): Stores remembered details about each Aunt Sue
            detail (str): Check aunts based on this remembered detail
            target (int): Upper limit for the detail value of the correct Aunt
        Returns:
            dict: Aunts without the detail or with a detail value < target
        """
        return {
            aunt: memory for aunt, memory in aunts.items()
            if detail not in memory or memory[detail] < target
        }

    @staticmethod
    def _get_aunts_with_detail_gt(aunts, detail, target):
        """Get aunts without the detail or with a value greater than the target

        Args:
            aunts (dict): Stores remembered details about each Aunt Sue
            detail (str): Check aunts based on this remembered detail
            target (int): Lower limit for the detail value of the correct Aunt
        Returns:
            dict: Aunts without the detail or with a detail value > target
        """
        return {
            aunt: memory for aunt, memory in aunts.items()
            if detail not in memory or memory[detail] > target
        }

    def _get_aunt_sue(self, aunts, filters):
        """Solves each part of a Advent of Code 2015 puzzle

        Args:
            aunts (dict): Stores remembered details about each Aunt Sue
            filters (dict): Methods to filter aunts by detail
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        aunt_sue = None
        for detail, target in self._mfcsam.items():
            aunt_filter = filters.get(detail, Solver._get_aunts_with_detail_eq)
            aunts = aunt_filter(aunts, detail, target)
            if len(aunts) == 1:
                aunt_sue, _ = aunts.popitem()
                break
        return aunt_sue

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        aunts = self._parse_input()
        return (
            self._get_aunt_sue(aunts, filters={}),
            self._get_aunt_sue(aunts, filters={
                'cats': Solver._get_aunts_with_detail_gt,
                'trees': Solver._get_aunts_with_detail_gt,
                'goldfish': Solver._get_aunts_with_detail_lt,
                'pomeranians': Solver._get_aunts_with_detail_lt,
            }),
        )

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        aunt = 'Sue {0}: {1}: {2}, {3}: {4}, {5}: {6}'
        input1 = (aunt.format(1, 'akitas', 0, 'cars', 2, 'cats', 7),)
        input2 = (
            aunt.format(1, 'akitas', 0, 'cars', 2, 'cats', 8),
            aunt.format(2, 'children', 3, 'goldfish', 5, 'perfumes', 1),
        )
        input3 = (
            aunt.format(1, 'cats', 8, 'goldfish', 4, 'pomeranians', 2),
            aunt.format(2, 'akitas', 10, 'perfumes', 10, 'children', 5),
            aunt.format(3, 'cars', 2, 'pomeranians', 3, 'vizslas', 0),
            aunt.format(4, 'goldfish', 5, 'children', 8, 'perfumes', 3),
            aunt.format(5, 'vizslas', 2, 'akitas', 7, 'perfumes', 6),
            aunt.format(6, 'vizslas', 0, 'akitas', 1, 'perfumes', 2),
            aunt.format(7, 'perfumes', 8, 'cars', 4, 'goldfish', 10),
            aunt.format(8, 'perfumes', 7, 'children', 2, 'cats', 1),
            aunt.format(9, 'pomeranians', 3, 'goldfish', 10, 'trees', 10),
            aunt.format(10, 'akitas', 7, 'trees', 8, 'pomeranians', 4),
        )
        test_cases = (
            solver.TestCase('\n'.join(input1), 'Sue 1', 'Sue 1'),
            solver.TestCase('\n'.join(input2), 'Sue 2', 'Sue 1'),
            solver.TestCase('\n'.join(input3), 'Sue 3', 'Sue 1'),
        )
        for test_case in test_cases:
            self._run_test_case(test_case)
