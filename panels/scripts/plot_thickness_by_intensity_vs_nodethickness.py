import matplotlib.pyplot as plt
import numpy as np
import latexipy as lp
import json
from pathlib import Path


import utils
defocus = []

lp.latexify()

for dataset, name in utils.dataset_info[:]:
    selected_micrographs = utils.get_thickness_data_from_db(dataset,2)
    with open(Path(dataset).stem +"_thickness.json","r") as fp:
        thickness_data = json.load(fp)
    defocus = [[thickness_data[m['movie_filename']],m['SAMPLE_THICKNESS']] for i,m in selected_micrographs.iterrows() if m['movie_filename'] in thickness_data ]
    print(defocus)
    with lp.figure(f"thickness_by_intensity_vs_by_node_{name}",size=lp.figure_size(ratio=1.0,doc_width_pt=250),tight_layout=True):
        cm = plt.cm.get_cmap('viridis')
        data_euc = np.array(defocus,dtype=float)
        # Average all values over 0.3 in data_euc[:,0]
        if name.startswith("euc"):
            thresh = 0.3
        else:
            thresh = 0.28
        average = np.mean(data_euc[data_euc[:,0]>thresh,0])
        
        data_euc[:,0] = - np.log(data_euc[:,0]/average) 
        print(data_euc[:,0])
        data_euc = data_euc[data_euc[:,1]>0]
        data_euc = data_euc[data_euc[:,1]< 3000]
        data_euc = data_euc[data_euc[:,0]<  1.0]
        #plt.hist(data_euc[:,0],bins=100,color='k',alpha=0.5)

        if True:
            if name.startswith("euc"):
                s = 9
            else:
                s = 11
            print(data_euc)

            x = data_euc[:,1]/10
            y = data_euc[:,0]

            sc = plt.scatter(x,y,s=1)
            x = x[:,np.newaxis]
            a, _, _, _ = np.linalg.lstsq(x, y)
            
            plt.plot(x,x*(1/300), color='r', linestyle='dashed', linewidth=1)
            print(1/a)
            # Write extinction coefficeint on plot
            plt.text(0.05, 0.95, f"$\kappa = {300:.2f}$", transform=plt.gca().transAxes, fontsize=9)
            plt.xlabel("Thickness by Node [nm]")
            plt.ylabel("ln(I/I0)")



