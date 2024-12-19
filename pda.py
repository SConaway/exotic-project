import utils


class PDA:
    def __init__(
        self,
        transitions: dict,
        initial_state: str,
        final_states: list[str],
        reject_states: list[str],
    ):
        """
        Initialize the PDA with transitions, initial state, final, and reject states.
        """
        self.transitions = transitions
        self.current_state = initial_state
        self.stack = []
        self.final_states = set(final_states)
        self.reject_states = set(reject_states)
        self.last_consumed_char = None

    def is_reversible(self):
        """
        Verify if the PDA is reversible.
        Returns True if reversible, False otherwise.
        """
        return utils.validate_transitions(self.transitions)

    def _has_epsilon_transitions(self, direction):
        """
        Check if there are epsilon transitions available for the current state.
        """
        if direction not in self.transitions:
            return False

        state_transitions = self.transitions[direction].get(self.current_state, {})
        for (input_char, _), _ in state_transitions.items():
            if input_char == "":  # Epsilon transition
                return True

        return False

    def simulate(self, input_string, direction):
        """
        Simulate the PDA for a given input string and direction ('f' or 'b').
        Returns the final state, stack content, and True if the simulation ends in an accept state and False if not.
        """
        input_index = 0

        while input_index < len(input_string) or self._has_epsilon_transitions(
            direction
        ):
            # Get the current input character or epsilon
            char = input_string[input_index] if input_index < len(input_string) else ""

            # Try to make a step
            proceed = self.step(char, direction)

            if not proceed:  # If no valid transition exists
                return self.current_state, self.stack, False

            # Advance the input index only if the transition consumed the input character
            if char != "" and char == self.last_consumed_char:
                input_index += 1

        # Check if the current state is an accept state
        return self.current_state, self.stack, (self.current_state in self.final_states)

    def step(self, char, direction):
        """
        Perform a single transition based on the current state, input character,
        and direction ('f' or 'b').
        Returns True if the step is successful, False otherwise.
        """
        # print(
        #     f"char: {char}, direction: {direction}, current_state: {self.current_state}, stack: {self.stack}"
        # )
        if direction not in self.transitions:
            return False

        state_transitions = self.transitions[direction].get(self.current_state, {})

        for (input_char, stack_char), (
            next_state,
            stack_change,
        ) in state_transitions.items():
            # Match input character and stack top
            if (input_char == char or input_char == "") and (
                (self.stack and stack_char == self.stack[-1]) or not stack_char
            ):
                # Update stack

                ## only pop if stack_char is not epsilon or if stack is not empty
                if stack_char and self.stack and self.stack[-1] == stack_char:
                    self.stack.pop()
                ## only push if stack_change is not epsilon
                if stack_change:
                    self.stack.extend(reversed(stack_change))

                # Update state
                self.current_state = next_state

                # Track whether input was consumed
                # this is then used by simulate to determine whether to advance the input index
                # as an epsilon transition does not consume input but still advances the state
                self.last_consumed_char = input_char

                return True

        # No valid transition found so
        return False
