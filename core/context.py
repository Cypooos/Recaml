from core.errors import *
from core.defaults import *

class Context:

  def __init__(self):

    self.indent = 0
    self.recursive_counter = 0 # count the number of blocks call within blocks calls
    self.act_path = []
    self.vars = {}

  def clean(self):
    for k in [x for x in self.vars.keys()]:
      if k.startswith(self.get_path()+self.recursive_counter*"."+"."):
        print("  "*self.indent+"[C] Removing block variable `"+k+"` (called from `"+str(self.get_path())+"`")
        del self.vars[k]

  def append(self,folder):
    self.act_path.append(folder.strip())
  
  def goto(self,path):
    if isinstance(path,str):
      self.act_path = path.split(".")
    else: self.act_path = path

  def back(self):
    try:
      self.act_path.pop()
    except IndexError:
      raise UnclosedBrackets("Unclosed brackets",self)
  
  def get_path(self):
    return ".".join(self.act_path)

  def create(self,ele,path=None):
    if path == None: path = self.get_path()
    self.vars[self.get_path()] = ele
  
  def defi(self,name,ele):
    print("  "*self.indent+"[C] Setting `"+name+"` as `"+str(ele)+"`")
    if self.get_path() == "":self.vars[name] = ele
    else: self.vars[self.get_path()+"."+name] = ele

  def rem(self,name):
    print("  "*self.indent+"[C] Removing `"+name+"`")
    try:
      if self.get_path() == "":del self.vars[name]
      else: del self.vars[self.get_path()+"."+name]
    except KeyError: pass

  def get(self,string,no_err=False):
    
    print("  "*self.indent+"[C] Searching for",string,"in",self.get_path())

    # list of path to search for in order (from more specific to less specific)
    
    search_paths = [""]
    for x in self.get_path().split("."):
      search_paths.append(search_paths[-1]+x+".")
    search_paths = search_paths[::-1]
    
    for path in search_paths:
      if path+string in self.vars.keys():
        print("  "*self.indent+"[C] Found",path+string,":",self.vars[path+string])

        return self.vars[path+string]
      elif path+string+"." in self.vars.keys():
        print("  "*self.indent+"[C] Found",path+string,":",self.vars[path+string+"."])

        return self.vars[path+string+"."]
    
    if no_err:
      print("  "*self.indent+"[C] Not found, returning None as no_err is set")
      return None
    try:
      a = int(string)
      print("  "*self.indent+"[C] Found litteral:",a)
      return a
    except ValueError:
        
      if string == "": # if we were searching for "" but no var was found : return expression was empty
        raise EmptyExpression("No definition of `"+self.get_path()+"`",self) from None
      else:
        raise UnknowLitteral("Unknow litteral or variable",self)


  def print(self,e=""):
    for key,value in self.vars.items():
      if key.startswith(e):
        if key.endswith("."):
          print(key[:-1]+" : "+str(value))
        else:print(key+" : "+str(value))