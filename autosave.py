"""Extension for managing periodic autosave of IPython notebooks

Usage:

%load_ext autosave

# autosave every 30 seconds:
%autosave 30

# disable autosave:
%autosave 0

# invoke save from Python:
%savenb

"""

from IPython.core.magic import magics_class, line_magic, Magics
from IPython.display import Javascript, display

_autosave_js_t = """
IPython.autosave_extension_interval = %i;

IPython.autosave_extension_schedule = function() {
    var interval = IPython.autosave_extension_interval;
    console.log(interval);
    if (interval) {
        IPython.notebook.save_notebook();
        setTimeout(IPython.autosave_extension_schedule, interval);
    } else {
        console.log("autosave disabled");
    }
};

IPython.autosave_extension_schedule();
"""

@magics_class
class AutoSaveMagics(Magics):
    
    interval = 60
    enabled = True
    
    @staticmethod
    def autosave_js(interval):
        if interval:
            print("autosaving every %is" % interval)
        else:
            print("autosave disabled")
        display(Javascript(_autosave_js_t % (1000 * interval)))
    
    @line_magic
    def autosave(self, line):
        """Schedule notebook autosave
        
        Usage:
        
            %autosave [interval]
        
        If `interval` is given, IPython will autosave the notebook every `interval` seconds.
        If `interval` is 0, autosave is disabled.
        
        If no interval is specified, autosave is toggled.
        """
        line = line.strip()
        if not line:
            # empty line, toggle
            self.enabled = bool(1 - self.enabled)
        else:
            interval = int(line)
            if interval:
                self.enabled = True
                self.interval = interval
            else:
                self.enabled = False
        
        self.autosave_js(self.enabled * self.interval)
    
    @line_magic
    def savenb(self, line):
        """save the current notebook
        
        This magic invokes the same javascript as the 'Save' button in the notebook UI.
        """
        display(Javascript("IPython.notebook.save_notebook();"))

_loaded = False

def load_ipython_extension(ip):
    """Load the extension in IPython."""
    global _loaded
    if not _loaded:
        ip.register_magics(AutoSaveMagics)
        _loaded = True
    # start initial autosave
    AutoSaveMagics.autosave_js(AutoSaveMagics.interval)
            