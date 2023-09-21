"""
# rotation matrix transform, find the 0 tilt initial axis direction and tilt angle
# by Lingli Kong @ Grigorieff lab

# minor changes by Johannes Elferich @ Grigorieff lab to make style consistent
"""
# %% module loading
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R


# %% data loading and parameter initialization========================================================================
# # # lamella grid 1 tilt04 dataset--------------
# filepath='../unstacked_tilt04/'
filepath='/data/lingli/CTFTiltFit/rawdata/rawdata_CTFTILT/tomo03_ctffind5/'
#outpath='./tmp/tilt04_ctffind5/tilt04_ctffind5/fit_1/'
rawtltfile='/data/lingli/CTFTiltFit/rawdata/tomo03.tlt'
ctffind5_info=np.loadtxt(filepath +'tilt_axis_angle') # it stores the [index AxisDirection TiltAngle]
# rotation_angle_imod=86.3
#rotation_angle_imod=88.4
#fib_tilt=20

image_no=len(ctffind5_info[:,0])

#microscope angle system:
rawtlt=np.loadtxt(rawtltfile)
tem_info=np.zeros(np.shape(ctffind5_info))
tem_info[:,0]=ctffind5_info[:,0] #index
tem_info[:,1]=0 #unknown
tem_info[:,2]=rawtlt


ctf_rotations = [R.from_euler('zxz',[-ctffind5_info[i,1],ctffind5_info[i,2],ctffind5_info[i,1]],degrees=True) for i in range(image_no)]
outliers = None

def optim_function(x,index=None):
    global outliers
    phi_zero, theta_zero, phi_tem = x
    res = []
    if index is None:
        index = range(image_no)
    for i in index:
        zero_rot = R.from_euler('zxz',[-phi_zero,theta_zero,phi_zero],degrees=True)
        tem_rot = R.from_euler('zxz',[-phi_tem,rawtlt[i],phi_tem],degrees=True)
        ctf_vec = ctf_rotations[i].apply([0,0,1])
        fit_vec = (tem_rot * zero_rot).apply([0,0,1])
        # Calculate angle between vectors ctf_vec and fit_vec
        res.append(np.linalg.norm(ctf_vec-fit_vec))
    rmse = np.sqrt(np.mean(np.array(res)**2))
    if np.max(np.array(res)/rmse) > 3.0:
        outliers = np.where(np.array(res)/rmse > 3.0)[0]
        return optim_function(x, np.where(np.array(res)/rmse < 3.0)[0])    
    return rmse


from scipy.optimize import minimize

sol = minimize(optim_function, [0,0,0])
phi_zero, theta_zero, phi_tem = sol.x
print(sol.x)
# JE Plotting code

exp_rot = [ R.from_euler('zxz',[-phi_tem,rawtlt[i],phi_tem],degrees=True) * R.from_euler('zxz',[-phi_zero,theta_zero,phi_zero],degrees=True) for i in range(image_no)]

exp_tilt = [r.as_euler('zxz',degrees=True)[1] for r in exp_rot]
exp_axis = [r.as_euler('zxz',degrees=True)[2] for r in exp_rot]
#exp_axis = [a-360 if a > 250 else a for a in exp_axis]

for i in range(image_no):
    if ctffind5_info[i,1] > 250 :
         ctffind5_info[i,1] -= 360

import latexipy as lp
import scienceplots
plt.style.use(['science','scatter','ieee'])

with lp.figure(f"ctftilt_lamella2_JE",tight_layout=False):
    # genrate two plots, One for fitted alues one for errors. Te error plot should be below and have 1/4 of the height. The figure should be 8.85 cm wide.
     
    plt,(ax_tilt, ax_axis_angle, ax_error) = plt.subplots(3,1,figsize=(3.5,3.5),sharex=True,gridspec_kw={'height_ratios':[2,2,1]})  
    ctffind5_data = ctffind5_info
    outlier_mask = np.in1d(range(ctffind5_data.shape[0]), outliers)
    no_outlier_mask = np.invert(outlier_mask)

    ax_tilt.plot(rawtlt,exp_tilt,linestyle='--',color='r')
    ax_tilt.scatter(rawtlt[no_outlier_mask],ctffind5_data[no_outlier_mask,2],marker='o')
    ax_tilt.scatter(ctffind5_data[outliers,0],ctffind5_data[outliers,2],marker='o',color='grey')#,label='outliers')

    ax_axis_angle.plot(rawtlt,exp_axis,linestyle='--',color='r',label='Overall tilt model')
    ax_axis_angle.scatter(rawtlt[no_outlier_mask],ctffind5_info[no_outlier_mask,1],marker='x',label='Single tilt measurement')
    ax_axis_angle.scatter(rawtlt[outliers],ctffind5_data[outliers,1],color='grey',marker='x')#,label='outliers')
    
  
    ax_error.scatter(rawtlt[no_outlier_mask],ctffind5_info[no_outlier_mask,2]-np.array(exp_tilt)[no_outlier_mask],marker='o')
    ax_error.scatter(rawtlt[no_outlier_mask],ctffind5_info[no_outlier_mask,1]-np.array(exp_axis)[no_outlier_mask],marker='x',color='k')
    ax_error.hlines(0,tem_info[0,2],tem_info[-1,2],'k',linestyles='-')
   

    plt.subplots_adjust(hspace=0.05)
    ax_tilt.set_ylabel('Tilt angle (°)')
    ax_axis_angle.set_ylabel('Tilt axis angle (°)')
    ax_error.set_ylabel('Error (°)')
    ax_error.set_xlabel('Nominal stage tilt angle (°)')
    ax_error.set_ylim(-12,12)