from core.errors import *

class Function:

  def __init__(self,variable,code,temp_var,def_path):
    self.variable = variable
    self.code = code
    self.def_path = def_path
    self.temp_var = temp_var
  
  def __str__(self):
    return "Fct[\\"+self.variable+"("+self.code.replace("\n","\\\\")[:20]+"):"+str(self.temp_var)+" at `"+self.def_path+"`]"
  
class Process:
  def __init__(self,code,temp_var,def_path):
    self.code = code
    self.def_path = def_path
    self.temp_var = temp_var
  def __str__(self):
    return "Prcss['"+self.code.replace("\n","\\\\")[:20]+"':"+str(self.temp_var)+" at `"+self.def_path+"`]"
  
class Arr:
  def __init__(self,size):
    self.size = size
    self.val = [None for _ in range(size)]


DEFAULT_TYPES = [int,bool,Function,Process]

def load_default(inter):

  # this decorator curryfy a function, and add a type checker on the aguments, to make adding defaults very easy.
  def to_default(aliases=[],use_def_name=True,force=True):
    def wrapper(fct):
      fct.types = list(fct.__annotations__.values())
      def new_fct(a,args=()):
        if force:a = inter.force(a)
        if a.__class__ == fct.types[len(args)] or fct.types[len(args)] == any or not force:
          args = args + (a,)
          if len(args) == len(fct.__annotations__.values()):
            return fct(*args)
          else:
            return lambda x:new_fct(x,args=args)
        else:
          raise WrongArgument("Wrong argument type in `"+str(fct.__name__)+"`, argument n°"+str(len(args)+1)+" should be of type `"+str(fct.types[len(args)].__name__)+"` but `"+str(a.__class__.__name__)+"` was found",inter.ctx)


      for x in aliases:
        inter.ctx.vars[x] = new_fct
      if use_def_name:inter.ctx.vars[fct.__name__] = new_fct
      return new_fct
    return wrapper

  @to_default(["+"])
  def add(a:int,b:int):
    return a + b
  
  @to_default(["-"])
  def sub(a:int,b:int):
    return a - b
  
  @to_default(["*"])
  def mul(a:int,b:int):
    return a * b

  @to_default(["/"])
  def div(a:int,b:int):
    return a // b
  
  @to_default(["%"])
  def mod(a:int,b:int):
    return a % b
  
  # don't force by default all arguments, otherwise all branch of a if statement would
  # be calculated and stack overflow would occur in recursive function for example
  @to_default(["if"],use_def_name=False,force=False) 
  def if_(cnd:bool,a:any,b:any):
    cnd = inter.force(cnd)
    if isinstance(cnd,bool):
      if cnd: return inter.force(a) # only force them once they are sure
      else: return inter.force(b)
    else:
      raise WrongArgument("Wrong argument type for `if a b c` : a is not a bool",inter.ctx)
  
  @to_default(["="])
  def eq(a:any,b:any):
    if isinstance(a,b.__class__):
      return a == b
    else:
      raise WrongArgument("Wrong argument type for `eq a b` : a and b are not of the same type",inter.ctx)
  
  @to_default(["or","||"],use_def_name=False)
  def or_(a:bool,b:bool):
    return a or b
  
  @to_default(["and","&&"],use_def_name=False)
  def and_(a:bool,b:bool):
    return a and b
  
  @to_default(["^^"])
  def xor(a:bool,b:bool):
    return a ^ b
  
  @to_default(["not","!"],use_def_name=False)
  def not_(a:bool):
    return not a
  
  for k,v in {
    "true":True,
    "false":False,
  }.items():
    inter.ctx.vars[k] = v
  