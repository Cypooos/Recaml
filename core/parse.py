from core.errors import *
from core.context import Context
from core.interpretor import Interpretor
from core.utils import find_next_brackets

#  
#  nom= expression;;
#  nom= expression;;
#  emission { clé=valeur;clé=valeur;clé=valeur};
#  ________________________________________
#  
#  CHAR := [a-zA-Z0-9_@!%]*
#  LETTERS := [a-zA-Z_@!%]*
#  nom := <LETTERS><CHAR>*
#  expression := nom | \ nom ... nom ( expression ) | expression expression
#  ________________________________________

class Parser:

  STATE_CLEF = 0
  STATE_VAL = 1
  STATE_CLEF_C = 2 # if comment in STATE_CLEF
  STATE_VAL_C = 3 # if comment in STATE_VAL

  STACK_LIMIT = 30 # t_lim = 333

  def __init__(self,is_debug=False):
    self.ctx = Context()
    if is_debug: self.ctx.log_level = self.ctx.log_level | Context.LOG_DEBUG_PRINT
    self.inter = Interpretor(self.ctx,self)

  def parse(self,string):
    #self.ctx.act_path = []
    
    state = Parser.STATE_CLEF
    i = 0
    buffer = ""

    while i <len(string):
      char = string[i]

      # Exploration du path
      if state == Parser.STATE_CLEF:

        if char == ":":
          state = Parser.STATE_VAL
          self.ctx.append(buffer)
          buffer = ""
        elif char == "{":
          self.ctx.append(buffer)
          buffer = ""
        elif char == "}":
          self.ctx.back()
          buffer = ""
        elif char == "#":
          state=Parser.STATE_CLEF_C
        elif char == ";":
          if buffer.strip() != "":raise NoValueExpression("Expression is of the form `key;` instead of either `key {...};` or `key:value;`",self.ctx)
        else:
          buffer+=char
      
      elif state == Parser.STATE_CLEF_C:
        if char == "#" or char == "\n":state = Parser.STATE_CLEF

      # Création de valeurs / fonctions
      elif state == Parser.STATE_VAL:
        if char == "{": # code block in code
          place = find_next_brackets(string[i:],"{","}")
          if place != 0:
            buffer += string[i:i+place+1]
            i += place
          else:
            raise UnclosedBrackets("Unclosed block code",self.ctx)

        elif char == ";":
          state = Parser.STATE_CLEF
          self.inter.ctx.debug("[P] Creating key at `"+self.ctx.get_path()+"`")
          self.ctx.create(self.inter.evaluate(buffer+" "))

          self.inter.ctx.debug("[P] Key created.")
          self.ctx.back()
          buffer = ""
          
        elif char == "}":
          state = Parser.STATE_CLEF
          self.inter.ctx.debug("[P] Creating last key of block at `"+self.ctx.get_path()+"`")
          self.ctx.create(self.inter.evaluate(buffer+" "))

          self.inter.ctx.debug("[P] Last block key created.")
          self.ctx.back()
          self.ctx.back()
          buffer = ""

        elif char == "#":
          state = Parser.STATE_VAL_C
        else:
          buffer += char
      elif state == Parser.STATE_VAL_C:
        if char == "#" or char == "\n": state = Parser.STATE_VAL
       
      i+= 1 
  
    if state == Parser.STATE_VAL:
      state = Parser.STATE_CLEF
      self.inter.ctx.debug("[P] Creating last key at `"+self.ctx.get_path()+"`")
      self.ctx.create(self.inter.evaluate(buffer+" "))
        
      self.inter.ctx.debug("[P] lastKey created. Path is now `"+str(self.ctx.get_path())+"`")
      self.ctx.back()
      buffer = ""

