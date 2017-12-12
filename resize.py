
# coding: utf-8

import os, sys
from PIL import Image

#resize shortside to the desire value while remain ratio
def ratio_resize (longside, shortside, desire_value): 
    long_side_precent = (desire_value/float(shortside))
    longside = int(float(longside)*long_side_precent)
    return longside

# run the ratio_resize and then crop the longside to the desired value 
def ratio_cropping (image, desire_value):
    if image.size[0] > image.size[1]:
        image = image.resize((ratio_resize(image.size[0], image.size[1], desire_value),desire_value), Image.ANTIALIAS)
        image = image.crop(((image.size[0]/2 - desire_value/2),0,(image.size[0]/2 + desire_value/2),desire_value))
    elif image.size[0] < image.size[1]:
        image = image.resize((desire_value, ratio_resize(image.size[1], image.size[0], desire_value)), Image.ANTIALIAS)
        image = image.crop((0,(image.size[1]/2 - desire_value/2),desire_value,(image.size[1]/2 + desire_value/2)))
    else: 
        image = image.resize((desire_value,desire_value))
    return image

# loop through current directory and save the resize image to "resize" folder (need to create in advance)

def image_resize(imagedir, desire_value):
    try:
        im = Image.open(imagedir)
        im.load()
        im = ratio_cropping(im, desire_value)
        return im
    except IOError:
        print "cannot resize'%s'" % imagedir
