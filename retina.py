"""
Enable Retina (2x) PNG figures with matplotlib

Usage:  %load_ext retina
"""

import struct
from base64 import encodestring
from io import BytesIO

def pngxy(data):
    """read the width/height from a PNG header"""
    ihdr = data.index(b'IHDR')
    # next 8 bytes are width/height
    w4h4 = data[ihdr+4:ihdr+12]
    return struct.unpack('>ii', w4h4)

def print_figure(fig, fmt='png', dpi=None):
    """Convert a figure to svg or png for inline display."""
    import matplotlib
    fc = fig.get_facecolor()
    ec = fig.get_edgecolor()
    bytes_io = BytesIO()
    dpi = dpi or matplotlib.rcParams['savefig.dpi']
    fig.canvas.print_figure(bytes_io, format=fmt, dpi=dpi,
                            bbox_inches='tight',
                            facecolor=fc, edgecolor=ec,
    )
    data = bytes_io.getvalue()
    return data

def png2x(fig):
    """render figure to 2x PNG via HTML"""
    import matplotlib
    if not fig.axes and not fig.lines:
        return
    # double DPI
    dpi = 2 * matplotlib.rcParams['savefig.dpi']
    pngbytes = print_figure(fig, fmt='png', dpi=dpi)
    x,y = pngxy(pngbytes)
    x2x = x // 2
    y2x = y // 2
    png64 = encodestring(pngbytes).decode('ascii')
    return u"<img src='data:image/png;base64,%s' width=%i height=%i/>" % (png64, x2x, y2x)

def enable_retina(ip):
    """enable retina figures"""
    from matplotlib.figure import Figure

    
    # unregister existing formatter(s):
    png_formatter = ip.display_formatter.formatters['image/png']
    png_formatter.type_printers.pop(Figure, None)
    svg_formatter = ip.display_formatter.formatters['image/svg+xml']
    svg_formatter.type_printers.pop(Figure, None)
    
    # register png2x as HTML formatter
    html_formatter = ip.display_formatter.formatters['text/html']
    html_formatter.for_type(Figure, png2x)
    

# load the extension:
loaded = False

def load_ipython_extension(ip):
    global loaded
    if loaded:
        return
    loaded = True
    try:
        enable_retina(ip)
    except Exception as e:
        print "Failed to load retina extension: %s" % e

