#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Puzzle Solver for Advent of Code 2015 Day 6
Author: James Walker
Copyright: MIT license

Description (https://adventofcode.com/2015/day/6):
--- Day 6: Probably a Fire Hazard ---

  Because your neighbors keep defeating you in the holiday house decorating
  contest year after year, you've decided to deploy one million lights in a
  1000x1000 grid.

  Furthermore, because you've been especially nice this year, Santa has mailed
  you instructions on how to display the ideal lighting configuration.

  Lights in your grid are numbered from 0 to 999 in each direction; the lights
  at each corner are at 0,0, 0,999, 999,999, and 999,0. The instructions
  include whether to turn on, turn off, or toggle various inclusive ranges
  given as coordinate pairs. Each coordinate pair represents opposite corners
  of a rectangle, inclusive; a coordinate pair like 0,0 through 2,2 therefore
  refers to 9 lights in a 3x3 square. The lights all start turned off.

  To defeat your neighbors this year, all you have to do is set up your lights
  by doing the instructions Santa sent you in order.

  For example:
    turn on 0,0 through 999,999 would turn on (or leave on) every light.
    toggle 0,0 through 999,0 would toggle the first line of 1000 lights,
      turning off the ones that were on, and turning on the ones that were off.
    turn off 499,499 through 500,500 would turn off (or leave off) the middle
      four lights.

  After following the instructions, how many lights are lit?
    Answer: 400,410

--- Day 6: Part Two ---

  You just finish implementing your winning light pattern when you realize you
  mistranslated Santa's message from Ancient Nordic Elvish. The light grid you
  bought actually has individual brightness controls; each light can have a
  brightness of zero or more. The lights all start at zero.

  The phrase turn on actually means that you should increase the brightness of
  those lights by 1. The phrase turn off actually means that you should
  decrease the brightness of those lights by 1, to a minimum of zero. The
  phrase toggle actually means that you should increase the brightness of
  those lights by 2.

  For example:
    turn on 0,0 through 0,0 would increase the total brightness by 1.
    toggle 0,0 through 999,999 would increase the total brightness by 2000000.

  What is the total brightness of all lights combined after following Santa's
  instructions?
    Answer: 15,343,601
"""

# Standard Library Imports
from collections import namedtuple
import re

# Application-specific Imports
from advent_of_code.solvers import solver


# Stores a pair of light grid coordinates
Point = namedtuple('Point', 'x y')


class LightGrid(object):
    """Abstract class for representing a 2D grid of lights

    Attributes:
        grid_size (Point): Stores maximum x- and y-coordinate of the light grid
        light_grid (list): Lights in the grid as a list of rows
    """

    def __init__(self, width=1000, height=1000):
        self._grid_size = Point(width, height)
        self._light_grid = [None] * height
        self.reset_grid()

    def reset_grid(self):
        """Turns off every light in the grid
        Args: None
        Returns: None
        """
        for row in range(0, self._grid_size.y):
            self._light_grid[row] = bytearray(self._grid_size.x)

    def count_lights(self):
        """Counts the number or total intensity of turned on lights in the grid
        Args: None
        Returns:
            int: The number or intensity of turned on lights in the grid
        """
        return sum(sum(row) for row in self._light_grid)

    def set_light_state(self, start, end, light_state):
        """Sets a row of lights to a specific state
        Args:
            start (int): The grid index for the light to begin setting states
            end (int): The grid index for the light to stop setting states
            light_state (str): Whether the lights should be 'on' or 'off'
        Returns: None
        """
        raise NotImplementedError()


class SimpleLightGrid(LightGrid):
    """Represents a 2D grid of lights that can be turned on and off

    Attributes:
        grid_size (Point): Stores maximum x- and y-coordinate of the light grid
        light_grid (list): Lights in the grid as a list of rows
    """

    def set_light_state(self, start, end, light_state):
        """Sets a row of lights to a specific state
        Args:
            start (int): The grid index for the light to begin setting states
            end (int): The grid index for the light to stop setting states
            light_state (str): Whether the lights should be 'on' or 'off'
        Returns: None
        """
        state = 1 if light_state == 'on' else 0
        for row in range(start.y, end.y + 1):
            for column in range(start.x, end.x + 1):
                self._light_grid[row][column] = state

    def toggle_light_state(self, start, end):
        """Toggles lights between on and off along indices of a grid row
        Args:
            start (int): The grid index for the light to begin toggling lights
            end (int): The grid index for the light to stop toggling lights
        Returns: None
        """
        for row in range(start.y, end.y + 1):
            for column in range(start.x, end.x + 1):
                self._light_grid[row][column] ^= 1


class ComplexLightGrid(LightGrid):
    """Represents a 2D grid of lights that can change intensity

    Attributes:
        grid_size (Point): Stores maximum x- and y-coordinate of the light grid
        light_grid (list): Lights in the grid as a list of rows
    """

    def set_light_state(self, start, end, light_state):
        """Sets a row of lights to a specific state

        Args:
            start (int): The grid index for the light to begin setting states
            end (int): The grid index for the light to stop setting states
            light_state (str): Whether the lights should be 'on' or 'off'
        Returns: None
        """
        if light_state == 'on':
            self.toggle_light_state(start, end, 1)
        else:
            for row in range(start.y, end.y + 1):
                for column in range(start.x, end.x + 1):
                    if self._light_grid[row][column]:
                        self._light_grid[row][column] -= 1

    def toggle_light_state(self, start, end, increment=2):
        """Increases the intensity for a row of lights between two indices

        Args:
            start (int): The grid index for the light to begin toggling lights
            end (int): The grid index for the light to stop toggling lights
            increment (int): The amount to increase each light's intensity
        Returns: None
        """
        end_x = end.x + 1
        for row in range(start.y, end.y + 1):
            for column in range(start.x, end_x):
                self._light_grid[row][column] += increment


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 6: Probably a Fire Hazard

    Attributes:
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
        toggle (RegexObject): Pattern for matching toggle instructions
        turn (RegexObject): Pattern for matching turn instructions
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The first grid had {0} lights lit and',
            'the second grid had a total brightness of {1}',
        ))
        toggle_pattern = 'toggle {0}'
        turn_pattern = 'turn (?P<state>on|off) {0}'
        overlap = r'(?P<x1>\d+),(?P<y1>\d+) through (?P<x2>\d+),(?P<y2>\d+)'
        self._toggle = re.compile(toggle_pattern.format(overlap))
        self._turn = re.compile(turn_pattern.format(overlap))

    @staticmethod
    def _parse_points(instruction):
        """Parses start and end points from the instruction

        Args:
            instruction (dict): Parsed coordinates for which lights to change
        Returns:
            tuple: Start and end coordinates for the intruction
        """
        start = Point(int(instruction['x1']), int(instruction['y1']))
        end = Point(int(instruction['x2']), int(instruction['y2']))
        return (start, end)

    def toggle_lights(self, light_grid, toggle_instr):
        """Changes the given lights based on their state (i.e., on or off)

        Args:
            light_grid (LightGrid): Represents a 2D grid of lights
            toggle_instr (MatchObject): Parsed coordinates for lights to change
        Returns: None
        """
        start, end = self._parse_points(toggle_instr.groupdict())
        light_grid.toggle_light_state(start, end)

    def change_light_state(self, light_grid, turn_instr):
        """Sets the given lights to a particular state (i.e., on or off)

        Args:
            light_grid (LightGrid): Represents a 2D grid of lights
            turn_instr (MatchObject): Parsed coordinates for lights to change
        Returns: None
        """
        light_instr = turn_instr.groupdict()
        start, end = self._parse_points(light_instr)
        light_grid.set_light_state(start, end, light_instr['state'])

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        simple_grid = SimpleLightGrid(width=1000, height=1000)
        complex_grid = ComplexLightGrid(width=1000, height=1000)
        for instruction in self._puzzle_input.splitlines():
            if instruction.startswith('toggle'):
                toggle_instr = self._toggle.match(instruction)
                self.toggle_lights(simple_grid, toggle_instr)
                self.toggle_lights(complex_grid, toggle_instr)
            elif instruction.startswith('turn'):
                turn_instr = self._turn.match(instruction)
                self.change_light_state(simple_grid, turn_instr)
                self.change_light_state(complex_grid, turn_instr)
        return (simple_grid.count_lights(), complex_grid.count_lights())

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        input1 = 'turn on 0,0 through 999,999'
        input2 = 'toggle 0,0 through 999,0'
        input3 = '\n'.join((input1, input2))
        input4 = 'turn off 499,499 through 500,500'
        input5 = '\n'.join((input1, input4))
        input6 = 'turn on 0,0 through 0,0'
        input7 = 'toggle 0,0 through 999,999'
        test_cases = (
            solver.TestCase(input1, '1000000', '1000000'),
            solver.TestCase(input2, '1000', '2000'),
            solver.TestCase(input3, '999000', '1002000'),
            solver.TestCase(input4, '0', '0'),
            solver.TestCase(input5, '999996', '999996'),
            solver.TestCase(input6, '1', '1'),
            solver.TestCase(input7, '1000000', '2000000'),
        )
        for test_case in test_cases:
            self._run_test_case(test_case)
