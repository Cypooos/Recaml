
def find_next_brackets(string,open,close):
  counter = 0 
  for x in range(len(string)):
    if string[x] == open:counter += 1
    elif string[x] == close: counter -= 1
    if counter == 0:
      return x
  return 0