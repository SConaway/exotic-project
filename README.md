# Exotic Project

## Reversible PDA Validator and Simulator

By Steven Conaway and Anna Teerlinck

Our Research Project for CSE 40932: Exotic Computing is a Reversible PDA Validator and Simulator.

---

## Usage

Our program, written in Python, operates on the following input:

```sh
$ python3 rePDAsim.py machine.pda 0101 f
#                     [1]         [2]  [3]
```

1. machine specification file, contains the transition information:

```csv
fromState, direction, inputChar, stackChar, toState, stackChange
q0,f,0,1,q1,ep
```

> [!WARNING]
> make an actual example

<!-- this should render nicely but idk if it will (thanks internet) -->

2. input string

   the string on which the PDA operates.

3. Direction:

   the direction either will be specified as `f` or `b`.

> [!WARNING]
> Need to figure out some plan for interactivity.

---

## Automaton Description

For our project, a "Bidirectional Pushdown Automata" (BPDA) is defined as an extension of the reversible DFA (BFA) to include a stack. It includes the following properties:

1. **Control Input**: The BPDA, like the BFA, has a second "control" input from the alphabet $\beta = \{f, b\}$, where $f$ stands for "forwards" and $b$ for "backwards". This control input determines the direction of tape head movement and affects the transitions.

2. **Tape Operations**:

   - When the control input is $f$ (forward), the BPDA reads the current character under the tape head, processes the state and stack, and moves the tape head one position to the right.
   - When the control input is $b$ (backward), the BPDA first moves the tape head one position to the left, reads the tape, processes the state and stack, and leaves the tape head in place after updating the state.

3. **Stack Operations**:

   - Like a traditional PDA, the BPDA maintains a stack on which it can perform push, pop, and no-op operations.
   - Transitions are determined by the current state, the current character on the tape, the stack's top symbol, and the control input (direction).

4. **Transition Function**:

   - The transition function $\delta$ is defined as: $\delta: Q \times \Sigma \times \Gamma \times \beta \to Q \times \Gamma^*$
     Here:
     - $Q$ is the set of states.
     - $\Sigma$ is the tape alphabet.
     - $\Gamma$ is the stack alphabet.
     - $\beta = \{f, b\}$ is the control alphabet.
     - $\Gamma^*$ represents the stack symbol resulting from the transition.

5. **Reversibility**:

   - The BPDA must be reversible, meaning every transition has a unique inverse. Specifically:
     - For every $\delta(q, a, Z, c) = (q', \gamma, d)$ (where $q$ is the current state, $a$ the tape character, $Z$ the stack's top, $c$ the control input, and $\gamma$ the new stack string), there exists a corresponding transition $\delta^{-1}(q', a', \gamma', c') = (q, Z, d')$ such that the automaton can backtrack.

6. **Acceptance**:

   - The BPDA accepts an input string if it reaches a designated accepting state.

7. **State Diagrams**:
   - State transitions are labeled with triplets of the form $x:a, Z \to \gamma$, where $x$ is the control direction, $a$ is the tape character, $Z$ is the current stack's top symbol, and $\gamma$ is the resulting stack string after the transition.
