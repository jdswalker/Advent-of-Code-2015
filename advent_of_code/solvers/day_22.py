#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/22
Author: James Walker
Copyright: MIT license

--- Day 22: Wizard Simulator 20XX ---

  Little Henry Case decides that defeating bosses with swords and stuff is
  boring. Now he's playing the game with a wizard. Of course, he gets stuck on
  another boss and needs your help again.

  In this version, combat still proceeds with the player and the boss taking
  alternating turns. The player still goes first. Now, however, you don't get
  any equipment; instead, you must choose one of your spells to cast. The first
  character at or below 0 hit points loses.

  Since you're a wizard, you don't get to wear armor, and you can't attack
  normally. However, since you do magic damage, your opponent's armor is
  ignored, and so the boss effectively has zero armor as well. As before, if
  armor (from a spell, in this case) would reduce damage below 1, it becomes 1
  instead - that is, the boss' attacks always deal at least 1 damage.

  On each of your turns, you must select one of your spells to cast. If you
  cannot afford to cast any spell, you lose. Spells cost mana; you start with
  500 mana, but have no maximum limit. You must have enough mana to cast a
  spell, and its cost is immediately deducted when you cast it. Your spells are
  Magic Missile, Drain, Shield, Poison, and Recharge.
    Magic Missile costs 53 mana. It instantly does 4 damage.
    Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit
        points.
    Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it
        is active, your armor is increased by 7.
    Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the
        start of each turn while it is active, it deals the boss 3 damage.
    Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the
        start of each turn while it is active, it gives you 101 new mana.

  Effects all work the same way. Effects apply at the start of both the
  player's turns and the boss' turns. Effects are created with a timer (the
  number of turns they last); at the start of each turn, after they apply any
  effect they have, their timer is decreased by one. If this decreases the
  timer to zero, the effect ends. You cannot cast a spell that would start an
  effect which is already active. However, effects can be started on the same
  turn they end.

  For example, suppose the player has 10 hit points and 250 mana, and that the
  boss has 13 hit points and 8 damage:
    -- Player turn --
    - Player has 10 hit points, 0 armor, 250 mana
    - Boss has 13 hit points
    Player casts Poison.

    -- Boss turn --
    - Player has 10 hit points, 0 armor, 77 mana
    - Boss has 13 hit points
    Poison deals 3 damage; its timer is now 5.
    Boss attacks for 8 damage.

    -- Player turn --
    - Player has 2 hit points, 0 armor, 77 mana
    - Boss has 10 hit points
    Poison deals 3 damage; its timer is now 4.
    Player casts Magic Missile, dealing 4 damage.

    -- Boss turn --
    - Player has 2 hit points, 0 armor, 24 mana
    - Boss has 3 hit points
    Poison deals 3 damage. This kills the boss, and the player wins.

  Now, suppose the same initial conditions, except that the boss has 14 hit
  points instead:

    -- Player turn --
    - Player has 10 hit points, 0 armor, 250 mana
    - Boss has 14 hit points
    Player casts Recharge.

    -- Boss turn --
    - Player has 10 hit points, 0 armor, 21 mana
    - Boss has 14 hit points
    Recharge provides 101 mana; its timer is now 4.
    Boss attacks for 8 damage!

    -- Player turn --
    - Player has 2 hit points, 0 armor, 122 mana
    - Boss has 14 hit points
    Recharge provides 101 mana; its timer is now 3.
    Player casts Shield, increasing armor by 7.

    -- Boss turn --
    - Player has 2 hit points, 7 armor, 110 mana
    - Boss has 14 hit points
    Shield's timer is now 5.
    Recharge provides 101 mana; its timer is now 2.
    Boss attacks for 8 - 7 = 1 damage!

    -- Player turn --
    - Player has 1 hit point, 7 armor, 211 mana
    - Boss has 14 hit points
    Shield's timer is now 4.
    Recharge provides 101 mana; its timer is now 1.
    Player casts Drain, dealing 2 damage, and healing 2 hit points.

    -- Boss turn --
    - Player has 3 hit points, 7 armor, 239 mana
    - Boss has 12 hit points
    Shield's timer is now 3.
    Recharge provides 101 mana; its timer is now 0.
    Recharge wears off.
    Boss attacks for 8 - 7 = 1 damage!

    -- Player turn --
    - Player has 2 hit points, 7 armor, 340 mana
    - Boss has 12 hit points
    Shield's timer is now 2.
    Player casts Poison.

    -- Boss turn --
    - Player has 2 hit points, 7 armor, 167 mana
    - Boss has 12 hit points
    Shield's timer is now 1.
    Poison deals 3 damage; its timer is now 5.
    Boss attacks for 8 - 7 = 1 damage!

    -- Player turn --
    - Player has 1 hit point, 7 armor, 167 mana
    - Boss has 9 hit points
    Shield's timer is now 0.
    Shield wears off, decreasing armor by 7.
    Poison deals 3 damage; its timer is now 4.
    Player casts Magic Missile, dealing 4 damage.

    -- Boss turn --
    - Player has 1 hit point, 0 armor, 114 mana
    - Boss has 2 hit points
    Poison deals 3 damage. This kills the boss, and the player wins.

  You start with 50 hit points and 500 mana points. The boss's actual stats
  are in your puzzle input. What is the least amount of mana you can spend and
  still win the fight? (Do not include mana recharge effects as "spending"
  negative mana.)

    Answer: 900

