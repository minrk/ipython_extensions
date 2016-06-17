"""Disable the IPython notebook pager

turn paged output into print statements
"""

from __future__ import print_function
from IPython.core import page

_save_page = None

def load_ipython_extension(ip):
    global _save_page
    if not hasattr(ip, 'kernel'):
        # not in a kernel, nothing to do
        return
    ip.set_hook('show_in_pager', page.as_hook(page.display_page), 90)

def unload_ipython_extension(ip):
    if hasattr(ip, 'display_page'):
        ip.display_page = _save_page
