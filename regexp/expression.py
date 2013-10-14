class Expression(object):
    """
    A class representing a single expression within a regular expression.
    """

    def __init__(self):
        self.accepting_expressions = []
        self.characters = []
        self.subexpressions = []
        self.parent = None
        self.match_type = MatchType.Once

    def add_accepting_expression(self, exp):
        self.accepting_expressions.append(exp)

    def add_character(self, c):
        self.characters.append(c)

    def add_subexpression(self, exp):
        exp.parent = self
        self.subexpressions.append(exp)

    @property
    def current_subexpression(self):
        return self.subexpressions[self.subexpressions.count() - 1]

    @property
    def current_character(self):
        return self.characters[self.characters.count() - 1]

    @property
    def current_accepting_expression(self):
        return self.accepting_expressions[self.accepting_expressions.count() - 1]

    def set_match_type(self, match_type):
        self.match_type = match_type


class MatchType(object):
    """
    An enumeration type for the different types of expression matches.
    """

    Once, ZeroToMany = range(2)


class RegularExpression(object):
    """
    A utility class that will parse strings into a regular expression
    and compare other strings to that expression.
    """

    def __init__(self):
        pass

    def parse(self, expr):
        pass

    def compare(self, expr):
        pass