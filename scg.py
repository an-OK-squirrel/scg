# SCG
# yep, it's happening! :D
# whee

import sys
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
program = ".xYz.yZ000x4"

print(split_into_st(program))