from core.errors import RecamlError
from core.parse import Parser
import glob 

parsing = Parser()


if __name__ == "__main__":
  for test in glob.glob("./tests/*"):
    f = open(test,"r")
    ctnt = f.read()
    f.close()

    try:
      parsing.parse(ctnt)
    except RecamlError as e:
      print(e)
      exit()
    else:
      print("TEST `"+test+"` COMPLETED")
  parsing.ctx.print_keys("Tests")