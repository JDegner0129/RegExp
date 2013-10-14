import unittest
from expression import *


class RegularExpressionTest(unittest.TestCase):

    def test_expression(self):
        test_exp = Expression()

        print 'Testing character addition...'

        print 'characters == []?'
        self.assertEqual(test_exp.characters, [])

        print 'Adding "a" to character list...'
        test_exp.add_character('a')

        print 'characters == [a]?'
        self.assertEqual(test_exp.characters, ['a'])

        print 'Testing change of match type...'

        print 'match_type == Once?'
        self.assertEqual(test_exp.match_type, MatchType.Once)

        print 'Changing match type...'
        test_exp.set_match_type(MatchType.ZeroToMany)

        print 'match_type == ZeroToMany?'
        self.assertEqual(test_exp.match_type, MatchType.ZeroToMany)

        print 'Testing sub-expression addition...'

        print 'subexpressions == []?'
        self.assertEqual(test_exp.subexpressions, [])

        print 'Adding a subexpression with "b"...'
        subexp = Expression()
        subexp.add_character('b')
        test_exp.add_subexpression(subexp)

        print 'subexpressions == [Expression("b")]?'
        self.assertEqual(test_exp.subexpressions, [subexp])

    def test_regularexpression(self):
        pass

if __name__ == '__main__':
    unittest.main()