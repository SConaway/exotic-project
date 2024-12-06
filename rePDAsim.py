import sys

from pda import PDA
from utils import parse_transitions


def interactive_simulation(pda):
    """
    Run the PDA in interactive mode.
    Allows users to input one character at a time with direction ('f' or 'b').
    """
    print("Enter characters and direction {'f' or 'b'} (e.g., '0f', '1b').")
    print("Type 'exit' to quit.")
    while True:
        user_input = input("Input: ").strip()
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
    if len(sys.argv) < 4:
        print(
            "Usage: python3 rePDAsim.py <machine.pda> <input string> <direction (f|b)>"
        )
        return

    machine_file = sys.argv[1]
    input_string = sys.argv[2]
    direction = sys.argv[3] or None

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
    if input_string == "interactive" or direction == "interactive":
        interactive_simulation(pda)
    else:
        print("Simulation result:", pda.simulate(input_string, direction))


if __name__ == "__main__":
    main()
