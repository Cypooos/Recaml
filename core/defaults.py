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
    def inner(fct):
      fct.args = []
      fct.annot = list(fct.__annotations__.values())
      print("[D] Adding `"+str(fct.__name__)+"` to defaults")
      print("[D] args are: "+str(fct.annot))
      def wrapper(a):
        if isinstance(inter.force(a),fct.annot[len(fct.args)]):
          if force:fct.args.append(inter.force(a))
          else:fct.args.append(a)
          if len(fct.args) == len(fct.annot):
            print("[D] Calling `"+str(fct.__name__)+"` with",fct.args)
            ret = fct(*fct.args)
            fct.args = [] # resseting the arguments
            return ret
          else: return wrapper
        else:
          raise WrongArgument("Wrong argument type in default",inter.ctx.get_path())
      for x in aliases:
        inter.ctx.vars[x] = wrapper
      if use_def_name:inter.ctx.vars[fct.__name__] = wrapper
    return inner

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
  def if_(cnd:bool,a:object,b:object):
    cnd = inter.force(cnd)
    if isinstance(cnd,bool):
      if cnd: return inter.force(a) # only force them once they are sure
      else: return inter.force(b)
    else:
      raise WrongArgument("If cnd a b not with bool, 'a, 'b",inter.ctx.get_path())
  
  @to_default(["="])
  def eq(a:object,b:object):
    if isinstance(a,b.__class__):
      return a == b
    else:
      raise WrongArgument("a==b not with the same type",inter.ctx.get_path())
  
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
  