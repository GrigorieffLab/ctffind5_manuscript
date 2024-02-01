"""
# rotation matrix transform, find the 0 tilt initial axis direction and tilt angle
# by Lingli Kong @ Grigorieff lab

# minor changes by Johannes Elferich @ Grigorieff lab to make style consistent
"""
# %% module loading
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
# %%
filepath='/data/lingli/CTFTiltFit/rawdata/rawdata_CTFTILT/tomo03_ctffind5/DataSet_2_0131/'
rawtltfile='/data/lingli/CTFTiltFit/rawdata/tomo03.tlt'


outliers=np.loadtxt(filepath+'outlier_index.txt')
ctffind5_info = np.loadtxt(filepath+'ctffind_tilt_and_axis_angle_counterclock.txt')
exp_tilt_axis=np.loadtxt(filepath+'fitted_tilt_and_axis_angle.txt')
mean_abs_error=np.loadtxt(filepath+'mean_abs_error_exclude_center_tilts.txt')
abs_error=np.loadtxt(filepath+'abs_error_tilt_and_axis_angle.txt')
rawtlt=np.loadtxt(rawtltfile)

outliers=int(outliers)
exp_tilt=exp_tilt_axis[:,1]
exp_axis=exp_tilt_axis[:,2]
# %%
import latexipy as lp
import scienceplots
plt.style.use(['science','scatter','ieee'])

with lp.figure(f"ctftilt_lamella1_JE2_cppresult",tight_layout=False):
    # genrate two plots, One for fitted alues one for errors. Te error plot should be below and have 1/4 of the height. The figure should be 8.85 cm wide.
     
    plt,(ax_tilt, ax_axis_angle, ax_error) = plt.subplots(3,1,figsize=(3.5,3.5),sharex=True,gridspec_kw={'height_ratios':[2,2,1]})  
    ctffind5_data = ctffind5_info
    outlier_mask = np.in1d(range(ctffind5_data.shape[0]), outliers)
    no_outlier_mask = np.invert(outlier_mask)

    ax_tilt.plot(rawtlt,exp_tilt,linestyle='--',color='r')
    ax_tilt.scatter(rawtlt[no_outlier_mask],ctffind5_data[no_outlier_mask,1],marker='o')
    ax_tilt.scatter(rawtlt[outliers],ctffind5_data[outliers,1],marker='o',color='grey')#,label='outliers')

    ax_axis_angle.plot(rawtlt,exp_axis,linestyle='--',color='r',label='Overall tilt model')
    ax_axis_angle.scatter(rawtlt[no_outlier_mask],ctffind5_info[no_outlier_mask,2],marker='x',label='Single tilt measurement')
    ax_axis_angle.scatter(rawtlt[outliers],ctffind5_data[outliers,2],color='grey',marker='x')#,label='outliers')
    
  
    ax_error.scatter(rawtlt[no_outlier_mask],ctffind5_info[no_outlier_mask,1]-np.array(exp_tilt)[no_outlier_mask],marker='o')
    ax_error.scatter(rawtlt[no_outlier_mask],ctffind5_info[no_outlier_mask,2]-np.array(exp_axis)[no_outlier_mask],marker='x',color='k')
    ax_error.hlines(0,rawtlt[0],rawtlt[-1],'k',linestyles='--')

    # ax_error.hlines(0,tem_info[0,2],tem_info[-1,2],'k',linestyles='-')
    # ax_error.scatter(rawtlt[no_outlier_mask],abs_error[:,1][no_outlier_mask],marker='o')
    # ax_error.scatter(rawtlt[no_outlier_mask],abs_error[:,2][no_outlier_mask],marker='x',color='k') 
    # ax_error.hlines(mean_abs_error[0],rawtlt[0],rawtlt[-1],'k',linestyles='-')
    # ax_error.hlines(mean_abs_error[1],rawtlt[0],rawtlt[-1],'k',linestyles='--')


    plt.subplots_adjust(hspace=0.05)
    ax_tilt.set_ylabel('Tilt angle (°)')
    ax_axis_angle.set_ylabel('Tilt axis angle (°)')
    ax_error.set_ylabel('Error (°)')
    ax_error.set_xlabel('Nominal stage tilt angle (°)')
    ax_error.set_ylim(-13,13)

# %%
