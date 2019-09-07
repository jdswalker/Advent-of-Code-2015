#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Puzzle Solver for Advent of Code 2015 Day 15
Author: James Walker
Copyright: MIT license

Description (https://adventofcode.com/2015/day/15):
--- Day 15: Science for Hungry People ---

  Today, you set out on the task of perfecting your milk-dunking cookie recipe.
  All you have to do is find the right balance of ingredients.

  Your recipe leaves room for exactly 100 teaspoons of ingredients. You make a
  list of the remaining ingredients you could use to finish the recipe (your
  puzzle input) and their properties per teaspoon:
    capacity (how well it helps the cookie absorb milk)
    durability (how well it keeps the cookie intact when full of milk)
    flavor (how tasty it makes the cookie)
    texture (how it improves the feel of the cookie)
    calories (how many calories it adds to the cookie)

  You can only measure ingredients in whole-teaspoon amounts accurately, and
  you have to be accurate so you can reproduce your results in the future. The
  total score of a cookie can be found by adding up each of the properties
  (negative totals become 0) and then multiplying together everything except
  calories.

  For instance, suppose you have these two ingredients:
    Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
    Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3

    Then, choosing to use 44 teaspoons of butterscotch and 56 teaspoons of
    cinnamon (because the amounts of each ingredient must add up to 100) would
    result in a cookie with the following properties:
      A capacity of 44*-1 + 56*2 = 68
      A durability of 44*-2 + 56*3 = 80
      A flavor of 44*6 + 56*-2 = 152
      A texture of 44*3 + 56*-1 = 76

    Multiplying these together (68 * 80 * 152 * 76, ignoring calories for now)
    results in a total score of 62842880, which happens to be the best score
    possible given these ingredients. If any properties had produced a negative
    total, it would have instead become zero, causing the whole score to
    multiply to zero.

  Given the ingredients in your kitchen and their properties, what is the total
  score of the highest-scoring cookie you can make?
    Answer: 18965440

--- Day 15: Part Two ---

  Your cookie recipe becomes wildly popular! Someone asks if you can make
  another recipe that has exactly 500 calories per cookie (so they can use it
  as a meal replacement). Keep the rest of your award-winning process the same
  (100 teaspoons, same ingredients, same scoring system).

  For example, given the ingredients above, if you had instead selected 40
  teaspoons of butterscotch and 60 teaspoons of cinnamon (which still adds to
  100), the total calorie count would be 40*8 + 60*3 = 500. The total score
  would go down, though: only 57600000, the best you can do in such trying
  circumstances.

  Given the ingredients in your kitchen and their properties, what is the total
  score of the highest-scoring cookie you can make with a calorie total of 500?
    Answer: 15862900
"""

# Standard Library Imports
from collections import namedtuple
from itertools import combinations_with_replacement as combinations
import re

# Application-specific Imports
from advent_of_code.solvers import solver


# Stores metadata about a recipe ingredient
Ingredient = namedtuple(
    typename='Ingredient',
    field_names='capacity durability flavor texture calories',
)


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 15: Science for Hungry People

    Attributes:
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The highest-scoring with these cookie ingredients has {0} points.',
            'The highest-scoring cookie with 500 calories has {1} points.',
        ))

    def _parse_input(self):
        """Parses recipe ingredients and associated metadata

        Args: None
        Returns:
            dict: Item names mapped to Ingredient namedtuples
        """
        ingredient_pattern = r'(\w+)' + ''.join([r'[^\d-]+(-?\d+)'] * 5)
        parser = re.compile(ingredient_pattern)
        pantry = {}
        for line in self.puzzle_input.splitlines():
            ingredient = parser.match(line)
            if ingredient is None:
                continue
            item = ingredient.group(1)
            pantry[item] = Ingredient(
                capacity=int(ingredient.group(2)),
                durability=int(ingredient.group(3)),
                flavor=int(ingredient.group(4)),
                texture=int(ingredient.group(5)),
                calories=int(ingredient.group(6)),
            )
        return pantry

    @staticmethod
    def _get_max_score(recipe, pantry):
        """Calculates the highest score possible for the recipe

        Args:
            recipe (list): Combination of ingredients for making the cookie
            pantry (dict): Item names mapped to Ingredient namedtuples
        Returns:
            int: Highest possible score for the given cookie recipe
        """
        score = max(0, sum(pantry[item].capacity for item in recipe))
        score *= max(0, sum(pantry[item].durability for item in recipe))
        score *= max(0, sum(pantry[item].flavor for item in recipe))
        score *= max(0, sum(pantry[item].texture for item in recipe))
        return score

    def _get_alt_score(self, recipe, pantry):
        """Calculates the highest score if the recipe has exactly 500 calories

        Args:
            recipe (list): Combination of ingredients for making the cookie
            pantry (dict): Item names mapped to Ingredient namedtuples
        Returns:
            int: Highest possible score for a 500 calory cookie recipe
        """
        calories = sum(pantry[ingredient].calories for ingredient in recipe)
        return self._get_max_score(recipe, pantry) if calories == 500 else -1

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        pantry = self._parse_input()
        teaspoons = 100
        max_score, alt_score = 0, 0
        for recipe in combinations(pantry.keys(), teaspoons):
            max_score = max(max_score, self._get_max_score(recipe, pantry))
            alt_score = max(alt_score, self._get_alt_score(recipe, pantry))
        return max_score, alt_score

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        item = '{0}: capacity {1}, durability {2}, flavor {3}'
        item += ', texture {4}, calories {5}'
        input1 = (
            item.format('Butterscotch', -1, -2, 6, 3, 8),
            item.format('Cinnamon', 2, 3, -2, -1, 3),
        )
        input2 = input1 + (item.format('Sugar', 1, 1, 1, 1, 1),)
        input3 = input1 + (item.format('Boogers', 2, 2, 2, 2, 2),)
        test_cases = (
            solver.TestCase('\n'.join(input1), 62842880, 57600000),
            solver.TestCase('\n'.join(input2), 105187500, 65014560),
            solver.TestCase('\n'.join(input3), 1600000000, 130975000),
        )
        for test_case in test_cases:
            self._run_test_case(test_case)
