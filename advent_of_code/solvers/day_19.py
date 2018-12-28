 #!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/19
Author: James Walker
Copyrighted 2018 under the MIT license:
  http://www.opensource.org/licenses/mit-license.php

--- Day 19: Medicine for Rudolph ---

  Rudolph the Red-Nosed Reindeer is sick! His nose isn't shining very brightly,
  and he needs medicine.

  Red-Nosed Reindeer biology isn't similar to regular reindeer biology; Rudolph
  is going to need custom-made medicine. Unfortunately, Red-Nosed Reindeer
  chemistry isn't similar to regular reindeer chemistry, either.

  The North Pole is equipped with a Red-Nosed Reindeer nuclear fusion/fission
  plant, capable of constructing any Red-Nosed Reindeer molecule you need. It
  works by starting with some input molecule and then doing a series of
  replacements, one per step, until it has the right molecule.

  However, the machine has to be calibrated before it can be used. Calibration
  involves determining the number of molecules that can be generated in one
  step from a given starting point.

  For example, imagine a simpler machine that supports only the following
  replacements:
    H => HO
    H => OH
    O => HH

  Given the replacements above and starting with HOH, the following molecules
  could be generated:
    HOOH (via H => HO on the first H).
    HOHO (via H => HO on the second H).
    OHOH (via H => OH on the first H).
    HOOH (via H => OH on the second H).
    HHHH (via O => HH).

  So, in the example above, there are 4 distinct molecules (not five, because
  HOOH appears twice) after one replacement from HOH. Santa's favorite
  molecule, HOHOHO, can become 7 distinct molecules (over nine replacements:
  six from H, and three from O).

  The machine replaces without regard for the surrounding characters. For
  example, given the string H2O, the transition H => OO would result in OO2O.

  How many distinct molecules can be created after all the different ways you
  can do one replacement on the medicine molecule?

    Answer: 576

--- Day 19: Part Two ---

  Now that the machine is calibrated, you're ready to begin molecule
  fabrication. Molecule fabrication always begins with just a single electron,
  e, and applying replacements one at a time, just like the ones during
  calibration.

  For example, suppose you have the following replacements:
    e => H
    e => O
    H => HO
    H => OH
    O => HH

    If you'd like to make HOH, you start with e, and then make the following
    replacements:
      e => O to get O
      O => HH to get HH
      H => OH (on the second H) to get HOH

  So, you could make HOH after 3 steps. Santa's favorite molecule, HOHOHO, can
  be made in 6 steps.

  How long will it take to make the medicine? Given the available replacements
  and the medicine molecule in your puzzle input, what is the fewest number of
  steps to go from e to the medicine molecule?

    Answer: 207
"""


# Standard Library Imports
from collections import namedtuple
import heapq
import re

# Application-specific Imports
from advent_of_code.solvers import solver


Candidate = namedtuple(
    typename='Candidate',
    field_names='suffix precursor_suffix steps molecule',
)


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 19: Medicine for Rudolph

    Attributes
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'There are {0} unique substitutions for the calibration molecule.',
            'The medicine molecule takes at least {1} steps to synthesize.',
        ))

    def _parse_input(self):
        """

        Args:
        Returns:
            tuple:
        """
        replace_instruction = re.compile(r'^\w+ => \w+$')
        elements = re.compile('[A-Z][a-z]?')
        replacements = {}
        molecule = None
        for line in self.puzzle_input.splitlines():
            if not line:
                continue
            instruction = replace_instruction.match(line.strip())
            if instruction:
                target_term, substitution = instruction.group().split(' => ')
                if target_term not in replacements:
                    replacements[target_term] = []
                replacement = tuple(
                    element.group()
                    for element in elements.finditer(substitution)
                    if element
                )
                if replacement:
                    replacements[target_term].append(replacement)
            else:
                molecule = tuple(
                    element.group()
                    for element in elements.finditer(line.strip())
                    if element is not None
                )
        return (replacements, molecule)

    @staticmethod
    def _get_unmatched_suffix_length(precursor, target_molecule):
        """

        Args:
            precursor (str):
            target_molecule (str):
        Returns:
            int:
        """
        unmatched_suffix_length = 0
        for index, element in enumerate(precursor):
            if element != target_molecule[index]:
                unmatched_suffix_length = len(target_molecule) - index
                break
        return unmatched_suffix_length

    @staticmethod
    def _get_substituted_molecules(substitutions, precursor, substitute_start):
        """

        Args:
            substitutions (dict):
            precursor (str):
            substitute_start (int):
        Returns:
            set:
        """
        new_molecules = set()
        for i in range(substitute_start, len(precursor)):
            target_element = precursor[i]
            if target_element in substitutions:
                prefix = precursor[:i]
                suffix = precursor[i + 1:]
                for reagent in substitutions[target_element]:
                    new_molecules.add(tuple(prefix + reagent + suffix))
        return new_molecules

    def _get_steps_to_synthesize(self, replacements, target_molecule):
        """

        Args:
            replacements (dict):
            target_molecule (str):
        Returns:
            int:
        """
        target_length = len(target_molecule)
        candidates = []
        for candidate in replacements['e']:
            new_candidate = Candidate(
                target_length,
                self._get_unmatched_suffix_length(candidate, target_molecule),
                1,
                candidate,
            )
            heapq.heappush(candidates, new_candidate)
        successful_syntheses = target_length
        while candidates:
            candidate = heapq.heappop(candidates)
            # If the new molecule matches the target
            if candidate.molecule == target_molecule:
                successful_syntheses = candidate.steps
                break
            substitute_start = target_length - candidate.suffix - 1
            if substitute_start < 1:
                substitute_start = 0
            substituted_molecules = self._get_substituted_molecules(
                replacements,
                candidate.molecule,
                substitute_start,
            )
            if substituted_molecules:
                num_synthetic_steps = candidate.steps + 1
                for new_candidate in sorted(substituted_molecules):
                    # If the new molecule is larger than the target
                    if len(new_candidate) > target_length:
                        continue
                    unmatched_suffix = self._get_unmatched_suffix_length(
                        new_candidate,
                        target_molecule,
                    )
                    # If the old molecule matches better than the new molecule
                    if unmatched_suffix > candidate.suffix:
                        continue
                    # If the new molecule is better than the molecule precursor
                    # => Avoids unproductive looping on certain replacements
                    if unmatched_suffix != candidate.precursor_suffix:
                        new_molecule = Candidate(
                            unmatched_suffix,
                            candidate.suffix,
                            num_synthetic_steps,
                            new_candidate,
                        )
                        heapq.heappush(candidates, new_molecule)
        return successful_syntheses

    def _get_substitution_count(self, replacements, molecule):
        """

        Args:
            replacements (dict):
            molecule (str):
        Returns:
            int:
        """
        return len(self._get_substituted_molecules(replacements, molecule, 0))

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        replacements, molecule = self._parse_input()
        new_molecules = self._get_substitution_count(replacements, molecule)
        minimum_steps = self._get_steps_to_synthesize(replacements, molecule)
        return (new_molecules, minimum_steps)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        input1 = '\n'.join((
            'e => H',
            'e => O',
            'H => HO',
            'H => OH',
            'O => HH',
            '',
            'HOH',
        ))
        input2 = input1.replace('HOH', 'HOHOHO')
        self._run_test_case(solver.TestCase(input1, 4, 3))
        self._run_test_case(solver.TestCase(input2, 7, 6))
