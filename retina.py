"""
Enable Retina (2x) PNG figures with matplotlib

Usage:  %load_ext retina
"""

import struct
from base64 import encodestring

import matplotlib
from matplotlib.figure import Figure

from IPython.core.pylabtools import print_figure

def pngxy(data):
    """read the width/height from a PNG header"""
    ihdr = data.index(b'IHDR')
    # next 8 bytes are width/height
    w4h4 = data[ihdr+4:ihdr+12]
    return struct.unpack('>ii', w4h4)

def png2x(fig):
    """render figure to 2x PNG via HTML"""
    pngbytes = print_figure(fig, 'png')
    x,y = pngxy(pngbytes)
    x2x = x // 2
    y2x = y // 2
    png64 = encodestring(pngbytes).decode('ascii')
    return u"<img src='data:image/png;base64,%s' width=%i height=%i/>" % (png64, x2x, y2x)
    
def enable_retina(ip):
    """enable retina figures"""
    # double DPI, so we don't end up changing the figure size
    matplotlib.rcParams['savefig.dpi'] = 2 * matplotlib.rcParams['savefig.dpi']
    
    # unregister existing formatter(s):
    png_formatter = ip.display_formatter.formatters['image/png']
    png_formatter.type_printers.pop(Figure, None)
    svg_formatter = ip.display_formatter.formatters['image/svg+xml']
    svg_formatter.type_printers.pop(Figure, None)
    
    # register png2x as HTML formatter
    html_formatter = ip.display_formatter.formatters['text/html']
    html_formatter.for_type(matplotlib.figure.Figure, png2x)
    

# load the extension:
loaded = False

def load_ipython_extension(ip):
    global loaded
    if loaded:
        # avoid
        return
    loaded = True
    enable_retina(ip)
