from random import randint
from core.errors import *
from core.context import Context
#from parse import Parser
from core.utils import find_next_brackets
from core.defaults import *

class Interpretor:

  STACK_LIMIT = 30

  STATE_NORMAL = 0
  STATE_LINK = 1

  SPECIAL = {
    "FUNCTION_DEF":'\\',
    "PARENTHESIS_OPEN":'(',
    "PARENTHESIS_CLOSE":')',
    "CODEBLOCK_OPEN":'{',
    "CODEBLOCK_CLOSE":'}',
  }


  # default function use it to force a Process / Codeblock to be unwrapped.
  # Codeblocks are only unwrapped with a default. 
  def force(self,x):
    
    if isinstance(x, Process):
      return self.force(self.exec(x,None))

    if isinstance(x, CodeBlock):
      s = "."*self.ctx.recursive_counter
      self.ctx.recursive_counter += 1 # to avoid overwriting variables, we make sure to be in a new scope
      self.ctx.append(s)
      
      self.ctx.debug("[I] Executing code block in ctx `"+self.ctx.get_path()+"`")
      try:
        self.parser.parse(x.code)
      except RecamlError as e:
        self.ctx.back()
        e.paths[-1] = self.ctx.get_path()
        raise e 
      self.ctx.back()
      returned = self.ctx.get(s+".")
      self.ctx.clean() # clear all '..' variables defined from this scope
      self.ctx.recursive_counter -= 1
      return self.force(returned)

    else: return x

  def __init__(self,ctx:Context,parser):
    self.ctx = ctx
    self.parser = parser
    load_default(self)
  
  # exec(a,b) calculate a(b)
  def exec(self,res,val,reversed=False):

    self.ctx.debug("[I] Executing "+str(res)+"("+str(val)+")")
    
    if callable(res):
      return res(val)
    
    while isinstance(res,Process):

      # On ce met dans le contexte de définition de la fonction pour l'executer
      path_save = self.ctx.act_path.copy()
      self.ctx.goto(res.def_path)

      # on créé les variables temporaire de contexte nécéssaire :
      self.ctx.debug("[I] Creating temporary variables (Process)")
      to_del = []
      for (key,value) in res.temp_var:
        if isinstance(value,Process):
          try:
            value = self.exec(value,None)
          except RecamlError as e:
            e.paths.append(".".join(path_save))
            raise e 
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
    
    if val == None: # this way you can use result = self.exec(process,None) to evaluate a process
      return res
    
    if isinstance(res,Function):

      # In case of custom functions, always call res if it's a Process before.
      # Otherwise, fact (sub a 1) will load fact witch will load fact... without calculating (sub a 1) since it's a Process
      # Also known as in (a + c()), we calculate the c() before calculating a + result
      while isinstance(val,Process):
        self.ctx.debug("[I] Function Called with Process, calculating process.")
        val = self.exec(val,None)

      # On ce met dans le contexte de définition de la fonction pour l'executer
      path_save = self.ctx.act_path.copy()
      self.ctx.goto(res.def_path)

      # on créé les variables temporaire de contexte nécéssaire :
      self.ctx.debug("[I] Creating temporary variables (Function)")
      to_del = []
      for (key,value) in res.temp_var:
        if isinstance(value,Process):
          value = self.exec(value,None)
        to_del.append((key,self.ctx.get(key,True)))
      to_del.append((res.variable,self.ctx.get(res.variable,True)))
      for (key,value) in res.temp_var:
        self.ctx.defi(key,value)
      self.ctx.defi(res.variable,val)
      self.ctx.debug("[I] Temporary variables: to_del =",to_del)

      try:
        returned = self.evaluate(res.code)
      except RecamlError as e:
        e.paths.append(".".join(path_save))
        raise e 

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

    else:
      if reversed:
        raise WrongArgument("Impossible to evaluate `"+res.__class__.__name__+"` with `"+val.__class__.__name__+"`",self.ctx)
      else:
        self.ctx.debug("[I] Trying reverse execution")
        return self.exec(val,res,True)


      
    

  def evaluate(self,string):

    self.ctx.indent += 1
    if self.ctx.indent >= Interpretor.STACK_LIMIT:
      raise StackOverflow("Too much recursion (limit is "+str(self.STACK_LIMIT)+")",self.ctx)
    
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
            raise UnclosedBrackets("Unclosed code parenthesis",self.ctx)
        
        elif char == "{":
          # evaluate the buffer
          buffer = buffer.strip()
          if buffer != "":result = self.exec(result,self.ctx.get(buffer))
          buffer = ""

          place = find_next_brackets(string[i:],"{","}")
          if place != 0:
            val = CodeBlock(string[i+1:i+place],[],self.ctx.get_path())
            result = self.exec(result,val)
            i += place
          else:
            raise UnclosedBrackets("Unclosed code brackets",self.ctx)

        # end of current fetching and evaluation of result
        elif char == " " and buffer != "" :
          
          # evaluate the buffer
          buffer = buffer.strip()
          if buffer != "":result = self.exec(result,self.ctx.get(buffer))
          buffer = ""
        
        # beginning of creating a fonction, also an end of the current fetching 
        elif char == Interpretor.SPECIAL["FUNCTION_DEF"]:
          self.ctx.debug("[I] Fetching linkable variables...")
          
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
          self.ctx.debug("[I] End of fetching variable for fct:`"+buffer+"`")

          place = find_next_brackets(string[i:],"(",")")
          if place != 0:
            self.ctx.debug("[I] Applying custom fct to result (execute)")
            fct = Function(buffer,string[i+1:i+place],[],self.ctx.get_path())
            result = self.exec(result,fct)
            buffer = ""
            i += place
            state = Interpretor.STATE_NORMAL
          else:
            raise UnclosedBrackets("Unclosed function opening parenthesis",self.ctx)
        elif char == "{":
          self.ctx.debug("[I] End of fetching variable for block:`"+buffer+"`")

          place = find_next_brackets(string[i:],"{","}")
          if place != 0:
            self.ctx.debug("[I] Applying custom fct to result (execute)")
            fct = Function(buffer,string[i:i+place+1],[],self.ctx.get_path())
            result = self.exec(result,fct)
            buffer = ""
            i += place
            state = Interpretor.STATE_NORMAL
          else:
            raise UnclosedBrackets("Unclosed function opening brackets",self.ctx)
        else:
          buffer += char
      i+=1


    # evaluate the buffer if there's things left
    buffer = buffer.strip()
    if buffer != "":result = self.exec(result,self.ctx.get(buffer))
    buffer = ""

    while isinstance(result,Process) or isinstance(result,CodeBlock):
      self.ctx.debug("[I] Delayed expression executed as it is the last remaning one")
      result = self.force(result)
    
    
    shorten = str(result) if len(str(result)) <= 40 else str(result)[:40]+"..."
    self.ctx.debug("[I] Result is: `"+shorten+"`")
    self.ctx.indent -= 1
    return result