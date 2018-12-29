#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015
Author: James Walker
Copyright: MIT license

Purpose:
  Advent of Code is a series of small programming puzzles for a variety of
  skill levels. They are self-contained and are just as appropriate for an
  expert who wants to stay sharp as they are for a beginner who is just
  learning to code. Each puzzle calls upon different skills and has two parts
  that build on a theme.
"""

# Standard Library Imports
import argparse
import sys

# Application-specific Imports
from advent_of_code.solvers import factory


def get_args_for_script(input_args=None):
    """Parses the command-line inputs to the script unless given a list

    Args
        inputArgs (list): The input parameters to the script
    Returns
        Namespace: An object populated with the values of the input arguments
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
        version='%(prog)s v1.0.0',
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
        dest='puzzle',
    )
    parser.add_argument(
        '-i',
        '--input',
        default=None,
        type=str,
        help='Input file for the Advent of Code 2015 puzzle',
        metavar='FILE',
        dest='input_file',
    )

    return parser.parse_args(input_args) if input_args else parser.parse_args()


def solve_puzzle(argv):
    """Solves the puzzle input from a file, if given, otherwise runs tests

    Args:
        argv (list): Command-line or input parameters for the program
    Returns: None
    """
    args = get_args_for_script(argv)
    solver = factory.get_solver(args.puzzle, args.input_file)
    if args.input_file is None:
        print('No puzzle input was provided')
        print('Running test cases for ' + solver.puzzle_title)
        solver.run_test_cases()
    else:
        print(solver.puzzle_title)
        print(solver.get_puzzle_solution())


if __name__ == '__main__':
    sys.exit(solve_puzzle(sys.argv[1:]))
