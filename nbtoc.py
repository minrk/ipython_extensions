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

if not os.path.isfile(os.path.join(here, 'nbtoc.js')) or not os.path.isfile(os.path.join(here, 'nbtoc.js')):
    import urllib2
    def download(url, fout):
        """ Saves the url file to fout filename """
        filein  = urllib2.urlopen(url)
        fileout = open(fout, "wb")

        while True:
            bytes = filein.read(1*1024) # 1*1024bytes
            fileout.write(bytes)

            if bytes == "": break

        filein.close()
        fileout.close()

    download('https://raw.github.com/minrk/ipython_extensions/master/nbtoc.js', os.path.join(here, 'nbtoc.js'))
    download('https://raw.github.com/minrk/ipython_extensions/master/nbtoc.html', os.path.join(here, 'nbtoc.html'))

with io.open(os.path.join(here, 'nbtoc.js')) as f:
    toc_js = f.read()

with io.open(os.path.join(here, 'nbtoc.html')) as f:
    toc_html = f.read()

def nbtoc(line):
    display_html(toc_html, raw=True)
    display_javascript(toc_js, raw=True)

def load_ipython_extension(ip):
    ip.magics_manager.register_function(nbtoc)
