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

    def test_regexp(self):
        pattern1 = "(a|b)*a"
        pattern2 = "((a|b)(a|b))*"
        pattern3 = "aaa*b*a*a"

        regexp1 = RegularExpression(pattern1)
        regexp2 = RegularExpression(pattern2)
        regexp3 = RegularExpression(pattern3)

        self.assertTrue(regexp1.match("aaaa"))
        self.assertTrue(regexp1.match("aba"))
        self.assertTrue(regexp1.match("bba"))
        self.assertTrue(regexp1.match("a"))
        self.assertFalse(regexp1.match("b"))
        self.assertFalse(regexp1.match("bbb"))

        self.assertTrue(regexp2.match("abbabb"))
        self.assertTrue(regexp2.match("e"))
        self.assertTrue(regexp2.match("aa"))
        self.assertTrue(regexp2.match("ab"))
        self.assertFalse(regexp2.match("aaaaa"))
        self.assertFalse(regexp2.match("bba"))

        self.assertTrue(regexp3.match("aabaa"))
        self.assertTrue(regexp3.match("aaa"))
        self.assertTrue(regexp3.match("aabba"))
        self.assertFalse(regexp3.match("abbaa"))
        self.assertFalse(regexp3.match("abbbbbbbbbbbbbbbbbbba"))
        self.assertFalse(regexp3.match("bbaa"))


if __name__ == '__main__':
    unittest.main()