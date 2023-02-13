import json
import numpy as np
import latexipy as lp
from pathlib import Path
import scienceplots
import matplotlib.pyplot as plt
import mrcfile
import pycistem

import logging
logging.disable(logging.CRITICAL)

plt.style.use(['science','scatter','ieee'])

image = pycistem.core.Image()
image.Allocate(512,512,1)
image.ForwardFFT(True)
image.SetToConstant(1.0)

ctf = pycistem.core.CTF(300,2.7,0.07,5000,5000,pixel_size=2.0)

image.ApplyCTF(ctf,True,False,False)

powerspectrum = pycistem.core.Image()
powerspectrum.Allocate(512,512,1)
image.ComputeAmplitudeSpectrumFull2D(powerspectrum, False, 0.0)


with lp.figure(f"tilt_search_explanation",tight_layout=False):
    # Generate 9 x9 subplots with plots wihtout touching each other and withotu
    # axes, but with boxes
    num_sections = 5
    overall_dim = num_sections * 512 + (num_sections + 1) * 100
    overall = np.zeros((overall_dim,overall_dim)) + 1.4
    #fig, ax = plt.subplots(5,5,sharex=True,sharey=True,figsize=(5.5,4.5))
    tilt_axis_angle = np.deg2rad(20)
    average_defocus = 5000
    for i in range(num_sections**2):
        x = i//num_sections 
        y = i%num_sections 
        x_center = x + 0.5 - num_sections/2
        y_center = y + 0.5 - num_sections/2
        print(x_center,y_center)
        # Rotate (x_center,y_center) by tilt_axis_angle
        x_rotated = x_center*np.cos(tilt_axis_angle) - y_center*np.sin(tilt_axis_angle)
        y_rotated = x_center*np.sin(tilt_axis_angle) + y_center*np.cos(tilt_axis_angle)
        defocus = average_defocus + 800*y_rotated

        image.SetToConstant(1.0)


        ctf = pycistem.core.CTF(300,2.7,0.07,defocus,defocus,pixel_size=2.0)
        image.ApplyCTF(ctf,True,False,False)
        image.ComputeAmplitudeSpectrumFull2D(powerspectrum, False, 0.0)
        data = powerspectrum.real_values.copy()
        # Add lowpass filtered guassian noise to the left half of the image
        # data[:,:256] += np.random.normal(0,0.5,data[:,:256].shape)
        # Add a black border around the image
        data = np.pad(data,((5,5),(5,5)),mode="constant",constant_values=0.0)
        overall[x*512 + (x+1)*100:(x+1)*512 + (x+1)*100+10,y*512 + (y+1)*100:(y+1)*512 + (y+1)*100+10] = data
    fig, axes = plt.subplots(1,2,figsize=(6.5,4.5))
    axes[0].imshow(overall,cmap="gray",vmin=0,vmax=1.4)
    # Draw the axis as a dashed line through the center at the tilt angle
    axes[0].plot([overall_dim/2,overall_dim/2 + overall_dim*np.sin(-tilt_axis_angle)],[overall_dim/2,overall_dim/2 + overall_dim*np.cos(-tilt_axis_angle)],"k--")
    axes[0].plot([overall_dim/2,overall_dim/2 - overall_dim*np.sin(-tilt_axis_angle)],[overall_dim/2,overall_dim/2 - overall_dim*np.cos(-tilt_axis_angle)],"k--")
    axes[0].set_xlim(0,overall_dim)
    axes[0].set_ylim(0,overall_dim)
    axes[0].axis("off")

    # Do the overlay figure



    overlay = np.zeros((1024,1024)) + 0.72


    # Higher defocus

    higher_defocus = average_defocus + 800 * np.sqrt(8)
    zoom_factor = np.sqrt(higher_defocus/average_defocus)
    box_size = int(512*zoom_factor)
    image = pycistem.core.Image()
    image.Allocate(box_size,box_size,True)
    image.ForwardFFT(True)
    image.SetToConstant(1.0)

    ctf = pycistem.core.CTF(300,2.7,0.07,higher_defocus,higher_defocus,pixel_size=2.0)

    image.ApplyCTF(ctf,True,False,False)

    powerspectrum = pycistem.core.Image()
    powerspectrum.Allocate(box_size,box_size,True)
    image.ComputeAmplitudeSpectrumFull2D(powerspectrum, False, 0.0)
    pad = int((1024 - box_size)/2)
    overlay[pad:pad+box_size,pad:pad+box_size] = (powerspectrum.real_values.copy() - np.sqrt(2)/2) * 1/3

    # normal defocus

    zoom_factor = 1.0
    box_size = int(512*zoom_factor)
    image = pycistem.core.Image()
    image.Allocate(box_size,box_size,True)
    image.ForwardFFT(True)
    image.SetToConstant(1.0)

    ctf = pycistem.core.CTF(300,2.7,0.07,average_defocus,average_defocus,pixel_size=2.0)

    image.ApplyCTF(ctf,True,False,False)

    powerspectrum = pycistem.core.Image()
    powerspectrum.Allocate(box_size,box_size,True)
    image.ComputeAmplitudeSpectrumFull2D(powerspectrum, False, 0.0)
    pad = int((1024 - box_size)/2)
    overlay[pad:pad+box_size,pad:pad+box_size] += (powerspectrum.real_values.copy() - np.sqrt(2)/2) * 1/3

# Lower defocus

    lower_defocus = average_defocus - 800 * np.sqrt(8)
    zoom_factor = np.sqrt(lower_defocus/average_defocus)
    box_size = int(512*zoom_factor)
    image = pycistem.core.Image()
    image.Allocate(box_size,box_size,True)
    image.ForwardFFT(True)
    image.SetToConstant(1.0)

    ctf = pycistem.core.CTF(300,2.7,0.07,lower_defocus,lower_defocus,pixel_size=2.0)

    image.ApplyCTF(ctf,True,False,False)

    powerspectrum = pycistem.core.Image()
    powerspectrum.Allocate(box_size,box_size,True)
    image.ComputeAmplitudeSpectrumFull2D(powerspectrum, False, 0.0)
    pad = int((1024 - box_size)/2)
    overlay[pad:pad+box_size,pad:pad+box_size] += (powerspectrum.real_values.copy() - np.sqrt(2)/2) * 1/3


    axes[1].imshow(overlay,cmap="gray")
    axes[1].set_xlim(0,1024)
    axes[1].set_ylim(0,1024)
    axes[1].axis("off")



    

    