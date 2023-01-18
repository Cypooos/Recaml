from errors import *
from context import Context
from utils import find_next_brackets
from defaults import *

class Interpretor:

  STACK_LIMIT = 10

  STATE_NORMAL = 0
  STATE_LINK = 1

  SPECIAL = {
    "FUNCTION_DEF":'\\',
    "PARENTHESIS_OPEN":'(',
    "PARENTHESIS_CLOSE":')',
    "CODEBLOCK_OPEN":'{',
    "CODEBLOCK_CLOSE":'}',
  }


  # default function use it to force a Process to be unwrapped
  def force(self,x):
    if isinstance(x, Process):
      return self.force(self.exec(x,None))
    else: return x

  def __init__(self,ctx:Context):
    self.ctx = ctx
    self.ctx.vars = load_default(self)
  
  # exec(a,b) calculate a(b)
  def exec(self,res,val):

    print("  "*self.ctx.indent+"Executing "+str(res)+"("+str(val)+")")
    
    if callable(res):
      return res(val)
    
    while isinstance(res,Process):

      # On ce met dans le contexte de définition de la fonction pour l'executer
      path_save = self.ctx.act_path.copy()
      self.ctx.goto(res.def_path)

      # on créé les variables temporaire de contexte nécéssaire :
      print("  "*self.ctx.indent+"Creating temporary variables (Process)")
      to_del = []
      for (key,value) in res.temp_var:
        if isinstance(value,Process):
          value = self.exec(value,None)
        to_del.append((key,self.ctx.get(key,True)))
        self.ctx.defi(key,value)

      returned = self.evaluate(res.code)

      if isinstance(returned,Function) or isinstance(returned,Process):
        for x in res.temp_var:
          returned.temp_var.append(x)
      
      for k,v in to_del:
        if v == None:
          self.ctx.rem(k)
        else:
          self.ctx.defi(k,v)
      
      self.ctx.goto(path_save)
      res = returned
    
    if val == None:
      return res
    
    if isinstance(res,Function):
      
      # On ce met dans le contexte de définition de la fonction pour l'executer
      path_save = self.ctx.act_path.copy()
      self.ctx.goto(res.def_path)

      # on créé les variables temporaire de contexte nécéssaire :
      print("  "*self.ctx.indent+"Creating temporary variables (Function)")
      to_del = []
      for (key,value) in res.temp_var:
        if isinstance(value,Process):
          value = self.exec(value,None)
        to_del.append((key,self.ctx.get(key,True)))
      to_del.append((res.variable,self.ctx.get(res.variable,True)))
      for (key,value) in res.temp_var:
        self.ctx.defi(key,value)
      self.ctx.defi(res.variable,val)
      print("  "*self.ctx.indent+"Temporary variables: to_del =",to_del)

      returned = self.evaluate(res.code)

      if isinstance(returned,Function) or isinstance(returned,Process):
        for x in res.temp_var:
          returned.temp_var.append(x)
        
        returned.temp_var.append((res.variable,val))
      
      for k,v in to_del:
        if v == None:
          self.ctx.rem(k)
        else:
          self.ctx.defi(k,v)
      
      self.ctx.goto(path_save)
      return returned

    if isinstance(res,int) or isinstance(res,Arr):
      raise WrongArgument("Evaluate arr or int with something, impossible",self.ctx.get_path())
    

      
    

  def evaluate(self,string):

    self.ctx.indent += 1
    if self.ctx.indent >= Interpretor.STACK_LIMIT:
      raise StackOverflow("AYAA",self.ctx.get_path())
    
    result = lambda x:x
    buffer = ""
    i = 0
    state = Interpretor.STATE_NORMAL


    while i < len(string):
      char = string[i]
      
      #--------------#
      # STATE_NORMAL |
      #--------------#

      if state == Interpretor.STATE_NORMAL:
        if char == "(": # if we have a parenthesis expression
          
          # evaluate the buffer
          buffer = buffer.strip()
          if buffer != "":result = self.exec(result,self.ctx.get(buffer))
          buffer = ""

          place = find_next_brackets(string[i:],"(",")")
          if place != 0:
            val = Process(string[i+1:i+place],[],self.ctx.get_path())
            result = self.exec(result,val)
            i += place
          else:
            raise UnclosedBrackets(0,"In code () at `"+str(self.ctx.get_path())+"`")
        
        elif char == "{":
          # TODO: check if it works
          
          # evaluate the buffer
          buffer = buffer.strip()
          if buffer != "":result = self.exec(result,self.ctx.get(buffer))
          buffer = ""

          self.ctx.append("INNER")
          print("  "*self.ctx.indent,"Executing block in ctx:",".".join(self.path))

          place = find_next_brackets(string[i:],"{","}")
          if place != 0:
            self.parse(string[i+1:i+place])
            del self.path[-1]
            result = self.exec(result,self.ctx.get("INNER"))
            i += place
          else:
            raise UnclosedBrackets()

        # end of current fetching and evaluation of result
        elif char == " " and buffer != "" :
          
          # evaluate the buffer
          buffer = buffer.strip()
          if buffer != "":result = self.exec(result,self.ctx.get(buffer))
          buffer = ""
        
        # beginning of creating a fonction, also an end of the current fetching 
        elif char == Interpretor.SPECIAL["FUNCTION_DEF"]:
          print("  "*self.ctx.indent + "Fetching linkable variables...")
          
          # evaluate the buffer
          buffer = buffer.strip()
          if buffer != "":result = self.exec(result,self.ctx.get(buffer))
          buffer = ""
          
          state = Interpretor.STATE_LINK
        else:buffer += char

      #------------#
      # STATE_LINK #
      #------------#
      
      elif state == Interpretor.STATE_LINK:

        # TODO: multiple variables

        # end of the fetching for the variable's name
        if char == "(":
          print("  "*self.ctx.indent + "End of fetching variable for fct:`"+buffer+"`")

          place = find_next_brackets(string[i:],"(",")")
          if place != 0:
            print("  "*self.ctx.indent + "Applying custom fct to result (execute)")
            fct = Function(buffer,string[i+1:i+place],[],self.ctx.get_path())
            result = self.exec(result,fct)
            buffer = ""
            i += place
            state = Interpretor.STATE_NORMAL
          else:
            raise UnclosedBrackets
        elif char == "{":
          print("  "*self.ctx.indent + "End of fetching variable for block:`"+buffer+"`")

          place = find_next_brackets(string[i:],"{","}")
          if place != 0:
            print("  "*self.ctx.indent + "Applying custom fct to result (execute)")
            fct = Function(buffer,string[i:i+place+1],[],self.ctx.get_path())
            result = self.exec(result,fct)
            buffer = ""
            i += place
            state = "normal"
          else:
            raise UnclosedBrackets
        else:
          buffer += char
      i+=1


    # evaluate the buffer if there's things left
    buffer = buffer.strip()
    if buffer != "":result = self.exec(result,self.ctx.get(buffer))
    buffer = ""

    # if only Process is left, executing it.
    while isinstance(result,Process):
      print("  "*self.ctx.indent+"Delayed expression executed as it is the last remaning one")
      result = self.exec(result,None)
    
    shorten = str(result) if len(str(result)) <= 40 else str(result)[:40]+"..."
    print("  "*self.ctx.indent + "Result is: `"+shorten+"`")
    self.ctx.indent -= 1
    return result