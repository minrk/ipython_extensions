# encoding: utf-8
"""
Does *not* execute the cell ("inactive"). Usefull to temporary disable a cell.

Authors:

* Jan Schulz
"""

#-----------------------------------------------------------------------------
#  Copyright (C) 2013  The IPython Development Team
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

from IPython.core.magic import (Magics, magics_class, cell_magic)
from IPython.testing.skipdoctest import skip_doctest
from IPython.core.error import UsageError

@magics_class
class InactiveMagics(Magics):
    """Magic to *not* execute a cell."""

    @skip_doctest
    @cell_magic
    def inactive(self, parameter_s='', cell=None):
        """Does *not* exeutes a cell.
        
        Usage:
          %%inactive
          code...
                
        This magic can be used to mark a cell (temporary) as inactive.
        """
        if cell is None:
            raise UsageError('empty cell, nothing to ignore :-)')
        print("Cell inactive: not executed!")
        

            
def load_ipython_extension(ip):
    ip.register_magics(InactiveMagics)
    print ("'inactive' magic loaded.")