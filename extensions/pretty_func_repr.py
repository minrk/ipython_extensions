"""
Trigger pinfo (??) to compute text reprs of functions, etc.

Requested by @katyhuff
"""

import types

from IPython import get_ipython


def pinfo_function(obj, p, cycle):
    """Call the same code as `foo?` to compute reprs of functions
    
    Parameters
    ----------
    obj:
        The object being formatted
    p:
        The pretty formatter instance
    cycle: 
        Whether a cycle has been detected (unused)
    """
    text = get_ipython().inspector._format_info(obj, detail_level=1)
    p.text(text)


_save_types = {}


def load_ipython_extension(ip):
    """register pinfo_function as the custom plain-text repr for funtion types"""
    pprinter = ip.display_formatter.formatters['text/plain']

    for t in (types.FunctionType,
              types.BuiltinMethodType,
              types.BuiltinFunctionType):
        f = pprinter.for_type(t, pinfo_function)
        _save_types[t] = f


def unload_ipython_extension(ip):
    """unregister pinfo_function"""
    pprinter = ip.display_formatter.formatters['text/plain']
    for t, f in _save_types.items():
        pprinter.for_type(t, f)
    
    _save_types.clear()

