class Expression(object):
    def __init__(self):
        self.subexpressions = []
        self.characters = []
        self.parent = None
        self.match_type = MatchType.Once

    def add_subexpression(self, exp):
        exp.parent = self
        self.subexpressions.append(exp)

    def add_character(self, c):
        self.characters.append(c)

    def set_match_type(self, match_type):
        self.match_type = match_type


class MatchType(object):
    Once, ZeroToMany = range(2)