from . import Lexer
from . import Tokens


def imp_lex(characters):
    lx = Lexer.Lexer()
    return lx.lex(characters, Tokens.token_exprs)
