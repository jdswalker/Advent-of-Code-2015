#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Advent of Code 2015 from http://adventofcode.com/2015/day/7
Author: James Walker
Copyright: MIT license

--- Day 7: Some Assembly Required ---

  This year, Santa brought little Bobby Tables a set of wires and bitwise logic
  gates! Unfortunately, little Bobby is a little under the recommended age
  range, and he needs help assembling the circuit.

  Each wire has an identifier (some lowercase letters) and can carry a 16-bit
  signal (a number from 0 to 65535). A signal is provided to each wire by a
  gate, another wire, or some specific value. Each wire can only get a signal
  from one source, but can provide its signal to multiple destinations. A gate
  provides no signal until all of its inputs have a signal.

  The included instructions booklet describes how to connect the parts
  together: x AND y -> z means to connect wires x and y to an AND gate, and
  then connect its output to wire z.

  For example:
    123 -> x means that the signal 123 is provided to wire x.
    x AND y -> z means that the bitwise AND of wire x and wire y is provided
        to wire z.
    p LSHIFT 2 -> q means that the value from wire p is left-shifted by 2 and
        then provided to wire q.
    NOT e -> f means that the bitwise complement of the value from wire e is
        provided to wire f.

  Other possible gates include OR (bitwise OR) and RSHIFT (right-shift). If,
  for some reason, you'd like to emulate the circuit instead, almost all
  programming languages (for example, C, JavaScript, or Python) provide
  operators for these gates.

  For example, here is a simple circuit:
    123 -> x
    456 -> y
    x AND y -> d
    x OR y -> e
    x LSHIFT 2 -> f
    y RSHIFT 2 -> g
    NOT x -> h
    NOT y -> i

  After it is run, these are the signals on the wires:
    d: 72
    e: 507
    f: 492
    g: 114
    h: 65412
    i: 65079
    x: 123
    y: 456

  In little Bobby's kit's instructions booklet (provided as your puzzle input),
  what signal is ultimately provided to wire a?
    Answer: 956

--- Day 7: Part Two ---

  Now, take the signal you got on wire a, override wire b to that signal, and
  reset the other wires (including wire a). What new signal is ultimately
  provided to wire a?
    Answer: 40149
