# SCG
# yep, it's happening! :D
# whee

import sys
from inter import *
from sparser import *


try:
    path = sys.argv[1]
    f = open(path, encoding='utf-8')
    program = f.read()
    f.close()
except Exception:
    exit()


program = fully_parse(program)
inter = Inter()
inter.run_code(program)
inter.output()
