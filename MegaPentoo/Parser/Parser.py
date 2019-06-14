from enum import Enum


class STATES(Enum):
    ASSIGNING = 0

class Parser:
    def put_token(self, token):
        pass


    def __if__(self, step):
        pass

    def analyze_tokens(self, tokens):
        expected_token = None
        state = None
        for name, tag in tokens:
            if tag != expected_token:
                raise NotExpected("Expected " + str(expected_token) + ", given " + str(tag))

            if state:
                if (state == STATES.ASSIGNING):
                    expected_token 
            else:
                if tag == TAGS.ID:
                    expected_token = TAGS.ASSIGN
                    state = STATES.ASSIGNING




class NotExpected(Exception):
    pass