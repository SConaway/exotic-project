import csv


def parse_transitions(file_contents: str):
    """
    Parse the PDA transition file into a nested dictionary.
    Returns:
        dict: The parsed transitions ("direction" > "fromState,inputChar,stackChar" > "toState,stackChange)"

    >>> parse_transitions('''fromState,direction,inputChar,stackChar,toState,stackChange
    ... q0,f,0,1,q1,ep
    ... q0,f,1,1,q1,ep
    ... q1,f,0,1,qacc,ep
    ... ''')
    {'f': {'q0,0,1': 'q1,ep', 'q0,1,1': 'q1,ep', 'q1,0,1': 'qacc,ep'}}
    """
    # initialize the transitions dictionary
    transitions: dict[str, dict[str, str]] = {}

    # open the file
    reader = csv.DictReader(file_contents.splitlines())
    for row in reader:
        if row == {}:
            continue
        fromState = row["fromState"]
        direction = row["direction"]
        inputChar = row["inputChar"]
        stackChar = row["stackChar"]
        toState = row["toState"]
        stackChange = row["stackChange"]

        key = f"{fromState},{inputChar},{stackChar}"
        value = f"{toState},{stackChange}"

        if direction not in transitions:
            transitions[direction] = {}

        transitions[direction][key] = value

    return transitions


def validate_transitions(transitions):
    """
    Validate the transition table for correctness.
    Returns True if valid, False otherwise.
    """
    # TODO: this
    pass
