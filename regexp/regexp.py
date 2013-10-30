from sys import stdin


class State(object):
    """
    A class to hold information concerning individual
    states within an automaton. Rather than storing
    transition information at the automaton level,
    this class provides an interface to store
    transitions at a per-state level.
    """

    def __init__(self, final):
        self._final = final
        self._transitions = {}

    @property
    def transitions(self):
        """
        A mapping of input symbols to next states.
        """
        return self._transitions

    @transitions.setter
    def transitions(self, value):
        self._transitions = value

    @property
    def final(self):
        """
        A Boolean representing if the current state is final.
        """
        return self._final

    @final.setter
    def final(self, value):
        self._final = value

    def add_transition(self, sym, state):
        """
        Adds a path to a provided state, given the provided symbol.
        @param sym: The symbol causing a transition.
        @param state: The state to transition to.
        """
        if sym in self._transitions:
            self._transitions[sym].append(state)
        else:
            self._transitions[sym] = [state]

    def match(self, expr, retries=10):
        """
        Determines if this state can match the expression provided.
        @param expr: A series of characters in the alphabet {a,b,e}
        @return: True if this state can match the expression, else False.
        """
        if len(expr) == 0:
            if self._final:
                return True
            elif 'e' not in self._transitions or retries == 0:
                return False
            else:
                retries -= 1
                for state in self._transitions['e']:
                    if state.match(expr, retries):
                        return True
                return False
        else:
            key = expr[0]
            if key in self._transitions:
                for state in self._transitions[key]:
                    if state.match(expr[1:]):
                        return True
            if 'e' in self._transitions and retries > 0:
                retries -= 1
                for state in self._transitions['e']:
                    if state.match(expr, retries):
                        return True
            return False


class Automaton(object):
    """
    A class to hold information concerning sub-automata.
    This class is meant to be composable, resulting in a
    start state that will provide correct traversal of
    a full automaton.
    """

    def __init__(self):
        self._start_state = None
        self._final_states = []

    @property
    def start_state(self):
        """
        The start state of this automaton. Provides the basis for
        traversal of the automaton.
        """
        return self._start_state

    @start_state.setter
    def start_state(self, value):
        self._start_state = value

    @property
    def final_states(self):
        """
        The final states of this automaton. Provide a basis for
        prepending this automaton to other automata.
        """
        return self._final_states

    @final_states.setter
    def final_states(self, value):
        self._final_states = value


class RegularExpression(object):
    """
    A class to hold information concerning a regular expression,
    such as its pattern and equivalent NFA's start state. Provides an
    interface to attempt to pattern match against given expressions.
    """

    def __init__(self, pattern):
        self._start_state = None
        self.build_machine(pattern)

    def match(self, expr):
        """
        Determines if this regular expression can match the
        expression provided by performing a match from this
        expression's equivalent NFA start state.
        """
        return self._start_state.match(expr)

    def build_machine(self, pattern):
        """
        Builds a non-deterministic automaton that is equivalent
        to the provided pattern. Pattern must be fewer than 80
        characters and composed of (, ), |, *, a, b, e.
        """

        # Local variables
        unioning = False
        prev_proc_char = None

        # Machine-related variables
        start_state = State(final=False)
        current_state = start_state
        current_machine = Automaton()
        current_machine.start_state = start_state
        last_complete_machine = None
        machines_in_progress = []

        # Begin parsing the string
        for c in pattern:

            # If it's a left paren, we know we're starting a new sub-automaton
            if c == '(':
                new_machine = Automaton()
                new_machine.start_state = current_state
                current_machine = new_machine
                machines_in_progress.append(new_machine)

            # If it's a right paren, we know we're completing the most recent sub-automaton
            elif c == ')':
                popped_machine = machines_in_progress.pop()

                # If the previously processed character was also a right paren, the last
                # complete machine's final states are also this one's
                if prev_proc_char == ')':
                    popped_machine.final_states = last_complete_machine.final_states

                last_complete_machine = popped_machine

            # If it's a star, we need to allow the last completed machine to recurse
            elif c == '*':
                new_state = State(final=True)
                for fs in last_complete_machine.final_states:
                    fs.final = False
                    fs.add_transition('e', new_state)

                new_state.add_transition('e', last_complete_machine.start_state)
                last_complete_machine.start_state.add_transition('e', new_state)
                last_complete_machine.final_states = [new_state]
                current_state = new_state

            # If it's a union, we need to create a new machine that allows traversal to the
            # last completed machine, and the next machine
            elif c == '|':
                new_state = State(final=False)
                intermediate_state = State(final=False)

                # Make it so this intermediate state is equivalent to the start state
                # of the last completed machine
                intermediate_state.transitions = last_complete_machine.start_state.transitions
                intermediate_state.final = last_complete_machine.start_state.final

                # Redesign the last complete machine's start state to point at this intermediate
                # state and a new start state
                last_complete_machine.start_state.transitions = {
                    'e': [intermediate_state, new_state]
                }

                # Set the current machine's start state to the last complete machine's now-augmented
                # start state
                current_machine.start_state = last_complete_machine.start_state

                # Add any remaining final states to the current machine
                for fs in last_complete_machine.final_states:
                    if fs not in current_machine.final_states:
                        current_machine.final_states.append(fs)

                #
                current_state = new_state
                unioning = True

            # If it's a character, we need to make an atomic (and complete) submachine and
            # append it to the most machine
            elif c in ['a', 'b', 'e']:
                new_machine = Automaton()
                join_state = State(final=False)

                # Point all previous final states at the newest state, but
                # only if we have them and we're not performing a union
                if last_complete_machine is not None and not unioning:
                    for fs in last_complete_machine.final_states:
                        fs.add_transition('e', join_state)
                        fs.final = False
                    new_machine.start_state = join_state

                # Else, we just concatenate to the current state
                else:
                    current_state.add_transition('e', join_state)
                    current_state.final = False
                    new_machine.start_state = current_state

                new_state = State(final=True)
                join_state.add_transition(c, new_state)

                if current_state in current_machine.final_states:
                    current_machine.final_states.remove(current_state)

                current_machine.final_states.append(new_state)
                new_machine.final_states = [new_state]

                # Update the current state and record this machine as the
                # last completed one
                current_state = new_state
                last_complete_machine = new_machine

                # Always reset the union state
                unioning = False

            prev_proc_char = c

        self._start_state = start_state

if __name__ == "__main__":
    pattern = None
    expressions = []

    # Parse a pattern and expression list from stdin
    for line in stdin:
        stripped_line = line.strip()
        if not stripped_line:
            break
        if pattern is None:
            pattern = stripped_line
        else:
            expressions.append(stripped_line)

    # For each expression, pattern match and print the results
    regexp = RegularExpression(pattern)
    for expr in expressions:
        if regexp.match(expr):
            print 'yes'
        else:
            print 'no'