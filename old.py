from errors import *
from context import Context
from utils import find_next_brackets
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

  STACK_LIMIT = 30 # t_lim = 333

  def __init__(self):
    self.ctx = Context()


  # use to evaluate `res` with a value `val`.
  # if `res` is a delayed and `val` is None it will just execute res
  def exec(self,res,val,inversed=False):

    # print("  "*self.ctx+"self.exec with",res,val,inversed)

    # if it's a default function
    if callable(res):
      return res(val)

    # if it's a user-defined function
    elif isinstance(res, tuple):

      # get path to call fct:
      if res[0] != None: res[3].append("X")
      current = ".".join(res[3])
      if current != "": current += "."

      # Setting the variables. Calculating them if they are delayed before setting -> o(1) instead of o(usages)
      to_del = []
      for (to_set,set) in res[2]:
        to_del.append(current+to_set)
        if isinstance(set,tuple) and set[0] == None:
          self.vars[current+to_set] = self.exec(set,None) 
        else:self.vars[current+to_set] = set 
      if res[0] != None:
        to_del.append(current+res[0])
        if isinstance(val,tuple) and val[0] == None:
          self.vars[current+res[0]] = self.exec(val,None)
        else:self.vars[current+res[0]] = val

      # setting path
      path_save = self.path.copy()
      self.path = res[3].copy()
      
      print("  "*self.ctx+"Setting",current+str(res[0]),":=",val,"for evalating `"+res[1]+"` with path",res[3],"and ctx var",res[2])
      # print("\n\n ---- VARS are ----")
      # print(self.path)
      # self.start()

      # executing the fct code / the delay code
      ret = self.execute(res[1])
      
      # restoring the path
      self.path = path_save




      # adding the context variables to the result if it's a function, and delete them
      if isinstance(ret,tuple):
        ret[3].pop()
        print("  "*self.ctx+"Applying complete, ret[2] is now",ret[2])
        if ret[0] != None:
          for x in to_del:
            ret[2].append((x.replace(current,""),self.vars[x]))
      else:
        print("  "*self.ctx+"Applying complete, ret is now",ret)

      # delete all vars
      for x in to_del:
        print("DELETE",x)
        del self.vars[x]
      
      return ret
    
    elif inversed:
      print("  "*self.ctx+"/!\ Applying",val,"on non callable result `"+str(res)+"`")
      raise WrongArgument
    else:
      # if we can't execute res with val, we will try to execute val with res
      print("  "*self.ctx+"Testing inverted version")
      return self.exec(val, res, True)

  def execute(self,string):

    string += " "
    shorten = string if len(string) <= 40 else string[:40]+"..."

    print("  "*self.ctx+">> Computing `"+string+"` <<")

    self.ctx += 1
    self.rec_counter = max(self.ctx,self.rec_counter)
    if self.ctx >= self.STACK_LIMIT:
      raise StackOverflow
    
    result = lambda x : x
    state = "normal"
    data = ""
    i = 0


    while i < len(string):

      char = string[i]
      data = data.strip()
      
      if state == "normal":
        
        if char == "(": # if we have a parenthesis expression
          
          if data != "":result = self.exec(result,self.get_expr(data))
          data = ""
          place = find_next_brackets(string[i:],"(",")")
          if place != 0:
            result = self.exec(result,(None,(string[i+1:i+place]),[],self.path.copy()))
            i += place
          else:
            raise UnclosedBrackets()
        
        elif char == "{":
          
          if data != "":result = self.exec(result,self.get_expr(data))
          data = ""
          self.path.append("INNER")
          print("  "*self.ctx,"Executing block in ctx:",".".join(self.path))

          place = find_next_brackets(string[i:],"{","}")
          if place != 0:
            self.parse(string[i+1:i+place])
            del self.path[-1]
            result = self.exec(result,self.get_expr("INNER"))
            i += place
          else:
            raise UnclosedBrackets()
          


        # end of current fetching and evaluation of result
        elif char == " " and data != "" :
          
          result = self.exec(result,self.get_expr(data))
          data = ""
        
        # beginning of creating a fonction, also an end of the current fetching 
        elif char == "\\":
          print("  "*self.ctx + "Fetching linkable variables...")
          
          if data != "":result = self.exec(result,self.get_expr(data))
          data = ""
          
          state = "link"
        else:data += char
      
      elif state == "link":
        # end of the fetching for the variable's name
        if char == "(":
          print("  "*self.ctx + "End of fetching variables for fct:`"+data+"`")

          place = find_next_brackets(string[i:],"(",")")
          if place != 0:
            print("  "*self.ctx + "Applying custom fct to result (execute)")
              
            fct_data = (data,string[i+1:i+place],[],self.path.copy()) # context
            result = self.exec(result,fct_data)
            data = ""
            i += place
            state = "normal"
            break
          else:
            raise UnclosedBrackets
        elif char == "{":
          print("  "*self.ctx + "End of fetching variables for block:`"+data+"`")

          place = find_next_brackets(string[i:],"{","}")
          if place != 0:
            print("  "*self.ctx + "Applying custom fct to result (execute)")
              
            fct_data = (data,string[i:i+place+1],[],self.path.copy()) # context
            result = self.exec(result,fct_data)
            data = ""
            i += place
            state = "normal"
            break
          else:
            raise UnclosedBrackets
        else:
          data += char
      i+=1
    
    while isinstance(result,tuple) and result[0] == None:
      print("  "*self.ctx+"Delayed expression executed as it is the last remaning one")
      result = self.exec(result,None)
    shorten = str(result) if len(str(result)) <= 40 else str(result)[:40]+"..."
    print("  "*self.ctx + "Result is: `"+shorten+"`")
    self.ctx -= 1
    return result


  def parse(self,string):

    # state in ["clef", "val","clefC", "valC"]
    
    state = "clef"
    i = 0
    self.path.append("")
    while i <len(string):
      char = string[i]


      if state == "clef":
        if char == ":":
          state = "val"
          self.path.append("")
        elif char == "{":
          self.path.append("")
        elif char == "}":
          del self.path[-1]
          self.path[-1] = ""
        elif char == "#":
          state="clefC"
        else:
          self.path[-1]+=char
      
      elif state == "clefC":
        if char == "#" or char == "\n":state = "clef"
      elif state == "val":
        if char == "{":
          place = find_next_brackets(string[i:],"{","}")
          if place != 0:
            self.path[-1] += string[i:i+place+1]
            i += place
          else:
            raise UnclosedBrackets

        elif char == ";":
          self.path = list(filter(lambda x: x != "", [ x.strip() for x in self.path]))
          self.path,code = self.path[:-1],self.path[-1]
          state = "clef"
          path_str = ".".join(self.path)

          print("  "*self.ctx +"\n --- New Key ---\nSetting `"+path_str+"`")
          self.rec_counter = 0
          print(self.path)
          self.vars[path_str] = self.execute(code)
          print("  "*self.ctx +"Key added. rec_counter="+str(self.rec_counter)+"\n")
          self.path[-1] = ""
        elif char == "}":
          del self.path[-1]
          self.path[-1] = ""
        elif char == "#":
          state = "valC"
        else:
          self.path[-1]+= char
      elif state == "valC":
        if char == "#" or char == "\n":state = "val"
       
      i+= 1 
    print(vars)


  def start(self):
    print("\n".join([k+":"+str(v) for k,v in self.vars.items() if "_" in k]))
    print(self.path)
    pass