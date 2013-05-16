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
import urllib2

from IPython.display import display_html, display_javascript

here = os.path.abspath(os.path.dirname(__file__))

def download_if_missing(fname):
    dest = os.path.join(here, fname)
    if os.path.exists(dest):
        return
    url = 'https://raw.github.com/minrk/ipython_extensions/master/' + fname
    print("Downloading %s to %s" % (url, dest))
    
    filein  = urllib2.urlopen(url)
    fileout = open(dest, "wb")
    chunk = filein.read(1024)
    while chunk:
        fileout.write(chunk)
        chunk = filein.read(1024)
    filein.close()
    fileout.close()

download_if_missing('nbtoc.js')
with io.open(os.path.join(here, 'nbtoc.js')) as f:
    toc_js = f.read()

download_if_missing('nbtoc.html')
with io.open(os.path.join(here, 'nbtoc.html')) as f:
    toc_html = f.read()

def nbtoc(line):
    display_html(toc_html, raw=True)
    display_javascript(toc_js, raw=True)

def load_ipython_extension(ip):
    ip.magics_manager.register_function(nbtoc)
