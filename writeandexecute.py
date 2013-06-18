# encoding: utf-8
"""
Writes a cell to a designated *.py file and executes the cell afterwards.

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
import os
import io

from IPython.utils import py3compat

from IPython.core.magic import (Magics, magics_class, cell_magic)
from IPython.testing.skipdoctest import skip_doctest
from IPython.core.error import UsageError

@magics_class
class WriteAndExecuteMagics(Magics):
    """Magic to save a cell into a .py file."""

    @skip_doctest
    @cell_magic
    def writeandexecute(self, parameter_s='', cell=None):
        """Writes the content of the cell to a file and then executes the cell.
        """
        
        opts,args = self.parse_options(parameter_s,'i:d')
        if cell is None:
            raise UsageError('Nothing to save!')
        if not ('i' in opts) or not opts['i']:
            raise UsageError('Missing indentifier: include "-i=<indentifier>"')
        identifier = opts['i']
        debug = False if not "d" in opts else True
        if not args:
            raise UsageError('Missing filename')
        filename = args
        code_content = self.shell.input_transformer_manager.transform_cell(cell)
        self._save_to_file(filename, identifier, code_content, debug=debug)

        ip = get_ipython()
        ip.run_cell(cell)
        
    def ensure_dir(self, f):
        d = os.path.dirname(f)
        if not os.path.exists(d):
            os.makedirs(d)  
            
    def _save_to_file(self, path, identifier, content, debug=False):
            pypath = os.path.splitext(path)[0] + '.py'
            code_identifier = "# -- ==%s== --" % identifier
            new_content = []
            if not os.path.isfile(pypath):
                # The file does not exist, so simple create a new one
                if debug:
                    print("Created new file: %s" % pypath)
                new_content.extend([u'# -*- coding: utf-8 -*-\n\n', code_identifier , content, code_identifier])
            else:
                # If file exist, read in the content and either replace the code or append it
                in_code_block = False
                included_new = False
                lineno = 0
                with io.open(pypath,'r', encoding='utf-8') as f:
                    for line in f:
                        if line[-1] == "\n":
                            line = line[:-1]
                        lineno += 1
                        if line.strip() == code_identifier:
                            if included_new and not in_code_block:
                                # we found a third one -> Error!
                                raise Exception("Found more than two lines with identifiers in file '%s' in line %s. "
                                    "Please fix the file so that the identifier is included exactly two times." % (pypath, lineno))
                            # Now we are either in the codeblock or just outside
                            # Switch the state to either "in our codeblock" or outside again
                            in_code_block = True if not in_code_block else False
                            if not included_new:
                                # The code was not included yet, so add it here...
                                # No need to add a code indentifier to the end as we just add the ending indentifier from the last 
                                # time when the state is switched again.
                                new_content.extend([code_identifier, content])
                                included_new = True
                        # This is something from other code cells, so just include it. All code 
                        # "in_code_block" is replace, so do not include it
                        if not in_code_block:
                            new_content.append(line)
                # And if we didn't include out code yet, lets append it to the end...
                if not included_new:
                    new_content.extend(["\n", code_identifier, content, code_identifier, "\n"])
            
            new_content = unicode(u'\n'.join(new_content))
            
            #Now write the complete code back to the file
            self.ensure_dir(pypath)
            with io.open(pypath,'w', encoding='utf-8') as f:
                if not py3compat.PY3 and not isinstance(new_content, unicode):
                    # this branch is likely only taken for JSON on Python 2
                    new_content = py3compat.str_to_unicode(new_content)
                f.write(new_content)
                if debug:
                    print("Wrote cell to file: %s" % pypath)


            
def load_ipython_extension(ip):
    ip.register_magics(WriteAndExecuteMagics)
    print ("'writeandexecute' magic loaded.")