"""namespace magic

Shorthand for initializing the user namespace in IPython with my common imports.
"""

from IPython import get_ipython
from IPython.utils.importstring import import_item

namespaces = {
    'numpy' : {
        'np' : 'numpy',
        'numpy' : 'numpy',
    },
    'pandas' : {
        'pandas' : 'pandas',
        'pd' : 'pandas',
    },
    'matplotlib' : {
        'mpl' : 'matplotlib',
        'matplotlib' : 'matplotlib',
        'plt' : 'matplotlib.pyplot',
    },
    'stdlib' : {
        'os' : 'os',
        're' : 're',
        'sys' : 'sys',
        'time' : 'time',
        'pjoin' : 'os.path.join',
        'dt' : 'datetime',
        'datetime' : 'datetime',
    }
}

def import_ns(d):
    """turn a dict of import strings into a dict of objects"""
    ns = {}
    for key, s in d.items():
        ns[key] = import_item(s)
    return ns

def load_namespace(names):
    """Load one or more predefined namespace
    
    Usage:
    
        %namespace numpy pandas matplotlib
    """
    ip = get_ipython()
    user_ns = ip.user_ns
    for name in names.split():
        d = namespaces[name]
        ns = import_ns(d)
        user_ns.update(ns)


def load_ipython_extension(ip):
    ip.magics_manager.register_function(load_namespace, 'line', 'namespace')