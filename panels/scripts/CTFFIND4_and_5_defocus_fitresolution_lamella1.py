# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def extract_data(file_path):
    data = pd.read_csv(file_path, sep='|', header=None)
    return data

# %%
ctffind4=extract_data('/data/lingli/CTFTiltFit/tilt04_ctffind5/tilt04_ctffind5/defocus_and_angle_ctffind4.txt')
ctffind5=extract_data('/data/lingli/CTFTiltFit/tilt04_ctffind5/tilt04_ctffind5/defocus_and_angle.txt')
# %%
ctffind4_defocus=(ctffind4.iloc[:,1] + ctffind4.iloc[:,2])/2
ctffind4_score=ctffind4.iloc[:,4]
ctffind4_fitreso=ctffind4.iloc[:,5]
ctffind5_defocus=(ctffind5.iloc[:,1] + ctffind5.iloc[:,2])/2
ctffind5_score=ctffind5.iloc[:,4]
ctffind5_fitreso=ctffind5.iloc[:,5]
# %%

filepath='/data/lingli/CTFTiltFit/tilt04_ctffind5/tilt04_ctffind5/DataSet_1_0131/'
rawtltfile='/data/lingli/Lingli_20221028/grid1/tilt04.tlt'

outliers=np.loadtxt(filepath+'outlier_index.txt')
ctffind5_info = np.loadtxt(filepath+'ctffind_tilt_and_axis_angle_counterclock.txt')
exp_tilt_axis=np.loadtxt(filepath+'fitted_tilt_and_axis_angle.txt')
mean_abs_error=np.loadtxt(filepath+'mean_abs_error_exclude_center_tilts.txt')
abs_error=np.loadtxt(filepath+'abs_error_tilt_and_axis_angle.txt')
rawtlt=np.loadtxt(rawtltfile)

outliers=int(outliers)
exp_tilt=exp_tilt_axis[:,1]
exp_axis=exp_tilt_axis[:,2]


import latexipy as lp
import scienceplots
plt.style.use(['science','scatter','ieee'])


with lp.figure(f"lamella1_ctffind4_5_tilt_defocus_fitresolution",tight_layout=False):
     
    # plt,(ax_defocus,ax_fitreso) = plt.subplots(2,1,figsize=(3.5,3.5),sharex=True,gridspec_kw={'height_ratios':[1,1]})  
    plt,(ax_tilt,ax_defocus,ax_fitreso) = plt.subplots(3,1,figsize=(3.5,3.5),sharex=True,gridspec_kw={'height_ratios':[1,1,1]})  


    ctffind5_data = ctffind5_info
    outlier_mask = np.in1d(range(ctffind5_data.shape[0]), outliers)
    no_outlier_mask = np.invert(outlier_mask)

    ax_tilt.plot(rawtlt,exp_tilt,linestyle='--',color='r')
    ax_tilt.scatter(rawtlt[no_outlier_mask],ctffind5_data[no_outlier_mask,1],marker='o')
    ax_tilt.scatter(rawtlt[outliers],ctffind5_data[outliers,1],marker='o',color='grey')#,label='outliers')

    ax_defocus.plot(rawtlt,ctffind4_defocus/10000,linestyle='--',marker='x',color='r')
    ax_defocus.plot(rawtlt,ctffind5_defocus/10000,linestyle='--',marker='o',fillstyle='none',color='k')
    ax_defocus.scatter(rawtlt[outliers],ctffind5_defocus[outliers]/10000,marker='o',color='grey')#,label='outliers')

    ax_fitreso.plot(rawtlt,ctffind4_fitreso,linestyle='--',marker='x',color='r')
    ax_fitreso.plot(rawtlt,ctffind5_fitreso,linestyle='--',marker='o',fillstyle='none',color='k')
    ax_fitreso.scatter(rawtlt[outliers],ctffind5_fitreso[outliers],marker='o',color='grey')#,label='outliers')


    plt.subplots_adjust(hspace=0.05)

    ax_tilt.set_ylabel('Tilt angle (°)')

    ax_defocus.set_ylabel('Defocus (µm)')
    ax_fitreso.set_ylabel('Fit resolution (Å)')
    ax_fitreso.set_xlabel('Nominal stage tilt angle (°)')

    current_values = ax_defocus.get_yticks()
    ax_defocus.set_yticklabels(['{:,.1f}'.format(x) for x in current_values])
