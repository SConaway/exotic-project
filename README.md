# Exotic Project

## Reversible PDA Validator and Simulator

**By Steven Conaway and Anna Teerlinck**

This project is a Reversible PDA Validator and Simulator developed as part of **CSE 40932: Exotic Computing**.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Usage](#usage)
   - [Input File](#input-file)
   - [Input String](#input-string)
   - [Direction](#direction)
3. [Formal Automaton Description](#formal-automaton-description)
4. [Examples](#examples)

---

## Introduction

This project explores a Reversible Pushdown Automaton (R-PDA), a computational model combining a stack-based automaton with reversibility. The validator checks for machine reversibility, while the simulator executes both forward and backward simulations of a PDA.

---

## Usage

Run the program using:

```sh
$ python3 rePDAsim.py machine.pda [input_string direction (f|b)]
```

### Parameters

1. **`machine.pda`** (required): A file containing the PDA transitions in CSV format.

   - Example:
     ```csv
     direction,fromState,inputChar,stackChar,toState,stackChange
     f,q0,ep,ep,q1,$
     f,q1,(,ep,q1,(
     f,q1,),(,q1,ep
     f,q1,ep,$,qacc,ep
     ```
     - `ep` represents an empty string ($\epsilon$ in formal notation).

2. **`input_string`** (optional): The string for the PDA to process.

   - If omitted, the program will run in interactive mode

3. **`direction`** (optional): Specifies the simulation direction.
   - `f` for forward, `b` for backward.

---

### Examples

#### Automated Mode

Run the simulator with an input string and direction:

```sh
$ python3 rePDAsim.py examples/counting.pda "(()())" f
Missing reverse transition for forward transition: 'q0' => 'q1' on input '' with stack ''.
current_state: q0, char: (, direction: f, stack: []
current_state: q1, char: (, direction: f, stack: ['$']
current_state: q1, char: (, direction: f, stack: ['$', '(']
current_state: q1, char: ), direction: f, stack: ['$', '(', '(']
current_state: q1, char: (, direction: f, stack: ['$', '(']
current_state: q1, char: ), direction: f, stack: ['$', '(', '(']
current_state: q1, char: ), direction: f, stack: ['$', '(']
current_state: q1, char: , direction: f, stack: ['$']
Simulation results:
	Final state: qacc
	Stack content: []
	Accept state reached: True
```

#### Interactive Mode

Run the validator without simulating:

```
$ python3 rePDAsim.py examples/counting.pda
Missing reverse transition for forward transition: 'q0' => 'q1' on input '' with stack ''.
Enter characters and direction {'f' or 'b'} (e.g., '0f', '1b').
Type 'exit' to quit.
Input: (f
current_state: q0, char: (, direction: f, stack: []
State: q1, Stack: ['$'], input not consumed
Input: (f
current_state: q1, char: (, direction: f, stack: ['$']
State: q1, Stack: ['$', '(']
Input: (f
current_state: q1, char: (, direction: f, stack: ['$', '(']
State: q1, Stack: ['$', '(', '(']
Input: )f
current_state: q1, char: ), direction: f, stack: ['$', '(', '(']
State: q1, Stack: ['$', '(']
Input: (f
current_state: q1, char: (, direction: f, stack: ['$', '(']
State: q1, Stack: ['$', '(', '(']
Input: )f
current_state: q1, char: ), direction: f, stack: ['$', '(', '(']
State: q1, Stack: ['$', '(']
Input: )f
current_state: q1, char: ), direction: f, stack: ['$', '(']
State: q1, Stack: ['$']
Input:
assuming no input character, forward
current_state: q1, char: , direction: f, stack: ['$']
State: qacc, Stack: []
Accept state reached.
```

---

## Formal Automaton Description

A Bidirectional Pushdown Automaton (BPDA) extends a PDA to support reversible computations. Key features include:

1. **Control Input**:

   - Control symbols $f$ and $b$ specify forward and backward directions, respectively.

2. **Stack Operations**:

   - Operations include push, pop, and no-op, defined for each transition.

3. **Transition Function**:

   - $\delta: Q \times \Sigma \times \Gamma \times \beta \to Q \times \Gamma^*$
   - Example:
     - Forward: $\delta(q_0, a, Z, f) = (q_1, \gamma)$
     - Reverse: $\delta^{-1}(q_1, a, \gamma, b) = (q_0, Z)$

4. **Reversibility**:
   - For every forward transition, there exists an inverse transition. Specifically, for every $\delta(q, a, Z, c) = (q', \gamma, d)$ (where $q$ is the current state, $a$ the tape character, $Z$ the stack's top, $c$ the control input, and $\gamma$ the new stack string), there exists a corresponding transition $\delta^{-1}(q', a', \gamma', c') = (q, Z, d')$ such that the automaton can backtrack.

---

## Notes

- The `ep` symbol:
  - Represents "no character" (input character or top of stack) or "no stack change."
  - Used for empty string transitions and no-op stack changes.
- **Non-reversible simulation**:
  - Machines do not need to be reversible to simulate them. However, the reversibility check will fail for such machines.
- **Limitations**:
  - A stack or input character which is a space character will be treated as an empty string.
