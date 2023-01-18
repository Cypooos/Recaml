class ParsingError(Exception):
  def __init__(self,line,msg):
    self.line = line
    self.msg = msg

class InterpretorError(Exception):
  def __init__(self,msg,path):
    self.msg = msg
    self.path = path


class StackOverflow (InterpretorError):
  pass

class UnknowLitteral (ParsingError):
  pass

class UnclosedBrackets (ParsingError):
  pass

class WrongArgument (InterpretorError):
  pass

class EmptyExpression (Exception):
  pass

