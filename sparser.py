import re

L_LETTERS = "abcdefghijklmnopqrstuvwxyz"
U_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
ALL_LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
OPERATORS = L_LETTERS + "+*/-"
WHITESPACE = " \t"

def does_regex_match(regex, string):
  thing = re.match(regex, string)
  try:
    return str(thing) != None and thing.group() == string
  except AttributeError:
    return False

def split_into_st(program):
  # split_into_st("apple") # ['a', 'p', 'p', 'l', 'e']
  result = []
  char_index = 0
  token_type = 0  # 0 is none, 1 is op, 2 is num, I'll think of more later
    # actually, for that matter, what other types are there?
  token = ""

  while char_index < len(program):
    char = program[char_index]
    if token_type == 0:  # Token is empty
      if char in WHITESPACE:  # Y U whitespace in codegolf?
        token = ""
        token_type = 0
      elif char in OPERATORS:  # Do things
        token += char
        token_type = 1
        result.append([token, token_type])
        token = ""  # reset
        token_type = 0
      elif char == ".":
        token += "."
        token_type = 1
      elif char in DIGITS:
        token += char
        token_type = 2
    elif token_type == 1:
      token += char
      result.append([token, token_type])
      token = ""
      token_type = 0
    elif token_type == 2:
      if char in DIGITS:
        token += char
      elif char == ".":
        pass  #token += char
      else:
        result.append([token, token_type])
        token = ""
        token_type = 0
        char_index -= 1

    char_index += 1
  result.append([token, token_type])
  return result

types = ["none", "operator", ".operator"]

def parse_token_st(tokens):
  result = []
  for token in tokens:
    token_type = token[1]
    if token_type == 0:
      pass
    elif token_type == 1:
      result.append({'token_type': 'operator', 'token_value': token[0]})
    elif token_type == 2:
      result.append({'token_type': 'integer', 'token_value': int(token[0])})
  return result