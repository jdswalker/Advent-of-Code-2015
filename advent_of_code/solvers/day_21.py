#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/21
Author: James Walker
Copyright: MIT license

--- Day 21: RPG Simulator 20XX ---

  Little Henry Case got a new video game for Christmas. It's an RPG, and he's
  stuck on a boss. He needs to know what equipment to buy at the shop. He hands
  you the controller.

  In this game, the player (you) and the enemy (the boss) take turns attacking.
  The player always goes first. Each attack reduces the opponent's hit points
  by at least 1. The first character at or below 0 hit points loses.

  Damage dealt by an attacker each turn is equal to the attacker's damage score
  minus the defender's armor score. An attacker always does at least 1 damage.
  So, if the attacker has a damage score of 8, and the defender has an armor
  score of 3, the defender loses 5 hit points. If the defender had an armor
  score of 300, the defender would still lose 1 hit point.

  Your damage score and armor score both start at zero. They can be increased
  by buying items in exchange for gold. You start with no items and have as
  much gold as you need. Your total damage or armor is equal to the sum of
  those stats from all of your items. You have 100 hit points. Here is what the
  item shop is selling:
	Weapons:    Cost  Damage  Armor
	Dagger        8     4       0
	Shortsword   10     5       0
	Warhammer    25     6       0
	Longsword    40     7       0
	Greataxe     74     8       0

	Armor:      Cost  Damage  Armor
	Leather      13     0       1
	Chainmail    31     0       2
	Splintmail   53     0       3
	Bandedmail   75     0       4
	Platemail   102     0       5

	Rings:      Cost  Damage  Armor
	Damage +1    25     1       0
	Damage +2    50     2       0
	Damage +3   100     3       0
	Defense +1   20     0       1
	Defense +2   40     0       2
	Defense +3   80     0       3

  You must buy exactly one weapon; no dual-wielding. Armor is optional, but you
  can't use more than one. You can buy 0-2 rings (at most one for each hand).
  You must use any items you buy. The shop only has one of each item, so you
  can't buy, for example, two rings of Damage +3.

  For example, suppose you have 8 hit points, 5 damage, and 5 armor, and that
  the boss has 12 hit points, 7 damage, and 2 armor:
    The player deals 5-2 = 3 damage; the boss goes down to 9 hit points.
    The boss deals 7-5 = 2 damage; the player goes down to 6 hit points.
    The player deals 5-2 = 3 damage; the boss goes down to 6 hit points.
    The boss deals 7-5 = 2 damage; the player goes down to 4 hit points.
    The player deals 5-2 = 3 damage; the boss goes down to 3 hit points.
    The boss deals 7-5 = 2 damage; the player goes down to 2 hit points.
    The player deals 5-2 = 3 damage; the boss goes down to 0 hit points.

  In this scenario, the player wins! (Barely.) You have 100 hit points. The
  boss's actual stats are in your puzzle input. What is the least amount of
  gold you can spend and still win the fight?

    Answer: 78

--- Day 21: Part Two ---

  Turns out the shopkeeper is working with the boss, and can persuade you to
  buy whatever items he wants. The other rules still apply, and he still only
  has one of each item. What is the most amount of gold you can spend and still
  lose the fight?

    Answer: 148
