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


def validate_transitions(transitions):
    """
    Validate the transition table for correctness.
    Returns True if valid, False otherwise.
    """
    # TODO: this
    pass