--- Day 22: Part Two ---

  On the next run through the game, you increase the difficulty to hard. At the
  start of each player turn (before any other effects apply), you lose 1 hit
  point. If this brings you to or below 0 hit points, you lose.

  With the same starting stats for you and the boss, what is the least amount
  of mana you can spend and still win the fight?

    Answer: 1216
"""

# Standard Library Imports
from collections import namedtuple
import heapq
import re
import sys

# Application-specific Imports
from advent_of_code.solvers import solver


# Defines containers relevant to the game mechanics
Spell = namedtuple(typename='Spell', field_names='cost effect turns')
Player = namedtuple(typename='Player', field_names='hit_pts mana')
Boss = namedtuple(typename='Boss', field_names='hit_pts damage')
Effects = namedtuple(typename='Effects', field_names='shield poison recharge')
Move = namedtuple(
    typename='Move',
    field_names='turn mana_used player boss effects',
)


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 22: Wizard Simulator 20XX

    Attributes
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The least amount of mana needed to win normally is {0}.',
            'The least amount of mana needed to win on hard mode is {1}',
        ))
        self._magic_missile = Spell(cost=53, effect=4, turns=None)
        self._drain = Spell(cost=73, effect=2, turns=None)
        self._shield = Spell(cost=113, effect=7, turns=6)
        self._poison = Spell(cost=173, effect=3, turns=6)
        self._recharge = Spell(cost=229, effect=101, turns=5)
        self._boss_raw_damage = None

    def _get_boss(self):
        """Parses attributes for the boss from the input

        Args: None
        Returns:
            Boss: Stores hit points and damage attributes for the boss
        """
        # parser = re.compile(r'\d+', re.DOTALL)
        # stats = parser.findall(self.puzzle_input.strip())
        stats = re.findall(r'\d+', self.puzzle_input.strip(), re.DOTALL)
        self._boss_raw_damage = int(stats[1])
        return Boss(hit_pts=int(stats[0]), damage=self._boss_raw_damage)

    def _cast_magic_missile(self, player, boss):
        """Magic Missile costs 53 mana. It instantly does 4 damage.

        Args:
            player (Player): Stores attributes for the player
            boss (Boss): Stores attributes for the boss
        Returns:
            tuple: Updated attributes for player and boss after casting spell
        """
        new_player = Player(
            hit_pts=player.hit_pts,
            mana=player.mana - self._magic_missile.cost,
        )
        new_boss = Boss(boss.hit_pts - self._magic_missile.effect, boss.damage)
        return (new_player, new_boss)

    def _cast_drain(self, player, boss):
        """Drain costs 73 mana. It instantly does 2 damage and heals you for 2
        hit points.

        Args:
            player (Player): Stores attributes for the player
            boss (Boss): Stores attributes for the boss
        Returns:
            tuple: Updated attributes for player and boss after casting spell
        """
        new_player = Player(
            hit_pts=player.hit_pts + self._drain.effect,
            mana=player.mana - self._drain.cost,
        )
        new_boss = Boss(boss.hit_pts - self._drain.effect, boss.damage)
        return (new_player, new_boss)

    def _cast_shield(self, player, boss, effects):
        """Shield costs 113 mana. It starts an effect that lasts for 6 turns.
        While it is active, your armor is increased by 7.

        Args:
            player (Player): Stores attributes for the player
            boss (Boss): Stores attributes for the boss
            effects (Effects): Stores turns remaining for each spell effect
        Returns:
            tuple: Updated attributes for player, boss, and spell effects
        """
        new_player = Player(player.hit_pts, player.mana - self._shield.cost)
        boss_dmg = self._boss_raw_damage - self._shield.effect
        if boss_dmg < 1:
            boss_dmg = 1
        new_boss = Boss(boss.hit_pts, boss_dmg)
        new_effects = Effects(
            shield=self._shield.turns,
            poison=effects.poison,
            recharge=effects.recharge,
        )
        return (new_player, new_boss, new_effects)

    def _cast_poison(self, player, effects):
        """Poison costs 173 mana. It starts an effect that lasts for 6 turns.
        At the start of each turn while it is active, it deals the boss 3
        damage.

        Args:
            player (Player): Stores attributes for the player
            effects (Effects): Stores turns remaining for each spell effect
        Returns:
            tuple: Updated attributes for player and spell effects
        """
        new_player = Player(player.hit_pts, player.mana - self._poison.cost)
        new_effects = Effects(
            shield=effects.shield,
            poison=self._poison.turns,
            recharge=effects.recharge,
        )
        return (new_player, new_effects)

    def _cast_recharge(self, player, effects):
        """Recharge costs 229 mana. It starts an effect that lasts for 5 turns.
        At the start of each turn while it is active, it gives you 101 new
        mana.

        Args:
            player (Player): Stores attributes for the player
            effects (Effects): Stores turns remaining for each spell effect
        Returns:
            tuple: Updated attributes for player and spell effects
        """
        new_player = Player(player.hit_pts, player.mana - self._recharge.cost)
        new_effects = Effects(
            shield=effects.shield,
            poison=effects.poison,
            recharge=self._recharge.turns,
        )
        return (new_player, new_effects)

    def _add_player_moves(self, move, moves, player, boss, effects):
        """

        Args:
            move (Move): Stores the state of the fight after the previous turn
            moves (list): Possible moves that can be made each turn
            player (Player): Stores attributes for the player
            boss (Boss): Stores attributes for the boss
            effects (Effects): Stores turns remaining for each spell effect
        Returns: None
        """
        if player.mana < self._magic_missile.cost:
            return
        next_turn = move.turn + 1
        if player.mana >= self._magic_missile.cost:
            _mana_used = move.mana_used + self._magic_missile.cost
            _player, _boss = self._cast_magic_missile(player, boss)
            new_move = Move(next_turn, _mana_used, _player, _boss, effects)
            if new_move not in moves:
                heapq.heappush(moves, new_move)
            if _boss.hit_pts < 1:
                return
        if player.mana >= self._drain.cost:
            _mana_used = move.mana_used + self._drain.cost
            _player, _boss = self._cast_drain(player, boss)
            new_move = Move(next_turn, _mana_used, _player, _boss, effects)
            if new_move not in moves:
                heapq.heappush(moves, new_move)
            if _boss.hit_pts < 1:
                return
        if not effects.shield and player.mana >= self._shield.cost:
            _mana_used = move.mana_used + self._shield.cost
            _player, _boss, _effects = self._cast_shield(player, boss, effects)
            new_move = Move(next_turn, _mana_used, _player, _boss, _effects)
            if new_move not in moves:
                heapq.heappush(moves, new_move)
        if not effects.poison and player.mana >= self._poison.cost:
            _mana_used = move.mana_used + self._poison.cost
            _player, _effects = self._cast_poison(player, effects)
            new_move = Move(next_turn, _mana_used, _player, boss, _effects)
            if new_move not in moves:
                heapq.heappush(moves, new_move)
        if not effects.recharge and player.mana >= self._recharge.cost:
            _mana_used = move.mana_used + self._recharge.cost
            _player, _effects = self._cast_recharge(player, effects)
            new_move = Move(next_turn, _mana_used, _player, boss, _effects)
            if new_move not in moves:
                heapq.heappush(moves, new_move)

    @staticmethod
    def _add_boss_move(move, moves, player, boss, effects):
        """

        Args:
            move (Move): Stores the state of the fight after the previous turn
            moves (list): Possible moves that can be made each turn
            player (Player): Stores attributes for the player
            boss (Boss): Stores attributes for the boss
            effects (Effects): Stores turns remaining for each spell effect
        Returns: None
        """
        if player.hit_pts < 1:
            return
        next_turn = move.turn + 1
        new_player = Player(player.hit_pts - boss.damage, player.mana)
        new_move = Move(next_turn, move.mana_used, new_player, boss, effects)
        if new_move not in moves:
            heapq.heappush(moves, new_move)

    def _apply_spells(self, move, hard_mode):
        """

        Args:
            move (Move): Stores the state of the fight after the previous turn
            hard_mode (bool): Removes 1 hit point from the player if True
        Returns: None
        """
        boss_hp, boss_dmg = move.boss.hit_pts, move.boss.damage
        player_hp, player_mana = move.player.hit_pts, move.player.mana
        if hard_mode and not move.turn & 1:
            player_hp -= 1
        if not move.effects.shield:
            boss_dmg = self._boss_raw_damage
        if move.effects.poison:
            boss_hp -= self._poison.effect
        if move.effects.recharge:
            player_mana += self._recharge.effect
        new_player = Player(player_hp, player_mana)
        new_boss = Boss(boss_hp, boss_dmg)
        new_effects = Effects(
            shield=move.effects.shield - 1 if move.effects.shield else 0,
            poison=move.effects.poison - 1 if move.effects.poison else 0,
            recharge=move.effects.recharge - 1 if move.effects.recharge else 0,
        )
        return (new_player, new_boss, new_effects)

    def _get_min_mana(self, player, boss, hard_mode):
        """

        Args:
            player (Player): Stores attributes for the player
            boss (Boss): Stores attributes for the boss
            hard_mode (bool): Removes 1 hit point from the player if True
        Returns: None
        """
        min_mana_used = sys.maxsize
        moves = [Move(0, 0, player, boss, Effects(0, 0, 0))]
        while moves:
            move = heapq.heappop(moves)
            if move.player.hit_pts < 1 or move.mana_used > min_mana_used:
                continue
            if move.boss.hit_pts < 1:
                min_mana_used = min(min_mana_used, move.mana_used)
                continue
            _player, _boss, _effects = self._apply_spells(move, hard_mode)
            if _player.hit_pts < 1:
                continue
            if _boss.hit_pts < 1:
                min_mana_used = min(min_mana_used, move.mana_used)
                continue
            if move.turn & 1:  # True when turn is an odd number
                self._add_boss_move(move, moves, _player, _boss, _effects)
            else:
                self._add_player_moves(move, moves, _player, _boss, _effects)
        return min_mana_used

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        player, boss = Player(hit_pts=50, mana=500), self._get_boss()
        mana_hard_mode = self._get_min_mana(player, boss, hard_mode=True)
        mana_normal_mode = self._get_min_mana(player, boss, hard_mode=False)
        return (mana_normal_mode, mana_hard_mode)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        test_input1 = '\n'.join(('Hit Points: 1', 'Damage: 100'))
        test_input2 = '\n'.join(('Hit Points: 5', 'Damage: 49'))
        test_input3 = '\n'.join(('Hit Points: 50', 'Damage: 1'))
        test_input4 = '\n'.join(('Hit Points: 50', 'Damage: 8'))
        self._run_test_case(solver.TestCase(test_input1, 53, 53))
        self._run_test_case(solver.TestCase(test_input2, 106, 126))
        self._run_test_case(solver.TestCase(test_input3, 787, 787))
        self._run_test_case(solver.TestCase(test_input4, 787, 900))
