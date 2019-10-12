#Import necessary libraries
import random
from math import pi
from PIL import Image
from numpy import squeeze
from bokeh.models import HoverTool
from bokeh.embed import components
from bokeh.plotting import figure

ALLOWED_EXTENSIONS = set(['png', 'bmp', 'jpg', 'jpeg', 'gif'])
                
def is_allowed_file(filename):
    """ Checks if a filename's extension is acceptable """
    allowed_ext = filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return '.' in filename and allowed_ext

def make_thumbnail(filepath):
    """ Converts input image to 64px by 64px thumbnail if not that size """
    img = Image.open(filepath)
    thumb = None
    w, h = img.size

    # if the width and height are equal, scale down
    if w == h:
        thumb = img.resize((64, 64), Image.BICUBIC)
        thumb.save(filepath)
        return True

    # when the image's width is smaller than the height
    if w < h:
        # scale so that the width is 64
        ratio = w / 64.
        w_new, h_new = 64, int(h / ratio)
        thumb = img.resize((w_new, h_new), Image.BICUBIC)

        # crop the excess
        top, bottom = 0, 0
        margin = h_new - 64
        top, bottom = margin // 2, 64 + margin // 2
        box = (0, top, 64, bottom)
        cropped = thumb.crop(box)
        cropped.save(filepath)
        return True

    # when the image's height is smaller than the width
    if h < w:
        # scale so that the height is 64
        ratio = h / 64.
        w_new, h_new = int(w / ratio), 64
        thumb = img.resize((w_new, h_new), Image.BICUBIC)

        # crop the excess
        left, right = 0, 0
        margin = w_new - 64
        left, right = margin // 2, 64 + margin // 2
        box = (left, 0, right, 64)
        cropped = thumb.crop(box)
        cropped.save(filepath)
        return True
    return False
