"""
Illustration of a configurable Magics class

To use:

%load_ext msgmagic
%msg
%config MsgMagic
%config MsgMagic.message = "Hello, there!"
%msg
"""
from IPython.config import Configurable
from IPython.core.magic import magics_class, Magics, line_magic

from IPython.utils.traitlets import Unicode

@magics_class
class MsgMagic(Magics, Configurable):
    message = Unicode("my message", config=True, help="The message printed by `%msg`")
    
    def __init__(self, shell):
        Configurable.__init__(self, parent=shell)
        Magics.__init__(self, shell)
        # this adds me to the `%config` list:
        shell.configurables.append(self)
    
    @line_magic
    def msg(self, line):
        print(self.message)

def load_ipython_extension(ip):
    ip.magics_manager.register(MsgMagic)
