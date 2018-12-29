#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/16
Author: James Walker
Copyright: MIT license

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

# Standard Library Imports
import re

# Application-specific Imports
from advent_of_code.solvers import solver


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 16: Aunt Sue

    Attributes
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The number of the Aunt Sue was thought to be {0}.',
            'The number of the "real" Aunt Sue is {1}.',
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
        """

        Args: None
        Returns:
            dict:
        """
        memory_of_aunt = r'(?<=Sue )(\d+)(?=:)|(\w+: \d+)'
        memories = re.compile(memory_of_aunt)
        aunts = {}
        for aunt_info in self.puzzle_input.splitlines():
            aunt_memory = memories.findall(aunt_info)
            aunt_number = aunt_memory[0][0]
            aunt = {}
            for i in range(1, len(aunt_memory)):
                detail, count = aunt_memory[i][1].split(': ')
                aunt[detail] = int(count)
            aunts[aunt_number] = aunt
        return aunts

    def _get_aunts_matching_detail(self, candidates, detail):
        """

        Args:
            candidates (dict):
            detail (str):
        Returns:
            dict:
        """
        new_candidates = {}
        for aunt_number in candidates:
            aunt = candidates[aunt_number]
            if detail not in aunt or aunt[detail] == self._mfcsam[detail]:
                new_candidates[aunt_number] = aunt
        return new_candidates

    def _get_aunts_less_than_detail(self, candidates, detail):
        """

        Args:
            candidates (dict):
            detail (str):
        Returns:
            dict:
        """
        new_candidates = {}
        for aunt_number in candidates:
            aunt = candidates[aunt_number]
            if detail not in aunt or aunt[detail] < self._mfcsam[detail]:
                new_candidates[aunt_number] = aunt
        return new_candidates

    def _get_aunts_greater_than_detail(self, candidates, detail):
        """

        Args:
            candidates (dict):
            detail (str):
        Returns:
            dict:
        """
        new_candidates = {}
        for aunt_number in candidates:
            aunt = candidates[aunt_number]
            if detail not in aunt or aunt[detail] > self._mfcsam[detail]:
                new_candidates[aunt_number] = aunt
        return new_candidates

    def _get_aunt_with_matching_details(self, aunts):
        """

        Args:
            aunts (dict):
        Returns:
            str:
        """
        aunt_sue = None
        candidates = aunts.copy()
        for detail in self._mfcsam:
            candidates = self._get_aunts_matching_detail(candidates, detail)
            if len(candidates) == 1:
                aunt_sue = list(candidates.keys())[0]
                break
        return aunt_sue

    def _get_aunt_with_fuzzy_details(self, candidates):
        """

        Args:
            candidates (dict):
        Returns:
            str:
        """
        aunt_sue = None
        aunts = candidates.copy()
        for detail in self._mfcsam:
            if detail in ('cats', 'trees'):
                aunts = self._get_aunts_greater_than_detail(aunts, detail)
            elif detail in ('goldfish', 'pomeranians'):
                aunts = self._get_aunts_less_than_detail(aunts, detail)
            else:
                aunts = self._get_aunts_matching_detail(aunts, detail)
            if len(aunts) == 1:
                aunt_sue = list(aunts.keys())[0]
                break
        return aunt_sue

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        aunts = self._parse_input()
        first_aunt_sue = self._get_aunt_with_matching_details(aunts)
        real_aunt_sue = self._get_aunt_with_fuzzy_details(aunts)
        return (first_aunt_sue, real_aunt_sue)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        output = 'There are no test cases to run...'
        print(output)
