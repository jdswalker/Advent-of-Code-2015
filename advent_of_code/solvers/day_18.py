#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/18
Author: James Walker
Copyright: MIT license

--- Day 18: Like a GIF For Your Yard ---

  After the million lights incident, the fire code has gotten stricter: now,
  at most ten thousand lights are allowed. You arrange them in a 100x100 grid.

  Never one to let you down, Santa again mails you instructions on the ideal
  lighting configuration. With so few lights, he says, you'll have to resort to
  animation.

  Start by setting your lights to the included initial configuration (your
  puzzle input). A # means "on", and a . means "off".

  Then, animate your grid in steps, where each step decides the next
  configuration based on the current one. Each light's next state (either on or
  off) depends on its current state and the current states of the eight lights
  adjacent to it (including diagonals). Lights on the edge of the grid might
  have fewer than eight neighbors; the missing ones always count as "off".

  For example, in a simplified 6x6 grid, the light marked A has the neighbors
  numbered 1 through 8, and the light marked B, which is on an edge, only has
  the neighbors marked 1 through 5:
    1B5...
    234...
    ......
    ..123.
    ..8A4.
    ..765.

  The state a light should have next is based on its current state (on or off)
  plus the number of neighbors that are on:
    A light which is on stays on when 2 or 3 neighbors are on, and turns off
      otherwise.
    A light which is off turns on if exactly 3 neighbors are on, and stays off
      otherwise.

  All of the lights update simultaneously; they all consider the same current
  state before moving to the next.

  Here's a few steps from an example configuration of another 6x6 grid:

  Initial state:
    .#.#.#
    ...##.
    #....#
    ..#...
    #.#..#
    ####..

  After 1 step:
    ..##..
    ..##.#
    ...##.
    ......
    #.....
    #.##..

  After 2 steps:
    ..###.
    ......
    ..###.
    ......
    .#....
    .#....

  After 3 steps:
    ...#..
    ......
    ...#..
    ..##..
    ......
    ......

  After 4 steps:
    ......
    ......
    ..##..
    ..##..
    ......
    ......

  After 4 steps, this example has four lights on. In your grid of 100x100
  lights, given your initial configuration, how many lights are on after 100
  steps?

    Answer: 821

--- Day 18: Part Two ---

  You flip the instructions over; Santa goes on to point out that this is all
  just an implementation of Conway's Game of Life. At least, it was, until you
  notice that something's wrong with the grid of lights you bought: four
  lights, one in each corner, are stuck on and can't be turned off. The example
  above will actually run like this:

  Initial state:
    ##.#.#
    ...##.
    #....#
    ..#...
    #.#..#
    ####.#

  After 1 step:
    #.##.#
    ####.#
    ...##.
    ......
    #...#.
    #.####

  After 2 steps:
    #..#.#
    #....#
    .#.##.
    ...##.
    .#..##
    ##.###

  After 3 steps:
    #...##
    ####.#
    ..##.#
    ......
    ##....
    ####.#

  After 4 steps:
    #.####
    #....#
    ...#..
    .##...
    #.....
    #.#..#

  After 5 steps:
    ##.###
    .##..#
    .##...
    .##...
    #.#...
    ##...#

  After 5 steps, this example now has 17 lights on. In your grid of 100x100
  lights, given your initial configuration, but with the four corners always in
  the on state, how many lights are on after 100 steps?

    Answer: 886
"""

# Application-specific Imports
from advent_of_code.solvers import solver


class LightGrid(object):
    """Class for representing a 2D grid of lights

    Attributes:
        light_grid (list): Lights in the grid as a list of rows
        broken (bool):
    """

    def __init__(self, rows, broken=False):
        self._light_grid = [
            bytearray((0 if light == '.' else 1 for light in row))
            for row in rows
        ]
        self._broken = broken
        if self._broken:
            self._light_grid[0][0] = self._light_grid[0][-1] = 1
            self._light_grid[-1][0] = self._light_grid[-1][-1] = 1

    def _get_lit_neighbor_coordinates(self, row, col):
        """

        Args:
            row (int):
            col (int):
        Returns:
            int:
        """
        neighbors = []
        for row_num in range(row - 1, row + 2):
            if -1 < row_num < len(self._light_grid):
                neighbors.extend((
                    (row_num, col_num) for col_num in range(col - 1, col + 2)
                    if -1 < col_num < len(self._light_grid)
                ))
        neighbors.remove((row, col))  # A light cannot be its own neighbor
        return sum(self._light_grid[r][c] for r, c in neighbors)

    def _toggle_light(self, row, col):
        """

        Args:
            row (int):
            col (int):
        Returns:
            int:
        """
        other_lights = self._get_lit_neighbor_coordinates(row, col)
        if self._light_grid[row][col]:
            light = 0 if other_lights not in (2, 3) else 1
        else:
            light = 0 if other_lights != 3 else 1
        return light

    def toggle_lights(self):
        """Applies rules for turning lights on and off

        Args: None
        Returns: None
        """
        num_rows, num_cols = len(self._light_grid), len(self._light_grid[0])
        light_grid = [bytearray(num_cols) for _ in range(num_rows)]
        for row in range(num_rows):
            for col in range(num_cols):
                light_grid[row][col] = self._toggle_light(row, col)
        if self._broken:
            light_grid[0][0] = light_grid[0][-1] = 1
            light_grid[-1][0] = light_grid[-1][-1] = 1
        self._light_grid = light_grid

    def count_lights(self):
        """Counts the number or total intensity of turned on lights in the grid

        Args: None
        Returns:
            int: The number or intensity of turned on lights in the grid
        """
        return sum(sum(row) for row in self._light_grid)

    def get_lights(self):
        """

        Args: None
        Returns:
            str:
        """
        lights = []
        for row in self._light_grid:
            lights.append(''.join(('#' if light else '.' for light in row)))
        lights.append('')
        return '\n'.join(lights)


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 18: Like a GIF For Your Yard

    Attributes:
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The first grid had {0} lights lit.',
            'The broken grid had {1} lights lit.',
        ))

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        light_grid = LightGrid(self.puzzle_input.splitlines())
        broken_grid = LightGrid(self.puzzle_input.splitlines(), broken=True)
        num_steps = 100
        for _ in range(num_steps):
            light_grid.toggle_lights()
            broken_grid.toggle_lights()
        return (light_grid.count_lights(), broken_grid.count_lights())

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        test_input = '\n'.join((
            '.#.#.#',
            '...##.',
            '#....#',
            '..#...',
            '#.#..#',
            '####..',
        ))
        self._run_test_case(solver.TestCase(test_input, 4, 7))
