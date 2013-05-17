"""
%%closure cell magic for running the cell in a function,
reducing pollution of the namespace

%%forget does the same thing, but explicitly deletes new names,
rather than wrapping the cell in a function.
"""

from IPython.utils.text import indent

def closure(line, cell):
    """run the cell in a function, generating a closure
    
    avoids affecting the user's namespace
    """
    ip = get_ipython()
    func_name = "_closure_magic_f"
    block = '\n'.join([
        "def %s():" % func_name,
        indent(cell),
        "%s()" % func_name
    ])
    ip.run_cell(block)
    ip.user_ns.pop(func_name, None)

def forget(line, cell):
    """cleanup any new variables defined in the cell
    
    avoids UnboundLocals that might show up in %%closure
    
    changes to existing variables are not affected
    """
    ip = get_ipython()
    before = set(ip.user_ns.keys())
    ip.run_cell(cell)
    after = set(ip.user_ns.keys())
    for key in after.difference(before):
        ip.user_ns.pop(key)

def load_ipython_extension(ip):
    mm = ip.magics_manager
    mm.register_function(closure, 'cell')
    mm.register_function(forget, 'cell')

    