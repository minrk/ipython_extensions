"""Table-of-contents magic
for IPython Notebook

Just do:

%load_ext nbtoc
%nbtoc

to get a floating table of contents

All the interesting code, c/o @magican and @nonamenix:
https://gist.github.com/magican/5574556

"""

import io
import os

from IPython.display import display_html, display_javascript

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'nbtoc.js')) as f:
    toc_js = f.read()

with io.open(os.path.join(here, 'nbtoc.html')) as f:
    toc_html = f.read()

def nbtoc(line):
    display_html(toc_html, raw=True)
    display_javascript(toc_js, raw=True)

def load_ipython_extension(ip):
    ip.magics_manager.register_function(nbtoc)
