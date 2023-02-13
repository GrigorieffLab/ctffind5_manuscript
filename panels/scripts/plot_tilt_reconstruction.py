import json
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import glob
from pathlib import Path
import scienceplots
import latexipy as lp
import pandas as pd
import sqlite3
from pycistem import database
import mrcfile

#Disable logger
import logging
logging.disable(logging.CRITICAL)


plt.style.use(['science','ieee'])

# Open the .txt file

classic_ctf = {}
with open("/scratch/bern/elferich/ER_HoxB8_96h/Assets/CTF/CF4-g1_00002_-20.0_3_0_CTF_2_avrot.txt") as f:
    for i, line in enumerate(f):
        if i == 5:
            classic_ctf["spatial_freq"] = np.array(line.split()[1:], dtype=float)
        if i == 7:
            classic_ctf["epa"] = np.array(line.split()[1:], dtype=float)
        if i == 8:
            classic_ctf["model"] = np.array(line.split()[1:], dtype=float)
        if i == 9:
            classic_ctf["quality_score"] = np.array(line.split()[1:], dtype=float)

classic_ctf["spatial_freq"] = 1/classic_ctf["spatial_freq"]

# Open the .txt file
tilt_ctf = {}
with open("/scratch/bern/elferich/ER_HoxB8_96h/Assets/CTF/CF4-g1_00002_-20.0_3_0_CTF_6_avrot.txt") as f:
    for i, line in enumerate(f):
        if i == 5:
            tilt_ctf["spatial_freq"] = np.array(line.split()[1:], dtype=float)
        if i == 7:
            tilt_ctf["epa"] = np.array(line.split()[1:], dtype=float)
        if i == 8:
            tilt_ctf["model"] = np.array(line.split()[1:], dtype=float)
        if i == 9:
            tilt_ctf["quality_score"] = np.array(line.split()[1:], dtype=float)

tilt_ctf["spatial_freq"] = 1/tilt_ctf["spatial_freq"]


info_image = database.get_image_info_from_db("/scratch/bern/elferich/ER_HoxB8_96h/ER_HoxB8_96h.db",2)
con = sqlite3.connect("/scratch/bern/elferich/ER_HoxB8_96h/ER_HoxB8_96h.db")
info_tilt_ctf = pd.read_sql(f"SELECT * FROM ESTIMATED_CTF_PARAMETERS WHERE CTF_ESTIMATION_ID = 571", con).iloc[0]
info_ctffind4_ctf = pd.read_sql(f"SELECT * FROM ESTIMATED_CTF_PARAMETERS WHERE CTF_ESTIMATION_ID = 381", con).iloc[0]

with lp.figure(f"tilt_correction_example",tight_layout=False):
    fig, [ax_classic,ax_tilt] = plt.subplots(2,1,sharex=True, sharey=True)
   
    ax_classic.plot(classic_ctf["spatial_freq"], classic_ctf["epa"], label="EPA")
    ax_classic.plot(classic_ctf["spatial_freq"], classic_ctf["model"], label="Model")
    ax_classic.plot(classic_ctf["spatial_freq"], classic_ctf["quality_score"], label="Fit quality")
    ax_tilt.plot(tilt_ctf["spatial_freq"], tilt_ctf["epa"], label="EPA")
    ax_tilt.plot(tilt_ctf["spatial_freq"], tilt_ctf["model"], label="Model")
    ax_tilt.plot(tilt_ctf["spatial_freq"], tilt_ctf["quality_score"], label="Fit quality")

    ax_tilt.set_xlabel("Spatial Resolution (Å)")
    ax_tilt.set_ylabel("Value")
    ax_classic.set_ylabel("Value")
    ax_tilt.set_xscale("log")
    ax_classic.set_xscale("log")
    ax_tilt.set_xlim(15,2.5)
    ax_tilt.set_xticks([12, 10, 8, 6, 4, 3])
    ax_tilt.set_xticklabels([12, 10, 8, 6, 4, 3])

    ax_classic.set_ylim(-0.1,1.05)
    ax_tilt.set_ylim(-0.1,1.05)

    # Set space between subplots
    fig.subplots_adjust(hspace=0.05)
