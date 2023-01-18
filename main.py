
from random import randint


from parse import Parser

# TESTS
parsing = Parser()

f = open("tests.jl","r")
ctnt = f.read()
f.close()

parsing.parse(ctnt)
parsing.ctx.print()