"""
abstraction magics

let's you turn a cell into a function

In [1]: plot(x, f(y))
   ...: xlabel('x')
   ...: ylabel('y')

In [2]: %functionize 1
"""
from IPython.utils.text import indent

def parse_ranges(s):
    blocks = s.split(',')
    ranges = []
    for block in blocks:
        if '-' in block:
            start, stop = [ int(b) for b in block.split('-') ]
            stop = stop + 1 # be inclusive?
        else:
            start = int(block)
            stop = start + 1
        ranges.append((start, stop))
    return ranges

def functionize(line):
    shell = get_ipython()
    splits = line.split(' ', 1)
    range_str = splits[0]
    args = splits[1] if len(splits) > 1 else ''
    
    ranges = parse_ranges(range_str)
    get_range = shell.history_manager.get_range
    
    blocks = ["def cell_function(%s):" % args]
    for start, stop in ranges:
        cursor = get_range(0, start, stop)
        for session_id, cell_id, code in cursor:
            blocks.append(indent(code))
    
    code = '\n'.join(blocks)
    shell.set_next_input(code)


def load_ipython_extension(ip):
    ip.magics_manager.register_function(functionize)