#!/usr/bin/env python

import json
import matplotlib.pyplot as plt
import matplotlib
import sys
import numpy as np
import scienceplots
import latexipy as lp

plt.style.use(['science','scatter','ieee'])

#Get first argument
filename = "/scratch/bern/elferich/ER_HoxB8_96h/Assets/CTF/CF4-g1_00008_-20.0_9_0_CTF_1_debug_thickness.json"
with open(filename) as f:
    s = f.read()
    s = s.replace('nan', '0.0')
    data = json.loads(s)

# Create two plots

with lp.figure(f"ctfnode_bruteforce1",tight_layout=False):

    fig = plt.figure()
    ax = plt.axes()


    # PLot the output of the 1D search in ax 3
    all_values = np.array(data['1D_brute_force_search']['all_values']).reshape(-1, 2)
    Xs = all_values[:,0].reshape(-1,351)
    np.set_printoptions(threshold=sys.maxsize)
    Ys = all_values[:,1].reshape(-1,351)
    all_scores = np.array(data['1D_brute_force_search']['all_scores']).reshape(1,-1)
    Zs = - all_scores.reshape(-1,351)
    a= ax.contourf(Xs, Ys, Zs, 50, cmap='viridis',)
    cbar = plt.colorbar(a)
    cbar.set_label('Score')
    ax.contour(Xs, Ys, Zs, 50, colors='black', linewidths=0.3)
    ax.set_xlabel('Thickness (Å)')
    ax.set_ylabel('Defocus (Å)')
    # Add colorbar legend
    


