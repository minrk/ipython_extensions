"""
PNG formatter for various Image objects (PIL, OpenCV, numpy arrays that look like image data)

Usage:  %load_ext pil_display

Now when displayhook gets an image, it will be drawn in the browser.

"""

from io import BytesIO
import os
import tempfile

def pil2imgdata(img, format='PNG'):
    """convert a PIL Image to png bytes"""
    fp = BytesIO()
    img.save(fp, format=format)
    return fp.getvalue()

def array2imgdata_pil(A, format='PNG'):
    """get png data from array via converting to PIL Image"""
    from PIL import Image
    img = Image.fromstring("L", A.shape[:2], A.tostring())
    return pil2imgdata(img, format)

def array2imgdata_fs(A, format='PNG'):
    """get png data via filesystem, using cv2.imwrite
    
    This is much faster than in-memory conversion with PIL on the rPi for some reason.
    """
    import cv2
    fname = os.path.join(tempfile.gettempdir(), "_ipdisplay.%s" % format)
    cv2.imwrite(fname, A)
    with open(fname) as f:
        data = f.read()
    os.unlink(fname)
    return data

def display_image_array(a):
    """If an array looks like RGB[A] data, display it as an image."""
    import numpy as np
    if len(a.shape) != 3 or a.shape[2] not in {3,4} or a.dtype != np.uint8:
        return
    return array2imgdata_pil(a)

def display_cv_image(cvimg):
    """display an OpenCV cvmat object as an image"""
    import numpy as np
    return array2imgdata_fs(np.asarray(cvimg))

def register_image_formatters(ip):
    png_formatter = ip.display_formatter.formatters['image/png']
    # both, in case of pillow or true PIL
    png_formatter.for_type_by_name('PIL.Image', 'Image', pil2imgdata)
    png_formatter.for_type_by_name('Image', 'Image', pil2imgdata)
    png_formatter.for_type_by_name('cv2.cv', 'iplimage', display_cv_image)
    png_formatter.for_type_by_name('cv2.cv', 'cvmat', display_cv_image)
    png_formatter.for_type_by_name("numpy", "ndarray", display_image_array)