"""

# Standard Library Imports
from collections import namedtuple
from itertools import combinations
import re
import sys

# Application-specific Imports
from advent_of_code.solvers import solver


# Defines an item from the shop
Item = namedtuple(typename='Item', field_names='cost damage armor')


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 21: RPG Simulator 20XX

    Attributes:
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The least amount of gold needed to win is {0}.',
            'The greatest amount of gold needed to lose is {1}',
        ))

    def _get_boss(self):
        """Parses attributes for the boss from the input

        Args: None
        Returns:
            dict: Stores hit points, damage, and armor attributes for the boss
        """
        parser = re.compile(r'\d+', re.DOTALL)
        stats = parser.findall(self.puzzle_input.strip())
        return {
            'Hit Points': int(stats[0]),
            'Damage': int(stats[1]),
            'Armor': int(stats[2]),
        }

    @staticmethod
    def _get_weapons():
        """Gets list of items that can be equiped as weapons

        Args: None
        Returns:
            tuple: Every item that can be equiped as a weapon
        """
        return (
            Item(cost=8, damage=4, armor=0),   # Dagger
            Item(cost=10, damage=5, armor=0),  # Shortsword
            Item(cost=25, damage=6, armor=0),  # Warhammer
            Item(cost=40, damage=7, armor=0),  # Longsword
            Item(cost=74, damage=8, armor=0),  # Greataxe
        )

    @staticmethod
    def _get_armors():
        """Gets list of items that can be equiped as armor (including nothing)

        Args: None
        Returns:
            tuple: Every item that can be equiped as armor
        """
        return (
            Item(cost=0, damage=0, armor=0),    # Nothing
            Item(cost=13, damage=0, armor=1),   # Leather
            Item(cost=31, damage=0, armor=2),   # Chainmail
            Item(cost=53, damage=0, armor=3),   # Splintmail
            Item(cost=75, damage=0, armor=4),   # Bandedmail
            Item(cost=102, damage=0, armor=5),  # Platemail
        )

    @staticmethod
    def _get_rings():
        """Gets list of items that can be equiped as rings (including nothing)

        Args: None
        Returns:
            tuple: Every item that can be equiped as a ring
        """
        return (
            Item(cost=0, damage=0, armor=0),    # Damage +0 (Nothing, Ring 1)
            Item(cost=25, damage=1, armor=0),   # Damage +1
            Item(cost=50, damage=2, armor=0),   # Damage +2
            Item(cost=100, damage=3, armor=0),  # Damage +3
            Item(cost=0, damage=0, armor=0),    # Defense +0 (Nothing, Ring 2)
            Item(cost=20, damage=0, armor=1),   # Defense +1
            Item(cost=40, damage=0, armor=2),   # Defense +2
            Item(cost=80, damage=0, armor=3),   # Defense +3
        )

    @staticmethod
    def _get_damage(attacker, defender):
        """Calculates the net damage inflicted by the attacker on the defender

        Args:
            attacker (dict): Stores attributes for the attacker
            defender (dict): Stores attributes for the defender
        Returns:
            int: Net damage inflicted by attacker if above 0, else 1
        """
        net_damage = attacker['Damage'] - defender['Armor']
        return net_damage if net_damage > 1 else 1

    def _player_wins_battle(self, player, boss):
        """

        Args:
            player (dict): Stores attributes for the player
            boss (dict): Stores attributes for the boss
        Returns:
            bool: True if the player wins the battle, else False
        """
        player_wins = False
        player_hp, player_hit = 100, self._get_damage(player, boss)
        boss_hp, boss_hit = boss['Hit Points'], self._get_damage(boss, player)
        while player_hp > 0:
            boss_hp -= player_hit
            if boss_hp < 1:
                player_wins = True
                break
            player_hp -= boss_hit
        return player_wins

    @staticmethod
    def _get_player(weapon, armor, ring1, ring2):
        """Calculates the damage and armor for a player with their equipment

        Args:
            weapon (Item): Stores a weapon's cost and damage attributes
            armor (Item): Stores an armor's cost and armor attributes
            ring1 (Item): Stores a ring's cost and damage or armor attributes
            ring2 (Item): Stores a ring's cost and damage or armor attributes
        Returns:
            dict: Stores damage and armor attributes for a player
        """
        return {
            'Damage': weapon.damage + ring1.damage + ring2.damage,
            'Armor': armor.armor + ring1.armor + ring2.armor,
        }

    def _get_player_equipment(self):
        """

        Args: None
        Yields:
            tuple:
        """
        for weapon in self._get_weapons():
            for armor in self._get_armors():
                for ring1, ring2 in combinations(self._get_rings(), 2):
                    yield (weapon, armor, ring1, ring2)

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        boss = self._get_boss()
        min_cost = sys.maxsize
        max_cost = -1
        for weapon, armor, ring1, ring2 in self._get_player_equipment():
            cost = weapon.cost + armor.cost + ring1.cost + ring2.cost
            player = self._get_player(weapon, armor, ring1, ring2)
            if cost < min_cost and self._player_wins_battle(player, boss):
                min_cost = cost
            if cost > max_cost and not self._player_wins_battle(player, boss):
                max_cost = cost
        return (min_cost, max_cost)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        test_input1 = '\n'.join((
            'Hit Points: 1',
            'Damage: 1000',
            'Armor: 1',
        ))
        test_input2 = '\n'.join((
            'Hit Points: 1',
            'Damage: 1',
            'Armor: 1000',
        ))
        test_input3 = '\n'.join((
            'Hit Points: 1000',
            'Damage: 1000',
            'Armor: 1000',
        ))
        test_input4 = '\n'.join((
            'Hit Points: 200',
            'Damage: 0',
            'Armor: 3',
        ))
        test_input5 = '\n'.join((
            'Hit Points: 150',
            'Damage: 7',
            'Armor: 2',
        ))
        self._run_test_case(solver.TestCase(test_input1, 8, -1))
        self._run_test_case(solver.TestCase(test_input2, 8, -1))
        self._run_test_case(solver.TestCase(test_input3, sys.maxsize, 356))
        self._run_test_case(solver.TestCase(test_input4, 10, 230))
        self._run_test_case(solver.TestCase(test_input5, 101, 189))
