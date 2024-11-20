class PDA:
    def __init__(self, transitions, initial_state, final_states, reject_states):
        """
        Initialize the PDA with transitions, initial state, final, and reject states.
        """
        self.transitions = transitions
        self.current_state = initial_state
        self.stack = []
        self.final_states = set(final_states)
        self.reject_states = set(reject_states)

    def is_reversible(self):
        """
        Verify if the PDA is reversible.
        Returns True if reversible, False otherwise.
        """
        # TODO: this
        pass

    def simulate(self, input_string, direction):
        """
        Simulate the PDA for a given input string and direction ('f' or 'b').
        Returns the final state and stack content.
        """
        # TODO: this
        pass

    def step(self, char, direction):
        """
        Perform a single transition based on the current state, input character,
        and direction ('f' or 'b').
        Returns True if the step is successful, False otherwise.
        """
        # TODO: this
        pass
