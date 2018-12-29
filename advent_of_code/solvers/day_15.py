#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/15
Author: James Walker
Copyright: MIT license

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


Ingredient = namedtuple(
    typename='Ingredient',
    field_names='capacity durability flavor texture calories',
)


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 15: Science for Hungry People

    Attributes
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The highest-score with these cookie ingredients has {0} points.',
            'The highest-score cookie with 500 calories has {1} points.',
        ))

    @staticmethod
    def _parse_ingredient_info(ingredient):
        """

        Args:
            ingredient
        Returns:
            tuple:
        """
        name = ingredient.group(1)
        stats = Ingredient(
            int(ingredient.group(2)),  # capacity
            int(ingredient.group(3)),  # durability
            int(ingredient.group(4)),  # flavor
            int(ingredient.group(5)),  # texture
            int(ingredient.group(6)),  # calories
        )
        return (name, stats)

    def _parse_input(self):
        """

        Args: None
        Returns:
            dict:
        """
        ingredient_pattern = r'(\w+)' + ''.join([r'[^\d-]+(-?\d+)'] * 5)
        parser = re.compile(ingredient_pattern)
        ingredients = {}
        for line in self.puzzle_input.splitlines():
            ingredient = parser.match(line)
            if not ingredient:
                continue
            name, stats = self._parse_ingredient_info(ingredient)
            ingredients[name] = stats
        return ingredients

    @staticmethod
    def _get_recipe_score(recipe, ingredients):
        """

        Args:
            recipe
            ingredients
        Returns:
            int:
        """
        capacity = sum(ingredients[name].capacity for name in recipe)
        durability = sum(ingredients[name].durability for name in recipe)
        flavor = sum(ingredients[name].flavor for name in recipe)
        texture = sum(ingredients[name].texture for name in recipe)
        score = 0 if capacity < 1 else capacity
        score *= 0 if durability < 1 else durability
        score *= 0 if flavor < 1 else flavor
        score *= 0 if texture < 1 else texture
        return score

    def _get_healthy_score(self, recipe, ingredients):
        """

        Args:
            recipe
            ingredients
        Returns:
            int:
        """
        calories = sum(ingredients[name].calories for name in recipe)
        healthy_score = -1
        if calories == 500:
            healthy_score = self._get_recipe_score(recipe, ingredients)
        return healthy_score

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        ingredients = self._parse_input()
        max_score = 0
        max_score_healthy = 0
        teaspoons = 100
        for recipe in combinations(ingredients.keys(), teaspoons):
            recipe_score = self._get_recipe_score(recipe, ingredients)
            healthy_recipe_score = self._get_healthy_score(recipe, ingredients)
            max_score = max(recipe_score, max_score)
            max_score_healthy = max(healthy_recipe_score, max_score_healthy)
        return (max_score, max_score_healthy)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        test_input = '\n'.join(((
            'Butterscotch: '
            'capacity -1, durability -2, flavor 6, texture 3, calories 8'
        ), (
            'Cinnamon: '
            'capacity 2, durability 3, flavor -2, texture -1, calories 3'
        )))
        self._run_test_case(solver.TestCase(test_input, 62842880, 57600000))
