"""
Use TextMate as the editor

Usage:  %load_ext editmate

Now when you %edit something, it opens in textmate.
This is only necessary because the textmate command-line entrypoint
doesn't support the +L format for linenumbers, it uses `-l L`.

"""

from subprocess import Popen, list2cmdline
from IPython.core.error import TryNext

def edit_in_textmate(self, filename, linenum=None, wait=True):
    cmd = ['mate']
    if wait:
        cmd.append('-w')
    if linenum is not None:
        cmd.extend(['-l', str(linenum)])
    cmd.append(filename)
    
    proc = Popen(list2cmdline(cmd), shell=True)
    if wait and proc.wait() != 0:
        raise TryNext()
    
def load_ipython_extension(ip):
    ip.set_hook('editor', edit_in_textmate)