"""

# Standard Library Imports
import re

# Application-specific Imports
from advent_of_code.solvers import solver


class Solver(solver.AdventOfCodeSolver):
    """Advent of Code 2015 Day 7: Some Assembly Required

    Attributes
        puzzle_input (list): A list of instructions for solving the puzzle
        puzzle_title (str): Name of the Advent of Code puzzle
        solved_output (str): A template string for solution output
        instructions (dict): Compiled regex for parsing instructions
        wire_tracker (dict): Dictionary of dictionaries holding wire info
    """

    def __init__(self, *args):
        solver.AdventOfCodeSolver.__init__(self, *args)
        self._solved_output = '\n'.join((
            'Wire "a" initially had a signal of {0}, but after feeding it',
            'back in to Wire "b", Wire "a" ultimately had a signal of {1}',
        ))
        self._instructions = {
            'SIGNAL_WIRE': re.compile(r'(\w+) -> (\w+)'),
            'AND_GATE': re.compile(r'(\w+) AND (\w+) -> (\w+)'),
            'OR_GATE': re.compile(r'(\w+) OR (\w+) -> (\w+)'),
            'NOT_GATE': re.compile(r'NOT (\w+) -> (\w+)'),
            'LEFT_SHIFT': re.compile(r'(\w+) LSHIFT (\d+) -> (\w+)'),
            'RIGHT_SHIFT': re.compile(r'(\w+) RSHIFT (\d+) -> (\w+)'),
        }
        self._wire_tracker = {}

    def _get_source_circuit(self, signal):
        """Initializes and or retrieves a circuit based on the input given

        Args:
            signal (str): A number for a signal value or letters for a wire ID
        Returns:
            (dict): A dictionary of wire and circuit attributes
        """
        source_circuit = None
        if signal in self._wire_tracker:
            # Circuit already initialized
            source_circuit = self._wire_tracker[signal]
        else:
            wire_id = None
            try:
                wire_signal = int(signal)
            except ValueError:
                wire_signal = None
                wire_id = signal  # Should be letters for a wire ID

            source_circuit = {
                'id': wire_id,
                'source_type': None,
                'input_a': None,
                'input_b': None,
                'outputs': set(),
                'signal': wire_signal,
            }
            if wire_id is not None:
                # Circuit must be new, so add it to the tracker
                self._wire_tracker[wire_id] = source_circuit
        return source_circuit

    def _update_input_circuit(self, source_circuit, signal, label):
        """Updates the signal source for a circuit

        Args:
            source_circuit (dict): A dictionary of wire and circuit attributes
            signal (str): The ID or source signal of one of the circuit inputs
            label (str): A wire ID key for the source_circuit dictionary
        Returns: None
        """
        input_circuit = self._get_source_circuit(signal)
        source_circuit[label] = input_circuit
        if input_circuit['id'] is not None:
            input_circuit['outputs'].add(source_circuit['id'])

    def _input_handler(self, output, handler_type, input_a, input_b=None):
        """Sets up inputs and circuit type for the given output circuit

        Args:
            output (str): The ID or source signal of the circuit's output
            handler_type (str): Specifies the logic circuit type
            input_a (str): The ID or source signal of one of the circuit inputs
            input_b (str): The ID or source signal of one of the circuit inputs
        Returns: None
        """
        source_circuit = self._get_source_circuit(output)
        source_circuit['source_type'] = handler_type
        self._update_input_circuit(source_circuit, input_a, 'input_a')
        if input_b is not None:
            self._update_input_circuit(source_circuit, input_b, 'input_b')

    def _handle_instruction(self, instruction):
        """Parses values from the instruction and initializes circuit wires

        Args:
            instruction (str): One of the puzzle instructions
        Returns: None
        """
        for circuit_type, pattern in self._instructions.items():
            parsed_type = pattern.match(instruction)
            if parsed_type is None:
                continue
            if circuit_type == 'SIGNAL_WIRE' or circuit_type == 'NOT_GATE':
                signal, wire = parsed_type.groups()
                self._input_handler(wire, circuit_type, signal)
                if circuit_type == 'SIGNAL_WIRE':
                    wire_signal = self._get_source_circuit(signal)['signal']
                    if wire_signal is not None:
                        self._wire_tracker[wire]['signal'] = wire_signal
                break
            if (circuit_type == 'AND_GATE' or circuit_type == 'OR_GATE'
                    or circuit_type == 'LEFT_SHIFT'
                    or circuit_type == 'RIGHT_SHIFT'):
                input_a, input_b, output = parsed_type.groups()
                self._input_handler(output, circuit_type, input_a, input_b)
                break

    def _get_circuit_sets(self):
        """Parses wire IDs for circuits with and without signal into two sets

        Args: None
        Returns:
            tuple: A pair of sets holding circuits with a signal to propagate
        """
        signaling_circuits = set()
        nonsignaling_circuits = set(self._wire_tracker.keys())
        for wire_id in sorted(nonsignaling_circuits):
            if self._wire_tracker[wire_id]['signal'] is None:
                continue
            signaling_circuits.add(wire_id)
        nonsignaling_circuits.difference_update(signaling_circuits)
        return (nonsignaling_circuits, signaling_circuits)

    @staticmethod
    def _get_circuit_signal(circuit_type, input_a, input_b):
        """Calculates the signal assuming inputs are valid for the circuit type

        Args:
            circuit_type (str): Specifies the logic circuit or instruction
            input_a (int): The ID or source signal of one of the circuit inputs
            input_b (int): The ID or source signal of one of the circuit inputs
        Returns:
            int: The signal output from the circuit or None
        """
        bit_mask = 0xFFFF
        if circuit_type == 'SIGNAL_WIRE':
            circuit_signal = input_a & bit_mask
        elif circuit_type == 'NOT_GATE':
            circuit_signal = ~input_a & bit_mask
        elif input_b is not None:
            if circuit_type == 'AND_GATE':
                circuit_signal = (input_a & input_b) & bit_mask
            elif circuit_type == 'OR_GATE':
                circuit_signal = (input_a | input_b) & bit_mask
            elif circuit_type == 'LEFT_SHIFT':
                circuit_signal = (input_a << input_b) & bit_mask
            elif circuit_type == 'RIGHT_SHIFT':
                circuit_signal = (input_a >> input_b) & bit_mask
        else:
            circuit_signal = None
        return circuit_signal

    def _propagate_signals(self):
        """Pushes circuit signals through the wire network for all circuits

        Args: None
        Returns: None
        """
        nonsignaling_circuits, signaling_circuits = self._get_circuit_sets()

        while signaling_circuits:
            for wire_id in sorted(signaling_circuits):
                circuit = self._wire_tracker[wire_id]
                circuit_type = circuit['source_type']
                input_a = circuit['input_a']['signal']
                input_b = None
                if circuit['input_b']:
                    input_b = circuit['input_b']['signal']

                new_signal = self._get_circuit_signal(
                    circuit_type,
                    input_a,
                    input_b,
                )
                if new_signal is not None:
                    circuit['signal'] = new_signal
                    for output_wire_id in circuit['outputs']:
                        signaling_circuits.add(output_wire_id)
                else:
                    nonsignaling_circuits.add(wire_id)
                signaling_circuits.remove(wire_id)
            nonsignaling_circuits -= signaling_circuits

    def _parse_instructions(self):
        """Parses each instruction in the puzzle input to initialize the wires

        Args: None
        Returns: None
        """
        self._wire_tracker = {}
        for instruction in self._puzzle_input.splitlines():
            if instruction:
                self._handle_instruction(instruction)

    def _solve_puzzle_parts(self):
        """Solves each part of a Advent of Code 2015 puzzle

        Args: None
        Returns:
            tuple: Pair of solutions for the two parts of the puzzle
        """
        # Part 1 of Day 7
        self._parse_instructions()
        self._propagate_signals()
        wire_b_override = self._wire_tracker['a']['signal']

        # Part 2 of Day 7
        self._parse_instructions()
        if 'b' in self._wire_tracker:  # Some tests do not have a b wire
            self._wire_tracker['b']['input_a']['signal'] = wire_b_override
        self._propagate_signals()

        return (wire_b_override, self._wire_tracker['a']['signal'])

    def run_test_cases(self):
        """Runs a series of inputs and compares against expected outputs

        Args: None
        Returns: None
        """
        input1 = '123 -> a'
        input2 = '\n'.join((input1, '321 -> a'))
        input3 = '\n'.join(('123 -> b', '456 -> c', 'b AND c -> a'))
        input4 = '\n'.join(('123 -> b', '456 -> c', 'b OR c -> a'))
        input5 = '\n'.join(('123 -> b', 'NOT b -> a'))
        input6 = '\n'.join(('123 -> b', 'b LSHIFT 2 -> a'))
        input7 = '\n'.join(('123 -> b', 'b RSHIFT 2 -> a'))
        self._run_test_case(solver.TestCase(input1, 123, 123))
        self._run_test_case(solver.TestCase(input2, 321, 321))
        self._run_test_case(solver.TestCase(input3, 72, 72))
        self._run_test_case(solver.TestCase(input4, 507, 507))
        self._run_test_case(solver.TestCase(input5, 65412, 123))
        self._run_test_case(solver.TestCase(input6, 492, 1968))
        self._run_test_case(solver.TestCase(input7, 30, 7))
