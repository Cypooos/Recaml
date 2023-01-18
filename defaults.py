from errors import *

class Function:

  def __init__(self,variable,code,temp_var,def_path):
    self.variable = variable
    self.code = code
    self.def_path = def_path
    self.temp_var = temp_var
  
  def __str__(self):
    return "Fct[\\"+self.variable+"("+self.code+"):"+str(self.temp_var)+" at `"+self.def_path+"`]"
  
class Process:
  def __init__(self,code,temp_var,def_path):
    self.code = code
    self.def_path = def_path
    self.temp_var = temp_var
  def __str__(self):
    return "Prcss['"+self.code+"':"+str(self.temp_var)+" at `"+self.def_path+"`]"
  
class Arr:
  def __init__(self,size):
    self.size = size
    self.val = [None for _ in range(size)]


DEFAULT_TYPES = [int,bool,Function,Process]

def load_default(inter):
  """
  DEFAULT_VALS = {}

  def to_default(aliases=[],use_def_name = True):
    def inner(fct):
      def wrapper(a):
        if isinstance(inter.force(a),fct.__annotations__[len(fct.args)-1]):
          fct.args.append(a)
          if len(fct.args) == len(fct.__annotations__)-1:
            fct(fct.args)
          else: return wrapper
        else:
          raise WrongArgument("wrong argument type in default",inter.ctx.get_path())
      for x in aliases:
        DEFAULT_VALS[x] = wrapper
      if use_def_name:DEFAULT_VALS[fct.__name__] = wrapper
    return inner



  @to_default(aliases=["+"])
  def add(a:int,b:int):
    return a + b 

  @to_default(aliases=["-"])
  def sub(a:int,b:int):
    return a - b 
  


  @to_default(aliases=["+"])
  def eq(a:int,b:int):
    return a + b 

  @to_default(aliases=["-"])
  def sub(a:int,b:int):
    return a - b 
  # __annotations__ == {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}

  """

  def add(a,b):
    a = inter.force(a)
    b = inter.force(b)
    if isinstance(a,int) and isinstance(b,int):
      return a + b
    else:
      raise WrongArgument("Add a+b not with int,int",inter.ctx.get_path())
  
  def sub(a,b):
    a = inter.force(a)
    b = inter.force(b)
    if isinstance(a,int) and isinstance(b,int):
      return a - b
    else:
      raise WrongArgument("Add a-b not with int,int",inter.ctx.get_path())

  def mul(a,b):
    a = inter.force(a)
    b = inter.force(b)
    if isinstance(a,int) and isinstance(b,int):
      return a * b
    else:
      raise WrongArgument("Add a*b not with int,int",inter.ctx.get_path())
  
  def if_(cnd,a,b):
    cnd = inter.force(cnd)
    if isinstance(cnd,bool):
      if cnd: return inter.force(a)
      else: return inter.force(b)
    else:
      raise WrongArgument("If cnd a b not with bool, 'a, 'b",inter.ctx.get_path())
  
  def eq(a,b):
    a = inter.force(a)
    b = inter.force(b)
    if isinstance(a,int) and isinstance(b,int):
      return a == b
    elif isinstance(a,bool) and isinstance(b,bool):
      return a == b
    else:
      raise WrongArgument("Add a==b not with int,int nor bool,bool",inter.ctx.get_path())
  
  

  DEFAULT_VALS = {
    "add":lambda a:lambda b: add(a,b),
    "sub":lambda a:lambda b: sub(a,b),
    "mul":lambda a:lambda b: mul(a,b),
    "if":lambda cnd:lambda a:lambda b: if_(cnd,a,b),
    "eq":lambda a:lambda b: eq(a,b),
    "false":False,
    "true":True,
  }
  # defaults function are lambda-defined
  # Aliases for default functions
  for k,v_ in [
      ("==","eq"),
      #(">=","ge"),
      #(">","gt"),
      #("<=","le"),
      #("<","ls"),
      #("&&","and"),
      #("||","or"),
      #("!","not"),
      ("+","add"),
      ("-","sub"),
      #("/","div"),
      ("*","mul"),
    ]:
    DEFAULT_VALS[k] = DEFAULT_VALS[v_]
  return DEFAULT_VALS