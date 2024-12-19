import csv


def parse_transitions(file_contents: str):
    """
    Parse the PDA transition file into a nested dictionary.

    Returns:
        dict: The parsed transitions ("direction" > "state" > ("inputChar", "stackChar") > ("toState", "stackChange"))

    >>> parse_transitions('''direction,fromState,inputChar,stackChar,toState,stackChange
    ... f,q0,0,1,q1,ep
    ... f,q0,1,1,q1,ep
    ... f,q1,0,1,qacc,ep
    ... ''')
    {'f': {'q0': {('0', '1'): ('q1', ''), ('1', '1'): ('q1', '')}, 'q1': {('0', '1'): ('qacc', '')}}, 'b': {}}
    """
    # Initialize the transitions dictionary
    transitions: dict[str, dict[str, dict[tuple[str, str], tuple[str, str]]]] = {
        "f": {},
        "b": {},
    }

    # Read the CSV contents
    reader = csv.DictReader(file_contents.strip().splitlines())
    for row in reader:
        # Extract and validate the values
        from_state = row.get("fromState", "").strip()
        direction = row.get("direction", "").strip()
        input_char = row.get("inputChar", "").strip()
        stack_char = row.get("stackChar", "").strip()
        to_state = row.get("toState", "").strip()
        stack_change = row.get("stackChange", "").strip()

        if not from_state or not to_state:
            raise ValueError(
                f"Invalid states: fromState='{from_state}', toState='{to_state}'"
            )
        if direction not in {"f", "b"}:
            raise ValueError(f"Invalid direction: {direction}")
        if input_char != "ep" and len(input_char) != 1:
            raise ValueError(f"Invalid inputChar: {input_char}")
        if stack_char != "ep" and len(stack_char) != 1:
            raise ValueError(f"Invalid stackChar: {stack_char}")
        if stack_change != "ep" and len(stack_change) != 1:
            raise ValueError(f"Invalid stackChange: {stack_change}")

        # Normalize epsilon values
        input_char = input_char if input_char != "ep" else ""
        stack_char = stack_char if stack_char != "ep" else ""
        stack_change = stack_change if stack_change != "ep" else ""

        # Create the key and value for the transition
        key = (input_char, stack_char)
        value = (to_state, stack_change)

        # Add the transition, grouping by state
        if from_state not in transitions[direction]:
            transitions[direction][from_state] = {}
        transitions[direction][from_state][key] = value

    return transitions


