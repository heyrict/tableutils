import sys
sys.path.insert(0,'../..')
import tableutils as tu
with open('template3.txt') as f: data = f.read()
t1 = tu.read_grid(data,reset_linebreak=False)
tu.to_grid(t1)
with open('template2.txt') as f: data = f.read()
t2 = tu.read_grid(data,reset_linebreak=False)
tu.to_grid(t2)
