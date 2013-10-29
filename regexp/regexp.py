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

    def match(self, expr, retries=5):
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
        return self._start_state

    @start_state.setter
    def start_state(self, value):
        self._start_state = value

    @property
    def final_states(self):
        return self._final_states

    @final_states.setter
    def final_states(self, value):
        self._final_states = value

    def add_final_state(self, state):
        self._final_states.append(state)


class RegularExpression(object):

    def __init__(self, pattern):
        self._start_state = None
        self.build_machine(pattern)

    def match(self, expr):
        return self._start_state.match(expr)

    def build_machine(self, pattern):
        # Setup
        start_state = State(final=False)
        current_state = start_state
        current_machine = Automaton()
        current_machine.start_state = start_state
        last_complete_machine = None

        # Begin parsing the string
        for c in pattern:

            # If it's a left paren, we know we're starting a new sub-automaton
            if c == '(':
                new_machine = Automaton()
                new_machine.start_state = current_state
                current_machine = new_machine

            # If it's a right paren, we know we're completing the most recent sub-automaton
            elif c == ')':
                last_complete_machine = current_machine

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
                new_machine = Automaton()
                new_state = State(final=False)
                new_machine.start_state = State(final=False)
                new_machine.start_state.add_transition('e', last_complete_machine.start_state)
                if start_state == last_complete_machine.start_state:
                    start_state = new_machine.start_state

                # TODO: Determine a way to redirect all states pointing
                # at the old start state to the new start state
                new_machine.start_state.add_transition('e', new_state)
                for fs in last_complete_machine.final_states:
                    new_machine.final_states.append(fs)
                current_state = new_state
                current_machine = new_machine

            # If it's a character, we need to make an atomic (and complete) submachine and
            # append it to the most recent state
            elif c in ['a', 'b', 'e']:
                new_machine = Automaton()
                join_state = State(final=False)

                # Point all previous final states at the newest read character
                if last_complete_machine is not None:
                    for fs in last_complete_machine.final_states:
                        fs.add_transition('e', join_state)
                        fs.final = False
                else:
                    current_state.add_transition('e', join_state)
                    current_state.final = False

                new_machine.start_state = join_state
                new_state = State(final=True)
                join_state.add_transition(c, new_state)

                if current_state in current_machine.final_states:
                    current_machine.final_states.remove(current_state)

                current_machine.final_states.append(new_state)
                new_machine.final_states = [new_state]
                current_state = new_state
                last_complete_machine = new_machine

            # Ignore any other kind of character
            else:
                pass

        self._start_state = start_state