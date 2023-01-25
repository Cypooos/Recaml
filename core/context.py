from core.errors import *
from core.defaults import *
from datetime import date, datetime

class Context:

  LOG_DEBUG_FILE = 1
  LOG_DEBUG_PRINT = 2
  LOG_INFO_FILE = 4
  LOG_INFO_PRINT = 8

  LOG_DEFAULT = LOG_DEBUG_FILE | LOG_INFO_FILE | LOG_INFO_PRINT
  LOG_FOLDER = "core/logs/"

  def __init__(self,log_level=None):
    if log_level == None: log_level = Context.LOG_DEFAULT
    self.log_level = log_level
    self.log_file = open(Context.LOG_FOLDER+str(date.today()),"a")
    self.log_file.write("\n\n --- New Instance ("+ str(datetime.now())+") ---\n\n")
    self.indent = 0
    self.recursive_counter = 0 # count the number of blocks call within blocks calls
    self.act_path = []
    self.vars = {}

  def clean(self):
    for k in [x for x in self.vars.keys()]:
      if k.startswith(self.get_path()+self.recursive_counter*"."+"."):
        self.debug("[C] Removing block variable `"+k+"` (called from `"+str(self.get_path())+"`")
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
    self.debug("[C] Setting `"+name+"` as `"+str(ele)+"`")
    if self.get_path() == "":self.vars[name] = ele
    else: self.vars[self.get_path()+"."+name] = ele

  def rem(self,name):
    self.debug("[C] Removing `"+name+"`")
    try:
      if self.get_path() == "":del self.vars[name]
      else: del self.vars[self.get_path()+"."+name]
    except KeyError: pass

  def get(self,string,no_err=False):
    
    self.debug("[C] Searching for",string,"in",self.get_path())

    # list of path to search for in order (from more specific to less specific)
    
    search_paths = [""]
    for x in self.get_path().split("."):
      search_paths.append(search_paths[-1]+x+".")
    search_paths = search_paths[::-1]
    
    for path in search_paths:
      if path+string in self.vars.keys():
        self.debug("[C] Found",path+string,":",self.vars[path+string])

        return self.vars[path+string]
      elif path+string+"." in self.vars.keys():
        self.debug("[C] Found",path+string,":",self.vars[path+string+"."])

        return self.vars[path+string+"."]
    
    if no_err:
      self.debug("[C] Not found, returning None as no_err is set")
      return None
    try:
      a = int(string)
      self.debug("[C] Found litteral:",a)
      return a
    except ValueError:
      if string == "": # if we were searching for "" but no var was found : return expression was empty
        raise EmptyExpression("No definition of `"+self.get_path()+"`",self) from None
      else:
        raise UnknowLitteral("Unknow litteral or variable",self)

  def debug(self,*args):
    msg = "  "*self.indent+" ".join([str(x) for x in args])
    if self.log_level & Context.LOG_DEBUG_PRINT != 0: print(msg)
    if self.log_level & Context.LOG_DEBUG_FILE != 0: self.log_file.write("DEBUG:"+msg+"\n")

  def print(self,msg):
    print(msg)
    self.log_file.write("PRINT:"+msg.replace("\n","\\n")+"\n")
  
  def info(self,*args):
    s = " ".join(args)
    if self.log_level & Context.LOG_INFO_PRINT != 0: print(s)
    if self.log_level & Context.LOG_INFO_FILE != 0: self.log_file.write("INFO :"+ s+"\n")

  def print_keys(self,e=""):
    self.print("\n --- print_keys ---\n")
    for key,value in self.vars.items():
      if key.startswith(e):
        if key.endswith("."):
          self.print(key[:-1]+" : "+str(value))
        else:self.print(key+" : "+str(value))