import unittest
from regexp import *


class RegexpTest(unittest.TestCase):

    def setUp(self):
        self.u = State(False)
        self.v = State(False)
        self.w = State(True)
        self.u.add_transition('a', self.v)
        self.v.add_transition('b', self.w)
        self.v.add_transition('a', self.u)
        self.u.add_transition('b', self.w)
        self.w.add_transition('b', self.w)
        self.w.add_transition('a', self.u)

        self.machine = Automaton()
        self.machine.start_state = self.u
        self.machine.final_states = [self.w]

    def tearDown(self):
        del self.u
        del self.v
        del self.w

    def test_node_add_transition(self):
        self.assertEqual(self.u.transitions['a'], [self.v])
        self.assertEqual(self.u.transitions['b'], [self.w])

    def test_node_matching(self):
        expr = "abbbbbbbbb"
        self.assertEqual(self.u.match(expr), True)

        expr = "a"
        self.assertEqual(self.u.match(expr), False)

        expr = "b"
        self.assertEqual(self.u.match(expr), True)

        expr = "abbbbbbbbbba"
        self.assertEqual(self.u.match(expr), False)

        expr = "abbbbababab"
        self.assertEqual(self.u.match(expr), True)

    def test_automaton_setup(self):
        self.assertEqual(self.machine.start_state, self.u)
        self.assertEqual(self.machine.final_states, [self.w])

    def test_automaton_matching(self):
        expr = "abbbbbbbbb"
        self.assertEqual(self.machine.match(expr), True)

        expr = "a"
        self.assertEqual(self.machine.match(expr), False)

        expr = "b"
        self.assertEqual(self.machine.match(expr), True)

        expr = "abbbbbbbbbba"
        self.assertEqual(self.machine.match(expr), False)

        expr = "abbbbababab"
        self.assertEqual(self.machine.match(expr), True)


if __name__ == '__main__':
    unittest.main()