#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Puzzle Solver Factory
  The factory module is used to instantiate puzzle solver objects for the
  various Advent of Code 2015 problems.

Author: James Walker
Copyright: MIT license
"""

# Application-specific Imports
from advent_of_code.solvers import (
    day_01,
    day_02,
    day_03,
    day_04,
    day_05,
    day_06,
    day_07,
    day_08,
    day_09,
    day_10,
    day_11,
    day_12,
    day_13,
    day_14,
    day_15,
    day_16,
    day_17,
    day_18,
    day_19,
    day_20,
    day_21,
    day_22,
    day_23,
    day_24,
    day_25,
)


def get_solver(day, file_name=None):
    """Instantiates the solver for the given Advent of Code problem

    Args:
        day (int): Day of the Advent of Code problem to solve
        file_name (str): Name of a file containing puzzle input
    Returns:
        Solver: Used to solve the given Advent of Code problem
    Raises:
        ValueError: If the puzzle number given is not between 1 and 25 (incl.)
    """
    aoc_solvers = (
        day_01,  # Day  1: Not Quite Lisp
        day_02,  # Day  2: I Was Told There Would Be No Math
        day_03,  # Day  3: Perfectly Spherical Houses in a Vacuum
        day_04,  # Day  4: The Ideal Stocking Stuffer
        day_05,  # Day  5: Doesn't He Have Intern-Elves For This?
        day_06,  # Day  6: Probably a Fire Hazard
        day_07,  # Day  7: Some Assembly Required
        day_08,  # Day  8: Matchsticks
        day_09,  # Day  9: All in a Single Night
        day_10,  # Day 10: Elves Look, Elves Say
        day_11,  # Day 11: Corporate Policy
        day_12,  # Day 12: JSAbacusFramework.io
        day_13,  # Day 13: Knights of the Dinner Table
        day_14,  # Day 14: Reindeer Olympics
        day_15,  # Day 15: Science for Hungry People
        day_16,  # Day 16: Aunt Sue
        day_17,  # Day 17: No Such Thing as Too Much
        day_18,  # Day 18: Like a GIF For Your Yard
        day_19,  # Day 19: Medicine for Rudolph
        day_20,  # Day 20: Infinite Elves and Infinite Houses
        day_21,  # Day 21: RPG Simulator 20XX
        day_22,  # Day 22: Wizard Simulator 20XX
        day_23,  # Day 23: Opening the Turing Lock
        day_24,  # Day 24: It Hangs in the Balance
        day_25,  # Day 25: Let It Snow
    )
    if 0 < day <= len(aoc_solvers):
        aoc_solver = aoc_solvers[day - 1].Solver
    else:
        raise ValueError('No solver exists for puzzle ' + str(day))
    return aoc_solver(file_name)
