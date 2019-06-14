import sys
import re


class Lexer:
    __pos__ = 0

    def lex(self, characters, token_exprs):
        tokens = []
        while self.__pos__ < len(characters):
            match = None
            for token_expr in token_exprs:
                pattern, tag = token_expr
                regex = re.compile(pattern)
                match = regex.match(characters, self.__pos__)
                if match:
                    text = match.group(0)
                    if tag:
                        token = (text, tag)
                        tokens.append(token)
                    break
            if not match:
                sys.stderr.write('Illegal character: %s\n' % characters[self.__pos__])
                sys.exit(1)
            else:
                self.__pos__ = match.end(0)
        return tokens
    pass
