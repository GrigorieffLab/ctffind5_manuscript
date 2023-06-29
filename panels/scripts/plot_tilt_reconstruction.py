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
from matplotlib.offsetbox import AnchoredText

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
    fig, ax_dict = plt.subplot_mosaic([['classic']],
                                  sharex=True,sharey=True,gridspec_kw={"width_ratios":[1.0]},figsize=(3.5,1.5))
    ax_classic = ax_dict["classic"]
    ax_tilt = ax_dict["classic"]
    #ax_dict["BLANK"].axis("off")
    ax_tilt.plot(tilt_ctf["spatial_freq"], tilt_ctf["epa"], label="Power spectrum")
    ax_tilt.plot(tilt_ctf["spatial_freq"], tilt_ctf["quality_score"], label="Fit quality",linestyle="--", color="black")

    ax_classic.plot(classic_ctf["spatial_freq"], classic_ctf["epa"], label="EPA", linestyle="-", color="deepskyblue")
    #ax_classic.plot(classic_ctf["spatial_freq"], classic_ctf["model"], label="Model")
    ax_classic.plot(classic_ctf["spatial_freq"], classic_ctf["quality_score"], label="Fit quality",linestyle="--", color="deepskyblue")
    
    ax_tilt.set_xlabel("Spatial Resolution (Å)")
    ax_classic.set_ylabel("Value")
    ax_classic.set_xscale("log")
    ax_tilt.set_xlim(15,4.0)
    ax_classic.set_xlim(15,4.0)
    ax_tilt.set_xticks([12, 10, 8, 6, 4])
    ax_tilt.set_xticklabels([12, 10, 8, 6, 4])

    ax_classic.set_ylim(-0.1,1.05)
    ax_tilt.set_ylim(-0.1,1.05)

    #text_classic = AnchoredText(
    print(f"\\underline{{Parameters:}}\nDefocus 1: {int(info_ctffind4_ctf['DEFOCUS1'])}Å\nDefocus 2: {int(info_ctffind4_ctf['DEFOCUS2'])}Å\nAstig. angle : {info_ctffind4_ctf['DEFOCUS_ANGLE']:.1f}°\n\\underline{{Fit resolution:}} {info_ctffind4_ctf['DETECTED_RING_RESOLUTION']:.1f}Å")
    #info_classic.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    #ax_dict["BLANK"].add_artist(text_classic)
    #text_tilt = AnchoredText(
    print(f"\\underline{{Parameters:}}\nDefocus 1: {int(info_tilt_ctf['DEFOCUS1'])}Å\nDefocus 2: {int(info_tilt_ctf['DEFOCUS2'])}Å\nAstig. angle : {info_tilt_ctf['DEFOCUS_ANGLE']:.1f}°\nTilt axis angle: {info_tilt_ctf['TILT_AXIS']:.1f}°\nTilt angle: {info_tilt_ctf['TILT_ANGLE']:.1f}°\n\\underline{{Fit resolution:}} {info_tilt_ctf['DETECTED_RING_RESOLUTION']:.1f}Å")
    #info_tilt.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    #ax_dict["BLANK"].add_artist(text_tilt)

    # Set space between subplots
    #fig.subplots_adjust(hspace=0.05)
    #plt.tight_layout()
