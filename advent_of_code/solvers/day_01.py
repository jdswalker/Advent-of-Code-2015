#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/1
Author: James Walker
Copyright: MIT license

--- Day 1: Not Quite Lisp ---

  Santa was hoping for a white Christmas, but his weather machine's "snow"
  function is powered by stars, and he's fresh out! To save Christmas, he needs
  you to collect fifty stars by December 25th.

  Collect stars by helping Santa solve puzzles. Two puzzles will be made
  available on each day in the advent calendar; the second puzzle is unlocked
  when you complete the first. Each puzzle grants one star. Good luck!

  Here's an easy puzzle to warm you up.

  Santa is trying to deliver presents in a large apartment building, but he
  can't find the right floor - the directions he got are a little confusing.
  He starts on the ground floor (floor 0) and then follows the instructions one
  character at a time.

  An opening parenthesis, (, means he should go up one floor, and a closing
  parenthesis, ), means he should go down one floor. The apartment building is
  very tall, and the basement is very deep; he will never find the top or
  bottom floors.

  For example:
    (()) and ()() both result in floor 0.
    ((( and (()(()( both result in floor 3.
    ))((((( also results in floor 3.
    ()) and ))( both result in floor -1 (the first basement level).
    ))) and )())()) both result in floor -3.

  To what floor do the instructions take Santa?
    Answer: 232

--- Day 1: Part Two ---

  Now, given the same instructions, find the position of the first character
  that causes him to enter the basement (floor -1). The first character in the
  instructions has position 1, the second character has position 2, and so on.

  For example:
    ) causes him to enter the basement at character position 1.
    ()()) causes him to enter the basement at character position 5.

  What is the position of the character that causes Santa to first enter the
  basement?
    Answer: 1783
"""

# Application-specific Imports
from advent_of_code.solvers import solver


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 1: Not Quite Lisp

    Attributes
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
        instruction_map (dict): A scheme for mapping instructions to numbers
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The instructions took Santa to floor {0}.',
            'Instruction number {1} caused Santa to first enter the basement.',
        ))
        self._instruction = {
            '(': 1,
            ')': -1,
        }

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        current_floor = 0  # Floor the instructions took Santa
        entered_basement = 0  # Index when Santa first enters the basement
        for instruction_number, character in enumerate(self._puzzle_input):
            # Day 1 - Part 1
            current_floor += self._instruction[character]
            # Day 1 - Part 2
            if current_floor == -1 and not entered_basement:
                entered_basement = instruction_number + 1
        return (current_floor, entered_basement)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        self._run_test_case(solver.TestCase('(())', 0, 0))
        self._run_test_case(solver.TestCase('()()', 0, 0))
        self._run_test_case(solver.TestCase('(((', 3, 0))
        self._run_test_case(solver.TestCase('(()(()(', 3, 0))
        self._run_test_case(solver.TestCase('))(((((', 3, 1))
        self._run_test_case(solver.TestCase('())', -1, 3))
        self._run_test_case(solver.TestCase('))(', -1, 1))
        self._run_test_case(solver.TestCase(')))', -3, 1))
        self._run_test_case(solver.TestCase(')())())', -3, 1))
        self._run_test_case(solver.TestCase(')', -1, 1))
        self._run_test_case(solver.TestCase('()())', -1, 5))
