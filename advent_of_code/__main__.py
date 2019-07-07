#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Puzzle Solvers for Advent of Code 2015 [https://adventofcode.com/2015]
  Advent of Code is a series of small programming puzzles for a variety of
  skill levels. They are self-contained and are just as appropriate for an
  expert who wants to stay sharp as they are for a beginner who is just
  learning to code. Each puzzle calls upon different skills and has two parts
  that build on a theme.

Author: James Walker
Copyright: MIT license
"""

# Standard Library Imports
import argparse
import sys

# Application-specific Imports
from advent_of_code.solvers import factory


def get_args():
    """Parses command-line inputs for the script or assigns default values

    Args: None
    Returns:
        Namespace: Values parsed from command-line arguments
    """
    parser = argparse.ArgumentParser(
        prog='advent_of_code',
        epilog=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='Advent of Code 2015 Puzzle Solver v1.0.1',
        help='Show the version number of this package',
    )
    parser.add_argument(
        '-p',
        '--puzzle',
        type=int,
        choices=range(1, 26),
        required=True,
        help='Day of the Advent of Code 2015 puzzle',
        metavar='DAY',
        dest='day',
    )
    parser.add_argument(
        '-f',
        '--file',
        default=None,
        type=str,
        help='Input file for the Advent of Code 2015 puzzle',
        metavar='PATH',
        dest='file_name',
    )

    return parser.parse_args()


def main():
    """Solves the puzzle input from a file, if given, otherwise runs tests

    Args: None
    Returns: None
    """
    args = get_args()
    solver = factory.get_solver(args.day, args.file_name)
    if args.file_name:
        print(solver.puzzle_title)
        print(solver.get_puzzle_solution())
    else:
        print('No puzzle input was provided')
        print('Running test cases for ' + solver.puzzle_title)
        solver.run_test_cases()


if __name__ == '__main__':
    sys.exit(main())
