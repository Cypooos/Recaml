from core.errors import RecamlError
from core.parse import Parser

parsing = Parser()


f = open("tests/parser.jl","r")
ctnt = f.read()
f.close()

try:
  parsing.parse(ctnt)
except RecamlError as e:
  print(e)

else:
  parsing.ctx.print_keys("Tests")