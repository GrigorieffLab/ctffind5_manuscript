import matplotlib.pyplot as plt
import numpy as np
import latexipy as lp
import json
from pathlib import Path
import scienceplots

plt.style.use(['science','scatter','ieee'])
import utils


dataset=Path(__file__).parent.parent.parent / "data/ER_Hox_120h_20211029_g1_l1_thickness_nodes.db"
selected_micrographs = utils.get_thickness_data_from_db(dataset,2)
with open(str(Path(dataset).with_suffix('')) + "_thickness.json","r") as fp:
    thickness_data = json.load(fp)
defocus = [[thickness_data[m['movie_filename']],m['SAMPLE_THICKNESS']] for i,m in selected_micrographs.iterrows() if m['movie_filename'] in thickness_data ]
with lp.figure(f"thickness_by_node_vs_by_lamber_beer",tight_layout=False):
    cm = plt.cm.get_cmap('viridis')
    data_euc = np.array(defocus,dtype=float)
    # Average all values over 0.3 in data_euc[:,0] (Images over vacuum)s
    thresh = 0.3
    average = np.mean(data_euc[data_euc[:,0]>thresh,0])
    
    data_euc[:,0] = - np.log(data_euc[:,0]/average) 
    data_euc = data_euc[data_euc[:,1]>0]
    data_euc = data_euc[data_euc[:,1]< 3000]
    data_euc = data_euc[data_euc[:,0]<  1.0]
    #plt.hist(data_euc[:,0],bins=100,color='k',alpha=0.5)

    if True:

        x = data_euc[:,1]/10
        y = data_euc[:,0]

        sc = plt.scatter(x,y,s=1)
        x = x[:,np.newaxis]
        a, _, _, _ = np.linalg.lstsq(x, y)
        x = np.linspace(0,300,10)
        plt.plot(x,x*a, 'r--' )
        # Write extinction coefficeint on plot
        plt.text(0.05, 0.95, f"$\kappa = {1/a[0]:.2f}$", transform=plt.gca().transAxes, fontsize=9)
        plt.xlabel("Thickness by Node [nm]")
        plt.ylabel(r"$\displaystyle-\ln\frac{I}{I_0}$")



