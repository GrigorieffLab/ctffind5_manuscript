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

#Disable logger
import logging
logging.disable(logging.CRITICAL)


plt.style.use(['science','ieee'])

# Open the .txt file

node_ctf = {}
with open("/nrs/elferich/DLP/Assets/CTF/May06_12.17.22_14_0_CTF_2_avrot.txt") as f:
    for i, line in enumerate(f):
        if i == 5:
            node_ctf["spatial_freq"] = np.array(line.split()[1:], dtype=float)
        if i == 7:
            node_ctf["epa"] = np.array(line.split()[1:], dtype=float)
        if i == 8:
            node_ctf["model"] = np.array(line.split()[1:], dtype=float)
        if i == 9:
            node_ctf["quality_score"] = np.array(line.split()[1:], dtype=float)

node_ctf["spatial_freq"] = 1/node_ctf["spatial_freq"]

# Open the .txt file
classic_ctf = {}
with open("/nrs/elferich/DLP/Assets/CTF/May06_12.17.22_14_0_CTF_0_avrot.txt") as f:
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


info_image = database.get_image_info_from_db("/nrs/elferich/DLP/DLP.db",14)
con = sqlite3.connect("/nrs/elferich/DLP/DLP.db")
info_node_ctf = pd.read_sql(f"SELECT * FROM ESTIMATED_CTF_PARAMETERS WHERE CTF_ESTIMATION_ID = 53", con).iloc[0]
info_ctffind4_ctf = pd.read_sql(f"SELECT * FROM ESTIMATED_CTF_PARAMETERS WHERE CTF_ESTIMATION_ID = 14", con).iloc[0]

with lp.figure(f"dlp_ctffind_alternative",tight_layout=False):
    fig, [ax_classic, ax_node] = plt.subplots(2,1, sharex=True)
    ax_classic.plot(classic_ctf["spatial_freq"], classic_ctf["epa"], label="EPA")
    ax_classic.plot(classic_ctf["spatial_freq"], classic_ctf["model"], label="Model")
    ax_classic.plot(classic_ctf["spatial_freq"], classic_ctf["quality_score"], label="Fit quality")
    ax_node.plot(node_ctf["spatial_freq"], node_ctf["epa"], label="EPA")
    ax_node.plot(node_ctf["spatial_freq"], node_ctf["model"], label="Model")
    ax_node.plot(node_ctf["spatial_freq"], node_ctf["quality_score"], label="Fit quality")

    ax_node.set_xlabel("Spatial Resolution (Å)")
    ax_node.set_ylabel("Value")
    ax_classic.set_ylabel("Value")
    ax_node.set_xscale("log")
    ax_classic.set_xscale("log")
    ax_node.set_xlim(15,2.5)
    ax_node.set_xticks([12, 10, 8, 6, 4, 3])
    ax_node.set_xticklabels([12, 10, 8, 6, 4, 3])

    ax_classic.set_ylim(-0.0,1.05)
    ax_node.set_ylim(-0.0,1.05)

    # Set space between subplots
    fig.subplots_adjust(hspace=0.05)




