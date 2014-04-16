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
    _save_page = page
    page.page = print

def unload_ipython_extension(ip):
    if _save_page is not None:
        page.page = _save_page
