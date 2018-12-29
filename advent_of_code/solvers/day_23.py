#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/23
Author: James Walker
Copyright: MIT license

--- Day 23: Opening the Turing Lock ---

  Little Jane Marie just got her very first computer for Christmas from some
  unknown benefactor. It comes with instructions and an example program, but
  the computer itself seems to be malfunctioning. She's curious what the
  program does, and would like you to help her run it.

  The manual explains that the computer supports two registers and six
  instructions (truly, it goes on to remind the reader, a state-of-the-art
  technology). The registers are named a and b, can hold any non-negative
  integer, and begin with a value of 0. The instructions are as follows:
    hlf r sets register r to half its current value, then continues with the
        next instruction.
    tpl r sets register r to triple its current value, then continues with the
        next instruction.
    inc r increments register r, adding 1 to it, then continues with the next
        instruction.
    jmp offset is a jump; it continues with the instruction offset away
        relative to itself.
    jie r, offset is like jmp, but only jumps if register r is even ("jump if
        even").
    jio r, offset is like jmp, but only jumps if register r is 1 ("jump if
        one", not odd).

  All three jump instructions work with an offset relative to that instruction.
  The offset is always written with a prefix + or - to indicate the direction
  of the jump (forward or backward, respectively). For example, jmp +1 would
  simply continue with the next instruction, while jmp +0 would continuously
  jump back to itself forever. The program exits when it tries to run an
  instruction beyond the ones defined.

  For example, this program sets a to 2, because the jio instruction causes it
  to skip the tpl instruction:
    inc a
    jio a, +2
    tpl a
    inc a

  What is the value in register b when the program in your puzzle input is
  finished executing?

    Answer: 170

--- Day 23: Part Two ---

  The unknown benefactor is very thankful for releasi-- er, helping little Jane
  Marie with her computer. Definitely not to distract you, what is the value in
  register b after the program is finished executing if register a starts as 1
  instead?

    Answer: 247
"""

# Standard Library Imports
from collections import namedtuple
import re

# Application-specific Imports
from advent_of_code.solvers import solver


# Stores information about an instruction for execution
Instruction = namedtuple(
    typename='Instruction',
    field_names='type register value',
)


class Computer(object):
    """Represents a computer with 2 registers that can execute 6 instructions

    Attributes
        registers (dict): Two registers that can hold any non-negative integer
        instruction_pointer (int): Index of an instruction in the program
    """

    def __init__(self, reg_a=None, reg_b=None):
        self._registers = {
            'a': reg_a if reg_a else 0,
            'b': reg_b if reg_b else 0,
        }
        self._instruction_pointer = None

    @property
    def register_a(self):
        """Returns the non-negative integer value stored in register a

        Args: None
        Returns:
            int: Value from register a
        """
        return self._registers['a']

    @property
    def register_b(self):
        """Returns the non-negative integer value stored in register b

        Args: None
        Returns:
            int: Value from register b
        """
        return self._registers['b']

    def _process_instruction(self, instr):
        """Returns the non-negative integer value stored in register a

        Args:
            instr (Instruction): Stores execution info for the instruction
        Returns: None
        """
        if instr.type == 'hlf':
            self._registers[instr.register] //= 2
            self._instruction_pointer += 1
        elif instr.type == 'tpl':
            self._registers[instr.register] *= 3
            self._instruction_pointer += 1
        elif instr.type == 'inc':
            self._registers[instr.register] += 1
            self._instruction_pointer += 1
        elif instr.type == 'jmp':
            self._instruction_pointer += instr.value
        elif instr.type == 'jie' and not self._registers[instr.register] % 2:
            self._instruction_pointer += instr.value
        elif instr.type == 'jio' and self._registers[instr.register] == 1:
            self._instruction_pointer += instr.value
        else:
            self._instruction_pointer += 1

    def run_program(self, program):
        """Executes the instructions in the given program

        Args:
            program (list): Program instructions to execute
        Returns: None
        """
        self._instruction_pointer = 0
        number_of_instructions = len(program)
        while 0 <= self._instruction_pointer < number_of_instructions:
            self._process_instruction(program[self._instruction_pointer])


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 23: Opening the Turing Lock

    Attributes
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'The value in register b when the program finished was {0}.',
            'The value in register b when register a is set to 1 was {1}.',
        ))

    def _parse_input(self):
        """

        Args: None
        Returns:
            list: Program instructions to execute
        """
        program = []
        instruction_pattern = r'^([a-z]{3})\s([ab]?)(?:,\s)?([+-]?(?:\d+)?)'
        parser = re.compile(instruction_pattern)
        for line in self.puzzle_input.splitlines():
            if not line:
                continue
            instruction = parser.match(line)
            if not instruction:
                continue
            register = instruction.group(2) if instruction.group(2) else None
            value = int(instruction.group(3)) if instruction.group(3) else None
            program.append(Instruction(instruction.group(1), register, value))
        return program

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        program = self._parse_input()
        computer_pt1 = Computer(reg_a=0, reg_b=0)
        computer_pt2 = Computer(reg_a=1, reg_b=0)
        computer_pt1.run_program(program)
        computer_pt2.run_program(program)
        return (computer_pt1.register_b, computer_pt2.register_b)

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        test_input1 = 'inc a'
        test_input2 = 'inc b'
        self._run_test_case(solver.TestCase(test_input1, 0, 0))
        self._run_test_case(solver.TestCase(test_input2, 1, 1))
