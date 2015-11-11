# SCG
# yep, it's happening! :D
# whee

import sys
from inter import *
from sparser import *

'''
try:
  path = sys.argv[1]
  f = open(path, 'r')
  program = f.read()
  f.close()

  print(program)
except Exception:
  exit()

'''

# for now, programs are taken by text input due for debugging
# TODO: Add like the real thing
program = '1 2'

# print(fully_parse(program))
# print(split_into_st(program))
program = fully_parse(program)
inter = Inter()
inter.run_code(program)
inter.output()
# print(inter.stack)