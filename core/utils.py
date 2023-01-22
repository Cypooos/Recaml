
def find_next_brackets(string,open,close,comm="#"):
  counter = 0 
  comment = False
  for x in range(len(string)):
    if string[x] == comm: comment = not comment
    if string[x] == "\n": comment = False
    if comment: continue
    if string[x] == open:counter += 1
    elif string[x] == close: counter -= 1
    if counter == 0:
      return x
  return 0