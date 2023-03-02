import json
import numpy as np
import latexipy as lp
from pathlib import Path
import scienceplots
import matplotlib.pyplot as plt
import mrcfile

plt.style.use(['science','scatter','ieee'])


json_file = "/scratch/bern/elferich/ER_HoxB8_96h/Assets/CTF/CF4-g1_00002_-20.0_3_0_CTF_3_debug__tilt.json"
image_file = "/scratch/bern/elferich/ER_HoxB8_96h/Assets/Images/CF4-g1_00002_-20.0_3_0.mrc"



# 
# PREPARE the image
#

mrc = mrcfile.open(image_file)


im = mrc.data[0].copy()


#im = downscale_image(im_data, 0.25)

mean = im.mean()
std = im.std()
im[im > mean + 1 * std] = mean + 1 * std
im[im < mean - 1 * std] = mean - 1 * std
im -= im.min()
im /= im.max()
im *= 255

#
# Get the tile data
#
tilt_binning_factor = 9.433963 /  2.83
with open(json_file) as f:
    data = json.load(f)
with lp.figure(f"tilt_search",tight_layout=False):
    plt.imshow(im, cmap='gray',vmin=0,vmax=255)
    for i, subregion in enumerate(data["search_tiles"]):
        # Plot rectangle
        x, y, w, h = subregion["x"]*tilt_binning_factor, subregion["y"]*tilt_binning_factor, subregion["width"]*tilt_binning_factor, subregion["height"]*tilt_binning_factor
        # Add jitter to avoid overlapping rectangles
        x += im.shape[1]/2
        y += im.shape[0]/2
        x -= w/2
        y -= h/2
        #x += 0.03 * y
        #y += 0.03 * x
        print(x,y,w,h)
        # Choose a random color
        if i == 0:
            plt.gca().add_patch(plt.Rectangle((x, y), w, h, fill=False, edgecolor="white", linewidth=0.7))
            plt.gca().add_patch(plt.Rectangle((x, y), w, h, fill=False, edgecolor="black", linewidth=0.2))
        # Place a cross at x,y, with a cross marker
        plt.plot(x+w/2, y+h/2, 'x', color="white", markersize=0.9)
        plt.plot(x+w/2, y+h/2, 'x', color="black", markersize=0.5)
        #plt.gca().add_patch(plt.Rectangle((-1353, -1353), 1000, 1000, fill=False, edgecolor=color, linewidth=0.5))
        plt.xlim(-1000, im.shape[1]+1000)
        plt.ylim( im.shape[0]+1000, -1000)
        plt.axis('off')