def validate(transitions, initial_state, final_states, reject_states):
    """
    Validate the PDA configuration.

    Args:
        transitions (dict): The PDA transitions.
        initial_state (str): The initial state of the PDA (needed to know where to start/stop)
        final_states (list[str]): The final (accepting) states of the PDA (where to stop/start)
        reject_states (list[str]): The rejecting states of the PDA

    Returns:
        bool: True if the PDA configuration is valid, False otherwise.

    Raises:
        ValueError: If any configuration error is found.

    >>> transitions = {
    ...     "f": {
    ...         "q0": {("a", ""): ("q1", "X")},
    ...         "q1": {("b", "X"): ("q2", "")},
    ...     },
    ...     "b": {
    ...         "q1": {("a", "X"): ("q0", "")},
    ...         "q2": {("b", ""): ("q1", "X")},
    ...     },
    ... }
    >>> initial_state = "q0"
    >>> final_states = ["q2"]
    >>> reject_states = []
    >>> validate(transitions, initial_state, final_states, reject_states)
    True

    >>> transitions = {
    ...     "f": {
    ...         "q0": {("a", ""): ("q1", "X")},
    ...         "q1": {("b", "X"): ("q2", "")},
    ...     },
    ...     "b": {
    ...         "q2": {("b", ""): ("q1", "X")},
    ...     },
    ... }
    >>> initial_state = "q0"
    >>> final_states = ["q2"]
    >>> reject_states = []
    >>> validate(transitions, initial_state, final_states, reject_states)
    Traceback (most recent call last):
        ...
    ValueError: Missing reverse transition for forward transition: 'q0' => 'q1' on input 'a' with stack ''.

    >>> transitions = {
    ...     "f": {
    ...         "q0": {("a", ""): ("q1", "X")},
    ...         "q1": {("b", "X"): ("q2", "")},
    ...     },
    ...     "b": {
    ...         "q1": {("a", "X"): ("q0", "")},
    ...         "q2": {("b", ""): ("q1", "X")},
    ...     },
    ... }
    >>> initial_state = "q3"
    >>> final_states = ["q2"]
    >>> reject_states = []
    >>> validate(transitions, initial_state, final_states, reject_states)
    Traceback (most recent call last):
        ...
    ValueError: Initial state 'q3' is not defined in transitions.

    >>> transitions = {
    ...     "f": {
    ...         "q0": {("a", ""): ("q1", "X")},
    ...     },
    ...     "b": {},
    ... }
    >>> initial_state = "q0"
    >>> final_states = ["q2"]
    >>> reject_states = []
    >>> validate(transitions, initial_state, final_states, reject_states)
    Traceback (most recent call last):
        ...
    ValueError: Final state 'q2' is not defined in transitions.

    >>> transitions = {
    ...     "f": {
    ...         "q0": {("a", ""): ("q1", "X")},
    ...     },
    ...     "b": {
    ...         "q1": {("a", "X"): ("q0", "")},
    ...     },
    ... }
    >>> initial_state = "q0"
    >>> final_states = ["q1"]
    >>> reject_states = ["q2"]
    >>> validate(transitions, initial_state, final_states, reject_states)
    Traceback (most recent call last):
        ...
    ValueError: Reject state 'q2' is not defined in transitions.

    >>> transitions = {
    ...     "f": {
    ...         "q0": {("a", ""): ("q1", "X")},
    ...         "q1": {("a", ""): ("q1", "X"), ("", ""): ("q2", "")},
    ...     },
    ...     "b": {
    ...         "q1": {("a", ""): ("q0", "")},
    ...     },
    ... }
    >>> initial_state = "q0"
    >>> final_states = ["q1"]
    >>> reject_states = []
    >>> validate(transitions, initial_state, final_states, reject_states)
    Traceback (most recent call last):
        ...
    ValueError: Missing reverse transition for forward transition: 'q0' => 'q1' on input 'a' with stack ''.
    """
    # Collect all states from transitions
    states = set()
    for direction, dir_transitions in transitions.items():
        for from_state, transitions_for_state in dir_transitions.items():
            states.add(from_state)
            for (_, _), (to_state, _) in transitions_for_state.items():
                states.add(to_state)

    # Check that the initial state exists
    if initial_state not in states:
        raise ValueError(
            f"Initial state '{initial_state}' is not defined in transitions."
        )

    # Check that at least one final state exists (but not necessarily all)
    has_final_state = False
    for state in final_states:
        if state in states:
            has_final_state = True
            break
    if not has_final_state:
        raise ValueError(f"No final states defined in transitions ({final_states}).")

    # skip check for reject as it can be implicit

    # Check for ambiguous transitions in deterministic directions
    for direction, dir_transitions in transitions.items():
        for state, transitions_for_state in dir_transitions.items():
            seen_conditions = set()
            for input_char, stack_char in transitions_for_state.keys():
                if (input_char, stack_char) in seen_conditions:
                    raise ValueError(
                        f"Ambiguous transitions detected in state '{state}' "
                        f"for input '{input_char}' and stack '{stack_char}' in direction '{direction}'."
                    )
                seen_conditions.add((input_char, stack_char))

    # Check reversibility
    for forward_state, forward_transitions in transitions["f"].items():
        for (input_char, stack_char), (
            to_state,
            stack_change,
        ) in forward_transitions.items():
            # Locate the reverse transition
            reverse_transitions = transitions["b"].get(to_state, {})
            reverse_found = False
            for (rev_input_char, rev_stack_char), (
                rev_to_state,
                rev_stack_change,
            ) in reverse_transitions.items():
                if (
                    rev_to_state == forward_state
                    and rev_stack_change == stack_char
                    and rev_stack_char == stack_change
                    and rev_input_char == input_char
                ):
                    reverse_found = True
                    break

            if not reverse_found:
                raise ValueError(
                    f"Missing reverse transition for forward transition: "
                    f"'{forward_state}' => '{to_state}' on input '{input_char}' with forward stack change '{stack_char}'."
                )

    return True
