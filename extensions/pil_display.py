"""
PNG formatter for PIL Image objects

Usage:  %load_ext pil_display

Now when displayhook gets an image, it will be drawn in the browser.

"""

from io import BytesIO

def display_image(img, format='PNG'):
    fp = BytesIO()
    img.save(fp, format=format)
    return fp.getvalue()

def register_pil_formatter(ip):
    png_formatter = ip.display_formatter.formatters['image/png']
    # both, in case of pillow or true PIL
    png_formatter.for_type_by_name('PIL.Image', 'Image', display_image)
    png_formatter.for_type_by_name('Image', 'Image', display_image)
    print png_formatter

def load_ipython_extension(ip):
    register_pil_formatter(ip)
