"""Extension for managing periodic autosave of IPython notebooks

THIS EXTENSION IS OBSOLETE, IPYTHON 1.0 SUPPORTS AUTOSAVE

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

// clear previous interval, if there was one
if (IPython.autosave_extension_interval) {{
    clearInterval(IPython.autosave_extension_interval);
    IPython.autosave_extension_interval = null;
}}

// set new interval
if ({0}) {{
    console.log("scheduling autosave every {0} ms");
    IPython.notebook.save_notebook();
    IPython.autosave_extension_interval = setInterval(function() {{
        console.log("autosave");
        IPython.notebook.save_notebook();
    }}, {0});
}} else {{
    console.log("canceling autosave");
}}
"""

@magics_class
class AutoSaveMagics(Magics):
    
    interval = 60
    enabled = False
    
    @staticmethod
    def autosave_js(interval):
        if interval:
            print("autosaving every %is" % interval)
        else:
            print("autosave disabled")
        display(Javascript(_autosave_js_t.format(1000 * interval)))
    
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

def load_ipython_extension(ip):
    """Load the extension in IPython."""
    if "autosave" in ip.magics_manager.magics['line']:
        print ("IPython 1.0 has autosave, this extension is obsolete")
        return
    ip.register_magics(AutoSaveMagics)
    print ("Usage: %autosave [seconds]")

