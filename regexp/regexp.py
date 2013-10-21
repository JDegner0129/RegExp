class State(object):

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

    def match(self, expr):
        """
        Determines if this state can match the expression provided.
        @param expr: A series of characters in the alphabet {a,b,e}
        @return: True if this state can match the expression, else False.
        """
        if len(expr) == 0:
            return self._final
        else:
            key = expr[0]
            if key in self._transitions:
                for state in self._transitions[key]:
                    if len(expr) > 1:
                        if state.match(expr[1:]):
                            return True
                    else:
                        return state.final
            return False


class Automaton(object):

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

    def add_start_state(self, state):
        self._start_states.append(state)

    def add_final_state(self, state):
        self._final_states.append(state)

    def match(self, expr):
        if len(expr) == 0:
            return self._start_state.final
        else:
            return self._start_state.match(expr)