#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/24
Author: James Walker
Copyright: MIT license

--- Day 24: It Hangs in the Balance ---

  It's Christmas Eve, and Santa is loading up the sleigh for this year's
  deliveries. However, there's one small problem: he can't get the sleigh to
  balance. If it isn't balanced, he can't defy physics, and nobody gets
  presents this year. No pressure.

  Santa has provided you a list of the weights of every package he needs to fit
  on the sleigh. The packages need to be split into three groups of exactly the
  same weight, and every package has to fit. The first group goes in the
  passenger compartment of the sleigh, and the second and third go in
  containers on either side. Only when all three groups weigh exactly the same
  amount will the sleigh be able to fly. Defying physics has rules, you know!

  Of course, that's not the only problem. The first group - the one going in
  the passenger compartment - needs as few packages as possible so that Santa
  has some legroom left over. It doesn't matter how many packages are in either
  of the other two groups, so long as all of the groups weigh the same.

  Furthermore, Santa tells you, if there are multiple ways to arrange the
  packages such that the fewest possible are in the first group, you need to
  choose the way where the first group has the smallest quantum entanglement to
  reduce the chance of any "complications". The quantum entanglement of a group
  of packages is the product of their weights, that is, the value you get when
  you multiply their weights together. Only consider quantum entanglement if
  the first group has the fewest possible number of packages in it and all
  groups weigh the same amount.

  For example, suppose you have ten packages with weights 1 through 5 and 7
  through 11. For this situation, some of the unique first groups, their
  quantum entanglements, and a way to divide the remaining packages are as
  follows:
    Group 1;             Group 2; Group 3
    11 9       (QE= 99); 10 8 2;  7 5 4 3 1
    10 9 1     (QE= 90); 11 7 2;  8 5 4 3
    10 8 2     (QE=160); 11 9;    7 5 4 3 1
    10 7 3     (QE=210); 11 9;    8 5 4 2 1
    10 5 4 1   (QE=200); 11 9;    8 7 3 2
    10 5 3 2   (QE=300); 11 9;    8 7 4 1
    10 4 3 2 1 (QE=240); 11 9;    8 7 5
    9 8 3      (QE=216); 11 7 2;  10 5 4 1
    9 7 4      (QE=252); 11 8 1;  10 5 3 2
    9 5 4 2    (QE=360); 11 8 1;  10 7 3
    8 7 5      (QE=280); 11 9;    10 4 3 2 1
    8 5 4 3    (QE=480); 11 9;    10 7 2 1
    7 5 4 3 1  (QE=420); 11 9;    10 8 2

  Of these, although 10 9 1 has the smallest quantum entanglement (90), the
  configuration with only two packages, 11 9, in the passenger compartment
  gives Santa the most legroom and wins. In this situation, the quantum
  entanglement for the ideal configuration is therefore 99. Had there been two
  configurations with only two packages in the first group, the one with the
  smaller quantum entanglement would be chosen.

  What is the quantum entanglement of the first group of packages in the ideal
  configuration?

    Answer: 10,439,961,859

--- Day 24: Part Two ---

  That's weird... the sleigh still isn't balancing. "Ho ho ho", Santa muses to
  himself. "I forgot the trunk". Balance the sleigh again, but this time,
  separate the packages into four groups instead of three. The other
  constraints still apply.

  Given the example packages above, this would be some of the new unique first
  groups, their quantum entanglements, and one way to divide the remaining
  packages:
    11 4    (QE=44); 10 5;   9 3 2 1; 8 7
    10 5    (QE=50); 11 4;   9 3 2 1; 8 7
    9 5 1   (QE=45); 11 4;   10 3 2;  8 7
    9 4 2   (QE=72); 11 3 1; 10 5;    8 7
    9 3 2 1 (QE=54); 11 4;   10 5;    8 7
    8 7     (QE=56); 11 4;   10 5;    9 3 2 1

  Of these, there are three arrangements that put the minimum (two) number of
  packages in the first group: 11 4, 10 5, and 8 7. Of these, 11 4 has the
  lowest quantum entanglement, and so it is selected.

  Now, what is the quantum entanglement of the first group of packages in the
  ideal configuration?

    Answer: 72,050,269
"""

# Standard Library Imports
from itertools import combinations
import sys

# Application-specific Imports
from advent_of_code.solvers import solver


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 24: It Hangs in the Balance

    Attributes
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The best quantum entanglement for the first 3 groups is {0}.',
            'The best quantum entanglement for the first 4 groups is {1}.',
        ))

    @staticmethod
    def _get_candidates(packages, target_weight, num_pkgs):
        """Generates all num_pkgs sized groups matching the target weight

        Args:
            packages (set): Package weights to divide into groups
            target_weight (int): Candidate groups must sum to this weight
            num_pkgs (int): Number of packages that should be in the group
        Returns:
            set: Tuples of candidate groups and leftover packages
        """
        candidates = set()
        min_first_pkg_weight = int((target_weight / num_pkgs) + (num_pkgs / 2))
        for group in combinations(sorted(packages, reverse=True), num_pkgs):
            if sum(group) == target_weight:
                candidates.add((group, tuple(set(packages).difference(group))))
            if min_first_pkg_weight > group[0]:
                # No further package group combinations will be valid
                break
        return candidates

    def _get_candidate_groups(self, packages, target_weight):
        """Generates all possible package groups matching the target weight

        Args:
            packages (set): Package weights to divide into groups
            target_weight (int): Candidate groups must sum to this weight
        Returns:
            set: Tuples of candidate groups and leftover packages
        """
        groups = set()
        max_packages_per_group = int(len(packages) / 2) + len(packages) % 2
        for num_pkgs in range(1, max_packages_per_group):
            groups.update(
                self._get_candidates(packages, target_weight, num_pkgs)
            )
            if groups:
                break
        return groups

    def _get_min_quantum_entanglement(self, packages, num_groups):
        """Calculates the best quantum entanglement of smallest package group

        Args:
            packages (set): Package weights to divide into groups
            num_groups (int): Number of equal weight groups to generate
        Returns:
            int: Minimum quantum entanglement of smallest package group
        """
        target_weight = int(sum(packages) / num_groups)
        candidates = self._get_candidate_groups(packages, target_weight)
        min_quantum_entanglement = sys.maxsize
        for first_group, remaining in candidates:
            if self._get_candidate_groups(remaining, target_weight):
                entanglment = 1
                for package in first_group:
                    entanglment *= package
                if min_quantum_entanglement > entanglment:
                    min_quantum_entanglement = entanglment
        return min_quantum_entanglement

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        packages = {int(pkg) for pkg in self.puzzle_input.splitlines() if pkg}
        best_triple_groups = self._get_min_quantum_entanglement(packages, 3)
        best_quad_groups = self._get_min_quantum_entanglement(packages, 4)
        return (best_triple_groups, best_quad_groups)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        input_range = tuple(range(1, 6)) + tuple(range(7, 12))
        test_input = '\n'.join(str(num) for num in input_range)
        self._run_test_case(solver.TestCase(test_input, 99, 44))
