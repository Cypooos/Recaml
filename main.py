
from core.parse import Parser

# TESTS
parsing = Parser()

f = open("tests/defaults.jl","r")
ctnt = f.read()
f.close()

parsing.parse(ctnt)
parsing.ctx.print()