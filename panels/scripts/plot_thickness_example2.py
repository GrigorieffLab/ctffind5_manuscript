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
with open("/scratch/bern/elferich/ER_HoxB8_96h/Assets/CTF/CF4-g1_00008_-20.0_9_0_CTF_0_avrot.txt") as f:
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
frc_cutoff_ctf = {}
with open("/scratch/bern/elferich/ER_HoxB8_96h/Assets/CTF/CF4-g1_00008_-20.0_9_0_CTF_3_avrot.txt") as f:
    for i, line in enumerate(f):
        if i == 5:
            frc_cutoff_ctf["spatial_freq"] = np.array(line.split()[1:], dtype=float)
        if i == 7:
            frc_cutoff_ctf["epa"] = np.array(line.split()[1:], dtype=float)
        if i == 8:
            frc_cutoff_ctf["model"] = np.array(line.split()[1:], dtype=float)
        if i == 9:
            frc_cutoff_ctf["quality_score"] = np.array(line.split()[1:], dtype=float)

frc_cutoff_ctf["spatial_freq"] = 1/frc_cutoff_ctf["spatial_freq"]


# Open the .txt file
refine_ctf = {}
with open("/scratch/bern/elferich/ER_HoxB8_96h/Assets/CTF/CF4-g1_00008_-20.0_9_0_CTF_1_avrot.txt") as f:
    for i, line in enumerate(f):
        if i == 5:
            refine_ctf["spatial_freq"] = np.array(line.split()[1:], dtype=float)
        if i == 7:
            refine_ctf["epa"] = np.array(line.split()[1:], dtype=float)
        if i == 8:
            refine_ctf["model"] = np.array(line.split()[1:], dtype=float)
        if i == 9:
            refine_ctf["quality_score"] = np.array(line.split()[1:], dtype=float)

refine_ctf["spatial_freq"] = 1/refine_ctf["spatial_freq"]


info_image = database.get_image_info_from_db("/scratch/bern/elferich/ER_HoxB8_96h/ER_HoxB8_96h.db",2)
con = sqlite3.connect("/scratch/bern/elferich/ER_HoxB8_96h/ER_HoxB8_96h.db")
info_frc_cutoff_ctf = pd.read_sql(f"SELECT * FROM ESTIMATED_CTF_PARAMETERS WHERE CTF_ESTIMATION_ID = 575", con).iloc[0]
info_refine_ctf = pd.read_sql(f"SELECT * FROM ESTIMATED_CTF_PARAMETERS WHERE CTF_ESTIMATION_ID = 198", con).iloc[0]

info_tilt_ctf = pd.read_sql(f"SELECT * FROM ESTIMATED_CTF_PARAMETERS WHERE CTF_ESTIMATION_ID = 9", con).iloc[0]

