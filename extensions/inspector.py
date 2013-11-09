import inspect
import linecache
import os
import sys

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

from IPython.core.magic import Magics, magics_class, line_magic

from IPython.display import display, HTML

@magics_class
class InspectorMagics(Magics):
    
    def __init__(self, **kwargs):
        super(InspectorMagics, self).__init__(**kwargs)
        self.formatter = HtmlFormatter()
        self.lexer = PythonLexer()
        self.style_name = "default"
    
    @line_magic
    def showsrc(self, line):
        line = line.strip()
        filename, identifier = line.rsplit(None, 1)
        modname, ext = os.path.splitext(filename)
        mod = __import__(modname)
        reload(mod)
        linecache.checkcache()
        obj = getattr(mod, identifier)
        lines, lineno = inspect.getsourcelines(obj)
        self.formatter.linenos = True
        self.formatter.linenostart = lineno
        html = "<span class='inspector-header'>"
        html += "<span class='inspector-filename'>%s: </span>" % filename
        html += "<span class='inspector-lineno'>%i-%i</span>" % (lineno, lineno + len(lines))
        html += "</span>"
        html += highlight(''.join(lines), self.lexer, self.formatter)
        display(HTML(html))
    
    @line_magic
    def showsrcstyle(self, line):
        """publish the CSS for highlighting used in %showsrc
        
        Takes a """
        
        name = line.strip()
        if not name:
            name = "default"
        self.style_name = name
        self.formatter = HtmlFormatter(style=name)
        display(HTML("""<style type='text/css'>
        span.inspector-header {
            font-family: monospace;
            border-bottom: 1px solid #555;
        }
        table.highlighttable, .highlighttable td, .highlighttable tr {
            border: 0px;
        }
        .highlighttable td.linenos {
            border-right: 1px solid #555;
        }
        
        span.inspector-filename {
            text-decoration: italic;
        }
        span.inspector-lineno {
            font-weight: bold;
        }
        %s
        </style>
        """ % self.formatter.get_style_defs()
        ))

def load_ipython_extension(ip):
    ip.register_magics(InspectorMagics)
    ip.magic("showsrcstyle")
