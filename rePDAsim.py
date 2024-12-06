#! /usr/bin/env python3

import sys

from pda import PDA
from utils import parse_transitions


def usage(status=0):
    print("Usage: python3 rePDAsim.py <machine.pda> [input string] [direction (f|b)]")
    sys.exit(status)


def interactive_simulation(pda):
    """
    Run the PDA in interactive mode.
    Allows users to input one character at a time with direction ('f' or 'b').
    """
    print("Enter characters and direction {'f' or 'b'} (e.g., '0f', '1b').")
    print("Type 'exit' to quit.")
    while True:
        try:
            user_input = input("Input: ").strip()
        except EOFError:
            break
        if user_input == "exit":
            break
        if len(user_input) == 2 and user_input[1] in ["f", "b"]:
            char, direction = user_input
            if pda.step(char, direction):
                print(f"State: {pda.current_state}, Stack: {pda.stack}")
            else:
                print("Invalid transition.")
        else:
            print("Invalid input. Format: <char><f|b> (e.g., '0f', '1b')")


def main():
    # Parse command-line arguments
    if "-h" in sys.argv or "--help" in sys.argv:
        usage(0)
    elif not (len(sys.argv) == 2 or len(sys.argv) == 4):
        usage(1)
    elif len(sys.argv) == 3:
        print("Input string specified but no direction.")
        usage(1)

    machine_file = sys.argv[1]

    # Load transitions
    with open(machine_file) as f:
        transitions_str = f.read()
    transitions = parse_transitions(transitions_str)
    initial_state = "q0"
    final_states = ["q_accept", "qacc"]
    reject_states = ["q_reject", "qrej"]

    # Initialize PDA
    pda = PDA(transitions, initial_state, final_states, reject_states)

    if pda.is_reversible():
        print("The machine is reversible.")
    else:
        print("The machine is not reversible.")

    # Simulate or check reversibility
    if len(sys.argv) == 2:
        interactive_simulation(pda)
    if len(sys.argv) == 4:
        input_string = sys.argv[2]
        direction = sys.argv[3]
        print("Simulation result:", pda.simulate(input_string, direction))


if __name__ == "__main__":
    main()