with lp.figure(f"thickness_correction_example2",tight_layout=False):
    fig, ax_dict = plt.subplot_mosaic([['classic', 'BLANK'], ['frc', 'BLANK'], ['refine', 'BLANK']],
                                  sharex=True,sharey=True,gridspec_kw={"width_ratios":[1.5,1.0]},figsize=(9.5,6.5))
    ax_classic = ax_dict["classic"]
    ax_frc = ax_dict["frc"]
    ax_refine = ax_dict["refine"]
    ax_dict["BLANK"].axis("off")
    ax_classic.plot(classic_ctf["spatial_freq"], classic_ctf["epa"], label="EPA")
    ax_classic.plot(classic_ctf["spatial_freq"], classic_ctf["model"], label="Model")
    ax_classic.plot(classic_ctf["spatial_freq"], classic_ctf["quality_score"], label="Fit quality")
    ax_frc.plot(frc_cutoff_ctf["spatial_freq"], frc_cutoff_ctf["epa"], label="EPA")
    ax_frc.plot(frc_cutoff_ctf["spatial_freq"], frc_cutoff_ctf["model"], label="Model")
    ax_frc.plot(frc_cutoff_ctf["spatial_freq"], frc_cutoff_ctf["quality_score"], label="Fit quality")
    ax_refine.plot(refine_ctf["spatial_freq"], refine_ctf["epa"], label="EPA")
    ax_refine.plot(refine_ctf["spatial_freq"], refine_ctf["model"], label="Model")
    ax_refine.plot(refine_ctf["spatial_freq"], refine_ctf["quality_score"], label="Fit quality")

    ax_refine.set_xlabel("Spatial Resolution (Å)")
    ax_frc.set_ylabel("Value")
    ax_refine.set_ylabel("Value")
    ax_classic.set_ylabel("Value")
    ax_frc.set_xscale("log")
    ax_classic.set_xscale("log")
    ax_refine.set_xlim(15,2.5)
    ax_refine.set_xticks([12, 10, 8, 6, 4, 3])
    ax_refine.set_xticklabels([12, 10, 8, 6, 4, 3])

    ax_classic.set_ylim(-0.1,1.05)
    ax_refine.set_ylim(-0.1,1.05)
    ax_frc.set_ylim(-0.1,1.05)

    
    text_tilt = AnchoredText(
    f"\\underline{{Parameters:}}\nDefocus 1: {int(info_tilt_ctf['DEFOCUS1'])}Å\nDefocus 2: {int(info_tilt_ctf['DEFOCUS2'])}Å\nAstig. angle : {info_tilt_ctf['DEFOCUS_ANGLE']:.1f}°\nTilt axis angle: {info_tilt_ctf['TILT_AXIS']:.1f}°\nTilt angle: {info_tilt_ctf['TILT_ANGLE']:.1f}°\n\\underline{{Fit resolution:}} {info_tilt_ctf['DETECTED_RING_RESOLUTION']:.1f}Å", frameon=False,loc='upper left',bbox_to_anchor=(1.05, 0.95), bbox_transform=ax_classic.transAxes, borderpad=0.0)
    #info_tilt.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax_classic.add_artist(text_tilt)

    text_frc = AnchoredText(
    f"\\underline{{Parameters:}}\nDefocus 1: {int(info_frc_cutoff_ctf['DEFOCUS1'])}Å\nDefocus 2: {int(info_frc_cutoff_ctf['DEFOCUS2'])}Å\nAstig. angle : {info_frc_cutoff_ctf['DEFOCUS_ANGLE']:.1f}°\nTilt axis angle: {info_frc_cutoff_ctf['TILT_AXIS']:.1f}°\nTilt angle: {info_frc_cutoff_ctf['TILT_ANGLE']:.1f}°\nSample Thickness: {int(info_frc_cutoff_ctf['SAMPLE_THICKNESS'])}Å\n\\underline{{Fit resolution:}} {info_frc_cutoff_ctf['DETECTED_RING_RESOLUTION']:.1f}Å", frameon=False,loc='upper left',bbox_to_anchor=(1.05, 0.95), bbox_transform=ax_frc.transAxes, borderpad=0.0)
    #info_frc.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax_frc.add_artist(text_frc)

    text_refine = AnchoredText(
    f"\\underline{{Parameters:}}\nDefocus 1: {int(info_refine_ctf['DEFOCUS1'])}Å\nDefocus 2: {int(info_refine_ctf['DEFOCUS2'])}Å\nAstig. angle : {info_refine_ctf['DEFOCUS_ANGLE']:.1f}°\nTilt axis angle: {info_refine_ctf['TILT_AXIS']:.1f}°\nTilt angle: {info_refine_ctf['TILT_ANGLE']:.1f}°\nSample Thickness: {int(info_refine_ctf['SAMPLE_THICKNESS'])}Å\n\\underline{{Fit resolution:}} {info_refine_ctf['DETECTED_RING_RESOLUTION']:.1f}Å", frameon=False,loc='upper left',bbox_to_anchor=(1.05, 0.95), bbox_transform=ax_refine.transAxes, borderpad=0.0)
    #info_refine.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax_refine.add_artist(text_refine)
    # Set space between subplots
    #fig.subplots_adjust(hspace=0.05)
    #plt.tight_layout()