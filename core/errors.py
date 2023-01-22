class RecamlError(Exception):
  def __init__(self,msg,ctx):
    self.msg = msg
    self.ctx = ctx
    self.paths = [ctx.get_path()]
  
  def __str__(self) -> str:
    if "".join(self.paths) == "":
      txt = " at top level"
    else:txt = "\nin :\n - "+"\n - ".join(self.paths)
    return self.__class__.__name__+"\nAn error as occured:\n"+str(self.msg)+txt

class StackOverflow (RecamlError):
  pass

class UnknowLitteral (RecamlError):
  pass

class UnclosedBrackets (RecamlError):
  pass

class WrongArgument (RecamlError):
  pass

class EmptyExpression (RecamlError):
  pass

class PathError (RecamlError):
  pass

