import json
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import glob
from pathlib import Path
import scienceplots
import latexipy as lp

plt.style.use(['science','ieee'])

# Open the .txt file
with open(Path(__file__).parent.parent.parent / "data/mmm/mmm/Assets/CTF/mmm_CTF_0_avrot.txt") as f:
    for i, line in enumerate(f):
        if i == 5:
            spatial_freq = np.array(line.split()[1:], dtype=float)
        if i == 7:
            epa = np.array(line.split()[1:], dtype=float)
        if i == 8:
            model = np.array(line.split()[1:], dtype=float)
        if i == 9:
            quality_score = np.array(line.split()[1:], dtype=float)

spatial_freq = 1/spatial_freq
with lp.figure(f"mmm_ctffind",tight_layout=False):
    plt.plot(spatial_freq, epa, label="EPA")
    plt.plot(spatial_freq, model, label="Model")
    plt.plot(spatial_freq, quality_score, label="Fit quality")
    # Put legend bottom left
    plt.legend(loc="lower left")
    plt.xlabel("Spatial Frequency (Å)")
    plt.ylabel("Value")
    # Set X axis to log
    plt.xscale("log")
    # Set X axis labels
    plt.xticks([600,400,200,150,100,80,60], ["600","400","200","150","100","80","60"])
    plt.xlim(600, 57)
    plt.ylim(0.01, 1)
    # Set plot ratio
    plt.gca().set_aspect(0.5)


