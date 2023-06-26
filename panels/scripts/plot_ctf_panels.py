import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import scienceplots
import latexipy as lp

import logging
logging.disable(logging.CRITICAL)

from pycistem.core import CTF


plt.style.use(['science','ieee'])

ctf = CTF(300,2.7,0.07,9000,9000,0,30,900,1.0)

ctf.SetSampleThickness(1500)


spatial_frequency = np.linspace(0.01,0.5,1000)
spatial_frequency_squared = spatial_frequency**2

ctf_values = np.array([ctf.Evaluate(x,0.0)**2 for x in spatial_frequency_squared])
ctf_values2 = np.array([ctf.EvaluatePowerspectrumWithThickness(x,0.0,False) for x in spatial_frequency_squared])

modulation = np.array([ctf.IntegratedDefocusModulation(x) for x in spatial_frequency_squared])
spatial_frequency = 1/spatial_frequency
with lp.figure(f"node_models",tight_layout=False):
    # Generate 2x3 subplots with plots touching each other

    fig, ax = plt.subplots(2,2,sharex=True,figsize=(3.5,2.5))
    ax[0][0].plot(spatial_frequency, ctf_values, label="CTF")
    ax[1][0].plot(spatial_frequency, ctf_values2, label="CTF")
    ax[1][1].plot(spatial_frequency, modulation, label="CTF")
    ax[1][1].set_ylim(-1.1,1.1)
    # Hide ax[0][1], as it is not used for any plot
    ax[0][1].axis('off')
    # Set labels
    ax[0][0].set_ylabel("Ctffind 4",labelpad=16)
    ax[1][0].set_ylabel("McMullan et al.",labelpad=16)
    ax[1][0].set_xlabel("Spatial Resolution (Å)")
    ax[1][1].set_xlabel("Spatial Resolution (Å)")
    ax[1][0].set_xscale("log")
    ax[1][0].set_xlim(15,3.1)
    ax[1][0].set_xticks([12, 10, 8, 6, 4])
    ax[1][0].set_xticklabels([12, 10, 8, 6, 4])
    ax[1][1].set_xscale("log")
    ax[1][1].set_xlim(15,3.1)
    ax[1][1].set_xticks([12, 10, 8, 6, 4])
    ax[1][1].set_xticklabels([12, 10, 8, 6, 4])
    
    fig.supylabel("Value",x=0.02)

    ax[0][0].set_title("CTF")
    ax[0][1].set_title("Modulation function")

    plt.subplots_adjust(wspace=0.15, hspace=0.05)


