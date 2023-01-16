#!/usr/bin/env python

import json
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import glob
from pathlib import Path
import scienceplots
import latexipy as lp

plt.style.use(['science','scatter','ieee'])

dataset=Path(__file__).parent.parent.parent / "data/tilt_brute_force/s_tiltseries04_00023_13.0_Oct28_14.05.56_24_0_CTF_1_debug__tilt.json"



with open(dataset) as f:
    data = json.load(f)
tilt = float(str(dataset).split('_')[-10])
with lp.figure(f"ctftilt_bruteforce",tight_layout=False):

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    axis, angle, score =  zip(*data["tilt_axis_and_angle_search"])
    score = np.array(score).reshape(13, 36)
    axis = np.array(axis).reshape(13, 36)
    angle = np.array(angle).reshape(13, 36)

    # Plot "initial_fit" in ax1
    norm = plt.Normalize(score.min(), score.max())
    colors = cm.viridis(norm(score)*0.9)
    rcount, ccount, _ = colors.shape
    surf = ax.plot_surface(axis, angle, score, rcount=rcount, ccount=ccount,
                       facecolors=colors, shade=False,linewidth=0.5, antialiased=True)
    surf.set_facecolor((0,0,0,0))
    ax.tick_params(axis='x', which='major', pad=-5)
    ax.tick_params(axis='y', which='major', pad=-5)
    ax.tick_params(axis='z', which='major', pad=-1)
   
    ax.set_xlabel('Axis angle [°]',labelpad=-10)
    ax.set_ylabel('Tilt angle [°]',labelpad=-10)
    ax.set_zlabel('Score',labelpad=-2,rotation=90)


    ax.view_init(elev=30., azim=-30.)

    #ax.set_title(f"Tilt {tilt:.1f}")


