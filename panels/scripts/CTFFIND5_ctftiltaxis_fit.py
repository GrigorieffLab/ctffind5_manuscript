"""
# rotation matrix transform, find the 0 tilt initial axis direction and tilt angle
# by Lingli Kong @ Grigorieff lab
"""
# %% module loading
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
# %% functions
def rotation_matrix_from_vectors(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix

def find_zero_axis(A_ctf, A_tem):
    A_zero=np.matmul(A_ctf,np.linalg.inv(A_tem))
    return A_zero

def force_matrix_zxz(A_mat):
    test_vec=[0,0,1]
    zero_obj=R.from_matrix(A_mat) 
    test_vec_n=zero_obj.apply(test_vec)
    matrix=rotation_matrix_from_vectors(test_vec,test_vec_n)
    degrees=R.from_matrix(matrix).as_euler('zxz',degrees=True)
    return degrees

def calc_zero_angs(euler_ctf, euler_tem):
    ctf_matrix=R.from_euler('zxz',[-euler_ctf[1],euler_ctf[2],euler_ctf[1]],degrees=True).as_matrix()
    tem_matrix=R.from_euler('zxz',[-euler_tem[1],euler_tem[2],euler_tem[1]],degrees=True).as_matrix()
    A_zero=find_zero_axis(ctf_matrix,tem_matrix)
    zero_r=R.from_matrix(A_zero)
    zero_r_deg=zero_r.as_euler('zxz',degrees=True)  
    return A_zero, zero_r_deg

def range_adjust_for_plot(tilt_axis_degrees,imod_rot,zero_orientation):
    no=len(tilt_axis_degrees)
    if imod_rot > 45:
        if zero_orientation[1]*zero_orientation[2]<0:
            tilt_axis_degrees[:,2]+=90
            for i in np.arange(0,image_no):
                while tilt_axis_degrees[i,2]>360:
                    tilt_axis_degrees[i,2]-=360
                while tilt_axis_degrees[i,2]<0:
                    tilt_axis_degrees[i,2]+=360
                if tilt_axis_degrees[i,2]<(imod_rot)/2.0:
                    tilt_axis_degrees[i,2]+=180
                    tilt_axis_degrees[i,1]*=-1
            tilt_axis_degrees[:,2]-=90
        if zero_orientation[1]*zero_orientation[2]>0:
            tilt_axis_degrees[:,2]-=90
            for i in np.arange(0,image_no):
                while tilt_axis_degrees[i,2]>360:
                    tilt_axis_degrees[i,2]-=360
                while tilt_axis_degrees[i,2]<0:
                    tilt_axis_degrees[i,2]+=360
                if tilt_axis_degrees[i,2]<(imod_rot)/2.0:
                    tilt_axis_degrees[i,2]+=180
                    tilt_axis_degrees[i,1]*=-1
            tilt_axis_degrees[:,2]+=90
    else:
        #this part need to be examined when imod rotation angle < 45. currently, test tomography not available
        for i in np.arange(0,image_no):
            while tilt_axis_degrees[i,2]>360:
                tilt_axis_degrees[i,2]-=360
            while tilt_axis_degrees[i,2]<0:
                tilt_axis_degrees[i,2]+=360
            if tilt_axis_degrees[i,2]<(imod_rot)/2.0:
                tilt_axis_degrees[i,2]+=180
                tilt_axis_degrees[i,1]*=-1


def generate_angle_axis_series(zero_obj,tem_matrices,image_no):
    angle_axis_degress=np.empty([image_no,3])
    for i in np.arange(0,image_no):
        angle_axis_matrix_cal=np.matmul(zero_obj.as_matrix(),tem_matrices[i])
        angle_axis_degress[i]=force_matrix_zxz(angle_axis_matrix_cal)
    # ctf degree correction, these operations are for figure plotting
# when flip the theta value, the axis direction should be rotated for 180 degrees.
    angle_axis_degress[:,1]=-angle_axis_degress[:,1]
    angle_axis_degress[:,2]=angle_axis_degress[:,2]+180
    return angle_axis_degress


def fitting_plot(ctffind5_data, fitted_data, index, zero_rot, filename, plotoutlier=False):
    fig,ax = plt.subplots(2,1,figsize=(8,6))
    if plotoutlier:
        fullindex=range(len(fitted_data[:]))
        ax[0].scatter(ctffind5_data[index,0],ctffind5_data[index,2],marker='x',s=16,c='k',label='ctffind5 axis')
        ax[0].plot(ctffind5_data[:,0],fitted_data[:,2],linewidth=2,c='r',linestyle='--',label='fitted axis')
        ax[1].scatter(ctffind5_data[index,0],ctffind5_data[index,1],marker='x',s=16,c='k',label='ctffind5 tilt')
        ax[1].plot(ctffind5_data[:,0],fitted_data[:,1],linewidth=2,c='r',linestyle='--',label='fitted tilt')
        outliers_index=np.delete(fullindex,new_index)
        print("outlier index",outliers_index)
        ax[0].scatter(ctffind5_data[outliers_index,0],ctffind5_data[outliers_index,2],marker='x',s=16,c='k')#,label='outliers')
        ax[0].scatter(ctffind5_data[outliers_index,0],ctffind5_data[outliers_index,2],s=60,facecolors='none',edgecolors='g')
        # ax[0].plot(ctffind5_data[:,0],fitted_data[:,2],linewidth=2,c='r',linestyle='--',label='fitted axis')
        ax[1].scatter(ctffind5_data[outliers_index,0],ctffind5_data[outliers_index,1],marker='x',s=16,c='k')#,label='outliers')
        ax[1].scatter(ctffind5_data[outliers_index,0],ctffind5_data[outliers_index,1],s=60,facecolors='none',edgecolors='g')

        # ax[1].plot(ctffind5_data[:,0],fitted_data[:,1],linewidth=2,c='r',linestyle='--',label='fitted tilt')
    else:
        ax[0].scatter(ctffind5_data[index,0],ctffind5_data[index,2],marker='x',s=16,c='k',label='ctffind5 axis')
        ax[0].plot(ctffind5_data[:,0],fitted_data[:,2],linewidth=2,c='r',linestyle='--',label='fitted axis')
        ax[1].scatter(ctffind5_data[index,0],ctffind5_data[index,1],marker='x',s=16,c='k',label='ctffind5 tilt')
        ax[1].plot(ctffind5_data[:,0],fitted_data[:,1],linewidth=2,c='r',linestyle='--',label='fitted tilt')
    
    # add the fitted result text
    # ax[0].text(0.5,250,'$\phi$ = '+str('{:.1f}'.format(zero_rot[2])+'$^\circ$'), style='italic',fontsize=15, bbox={'facecolor': 'gray', 'alpha': 0.2, 'pad': 3})
    # ax[1].text(0.5,-60.0,'$\\theta$ = '+str('{:.1f}'.format(zero_rot[1])+'$^\circ$'), style='italic',fontsize=15, bbox={'facecolor': 'gray', 'alpha': 0.2, 'pad': 3})

    ax[1].set_xlabel("image index",fontsize=15)
    ax[0].legend(loc='best', frameon=False)
    ax[1].legend(loc='best', frameon=False)
    # ax[0].text(1, 13, 'axis', style='italic', bbox={'facecolor': 'green', 'alpha': 0.5, 'pad': 10})

    fig.supylabel("angle")
    plt.rc('font',size=15)
    plt.savefig(filename)
    # plt.close()

def error_plot(error_series, threshold, index, zero_rot,filename):
    fig,ax = plt.subplots(1,1,figsize=(8,6))
    fullindex=range(len(error_series[:]))
    outliers_index=np.delete(fullindex,index)
    ax.scatter(index,error_series[index],s=60,alpha=0.5)
    ax.scatter(outliers_index,error_series[outliers_index],s=60,alpha=0.5, label='outliers')
    ax.hlines(threshold,0,len(error_series),'k',linestyles='dotted')
    ax.text(1,threshold*2,'$\phi$ = '+str('{:.1f}'.format(zero_rot[2]))+'$^\circ$'+'\n'+'$\\theta$ = '+ \
                                    str('{:.1f}'.format(zero_rot[1])+'$^\circ$'), style='italic',fontsize=15, bbox={'facecolor': 'gray', 'edgecolor': 'none', 'alpha': 0.1, 'pad': 3})
    # ax.text(25,threshold*2,'$\phi$ = '+str('{:.1f}'.format(zero_rot[2]))+'$^\circ$'+'\n'+'$\\theta$ = '+ \
                                    # str('{:.1f}'.format(zero_rot[1])+'$^\circ$'), style='italic',fontsize=15, bbox={'facecolor': 'gray', 'edgecolor': 'none', 'alpha': 0.1, 'pad': 3})

    # ax[1].text(0.5,-60.0,'$\\theta$ = '+str('{:.1f}'.format(zero_rot[1])+'$^\circ$'), style='italic',fontsize=15, bbox={'facecolor': 'gray', 'alpha': 0.2, 'pad': 3})
    ax.annotate('RMSE', xy=(1,threshold))
    ax.set_xlabel("image index",fontsize=15)
    ax.set_ylabel("error",fontsize=15)
    ax.legend(frameon=False)
    plt.rc('font',size=15)
    plt.savefig(filename)
    # plt.close()
    

# %% data loading and parameter initialization========================================================================
# # # lamella grid 1 tilt04 dataset--------------
# # filepath='../unstacked_tilt04/'
# filepath='/data/lingli/CTFTiltFit/tilt04_ctffind5/tilt04_ctffind5/'
# outpath='/data/lingli/CTFTiltFit/tilt04_ctffind5/tilt04_ctffind5/fit_1/'
# rawtltfile='/data/lingli/Lingli_20221028/grid1/tilt04.tlt'
# ctffind5_info=np.loadtxt(filepath +'tilt_axis_angle_1') # it stores the [index AxisDirection TiltAngle]
# # rotation_angle_imod=86.3
# rotation_angle_imod=88.4
# fib_tilt=20
# # print(ctffind5_info)

# # ctffind5 paper tomo03----------------
filepath='/data/lingli/CTFTiltFit/rawdata/rawdata_CTFTILT/tomo02_ctffind5/'
outpath='/data/lingli/CTFTiltFit/rawdata/rawdata_CTFTILT/tomo02_ctffind5/'
rawtltfile='/data/lingli/CTFTiltFit/rawdata/tomo02.tlt'
rotation_angle_imod=86.3
# rotation_angle_imod=88.4
fib_tilt=-20
ctffind5_info=np.loadtxt(filepath +'tilt_axis_angle') # it stores the [index AxisDirection TiltAngle]
# # ###--------------------------------------

#ctffind angle:
image_no=len(ctffind5_info[:,0])
# in cisTEM, both axis direction and tilt are clockwise. 
# the following convert them to counter-clockwise
ctffind5_info[:,1]=360-ctffind5_info[:,1] #ensure the rotation angle is counter-clockwise
ctffind5_info[:,2]=-ctffind5_info[:,2] #make sure the tilts is couter-clockwise
#---------------------------------------------

#microscope angle system:
rawtlt=np.loadtxt(rawtltfile)
tem_info=np.zeros(np.shape(ctffind5_info))
tem_info[:,0]=ctffind5_info[:,0] #index
tem_info[:,1]=90+rotation_angle_imod #counter clock wise starting from x axis direction
tem_info[:,2]=rawtlt

euler_ctf=ctffind5_info[1]
euler_tem=tem_info[1]
# ctf_matrix_series=np.zeros((3,3))
ctf_matrix_series=np.empty([image_no,3,3])
tem_matrix_series=np.empty([image_no,3,3])
zero_angle_series=np.empty([image_no,3])

ctf_degrees=np.empty([image_no,3])
exp_degrees=np.empty([image_no,3])
ctf_degrees_new=np.empty([image_no,3])

vec=[0,0,1] #normal vector along z direction
# print(np.shape(ctf_matrix_series))
for i in np.arange(0,len(rawtlt)):
    tem_matrix_series[i]=np.array(R.from_euler('zxz',[-tem_info[i][1],tem_info[i][2],tem_info[i][1]],degrees=True).as_matrix())

# %% main program for fitting========================================================================
# step 1: find the zero matrix for each tilt by: Rzero X Rtem = Rctf
print("---the initial tilt and axis calculated from each tilt image---")
for i in np.arange(0,image_no):
    zero_degress=calc_zero_angs(ctffind5_info[i],tem_info[i])
    zero_angle_series[i]=np.array(zero_degress[1])
    print(zero_degress[1][1:])

#step 2: apply a normal vector to the zero_degree matrix to check how much the z axis 
count_no=0
vec_series=np.zeros([image_no,3]) # this stores the vector after the vec[0,0,1] rotated by the zero matrix
for i in np.arange(0,image_no):
    if(i>=0):
        rot_obj=R.from_euler('zxz',zero_angle_series[i],degrees=True)
        vec_series[i]=rot_obj.apply(vec)
        count_no+=1

#step 3: average the normal vectors of the initial tilt calculated from different tilting images
rotated_vec=np.sum(vec_series, axis=0)/count_no #average the normal vectors 
target_matrix=rotation_matrix_from_vectors(vec,rotated_vec)
zero_rot=R.from_matrix(target_matrix).as_euler('zxz',degrees=True)

#step 4: generate angle and axis for the tilt series
zero_tilt_obj=R.from_euler('zxz',zero_rot,degrees=True)
exp_zero_obj=R.from_euler('zxz',[-90-rotation_angle_imod,fib_tilt,90+rotation_angle_imod],degrees=True)
ctf_degrees=generate_angle_axis_series(zero_tilt_obj,tem_matrix_series,image_no)
exp_degrees=generate_angle_axis_series(exp_zero_obj,tem_matrix_series,image_no)

np.set_printoptions(suppress=True,formatter={'float_kind':'{:2f}'.format})
print("---fitted tilt angle and axis angle for each tilt---")
print(np.around(ctf_degrees[:,1:],decimals=2))
print("the initial tilt:", zero_rot[1])
print("the initial axis:", zero_rot[2])
range_adjust_for_plot(ctf_degrees,rotation_angle_imod,zero_rot)
range_adjust_for_plot(exp_degrees,rotation_angle_imod,zero_rot)
# # swap the column to use the function range_adjust_for_plot
ctffind5_info[:,[2,1]]=ctffind5_info[:,[1,2]]
range_adjust_for_plot(ctffind5_info,rotation_angle_imod,zero_rot)
fitting_plot(ctffind5_info,ctf_degrees,range(image_no),zero_rot,outpath + 'fitted_ctffind.pdf', False)

# %%  Refinement: find the outliers and refine fitting=============================================================
# sample orientation error calculation
# vector distance, root mean squared error: RMSE
# %%
# axis and angle error 
angle_diff=ctffind5_info[:,1]-ctf_degrees[:,1]
axis_diff=ctffind5_info[:,2]-ctf_degrees[:,2]
print(angle_diff)
# plt.scatter(x,angle_diff)
# plt.close()
print(axis_diff)
# plt.scatter(x,axis_diff)

vec_dis=vec_series-rotated_vec
vec_dis_val=np.sqrt(vec_dis[:,0]**2+vec_dis[:,1]**2+vec_dis[:,2]**2)
rmse=np.sqrt(np.sum(vec_dis_val**2)/len(vec_dis_val))
print("root mean squre error is ", rmse)
# x=np.linspace(1,len(vec_dis_val),len(vec_dis_val))

# scatter plot to show the vector distance
new_index=np.where(vec_dis_val<=rmse)
# three_sigma=np.mean(vec_dis_val) + 3 * np.std(vec_dis_val)
# new_index=np.where(vec_dis_val<=three_sigma)
# one_sigma=np.mean(vec_dis_val) + np.std(vec_dis_val)
# new_index=np.where(vec_dis_val<=one_sigma)


rotated_vec_new=np.sum(vec_series[new_index], axis=0)/len(new_index[0]) #average the normal vectors 
target_matrix=rotation_matrix_from_vectors(vec,rotated_vec_new)
zero_rot_new=R.from_matrix(target_matrix).as_euler('zxz',degrees=True)
error_plot(vec_dis_val, rmse, new_index, zero_rot_new,outpath+'error_plot.pdf')
# error_plot(vec_dis_val, three_sigma, new_index)
# error_plot(vec_dis_val, one_sigma, new_index)

# plt.scatter(x,vec_dis_val)
# plt.hlines(rmse,0,image_no,'r',linestyles='dotted')
# plt.hlines(three_sigma,0,image_no,'k',linestyles='dotted')
# error_plot(vec_dis_val, three_sigma, new_index)

print("---fitted tilt and axis after outlier removed---")
print("the initial tilt:", zero_rot_new[1])
print("the initial axis:", zero_rot_new[2])


# %%
# generate angle and axis for the tilt series
zero_tilt_obj_new=R.from_euler('zxz',zero_rot_new,degrees=True)
ctf_degrees_new=generate_angle_axis_series(zero_tilt_obj_new,tem_matrix_series,image_no)
print("---refined fitted tilt angle and axis angle for each tilt---")
print(np.around(ctf_degrees_new[:,1:],decimals=2))
range_adjust_for_plot(ctf_degrees_new,rotation_angle_imod,zero_rot_new)
fitting_plot(ctffind5_info,ctf_degrees_new,new_index,zero_rot_new,outpath + 'fitted_ctffind_outlier_removed.pdf', True)

# %% save the results
np.savetxt(outpath+'calculated_ctf_deg.txt',ctf_degrees[:,1:],fmt="%10.3f")
# np.savetxt(filepath+'calculated_ctf_deg_tmp.txt',ctf_degrees[:,1:],fmt="%10.3f")
np.savetxt(outpath+'tem_degreeinfo.txt',tem_info,fmt="%10.3f")
np.savetxt(outpath+'zero_tilt.txt',zero_rot[1:],fmt="%10.3f")
np.savetxt(outpath+'tilt_axis_angle_rotfix.txt',ctffind5_info,fmt="%10.3f")
np.savetxt(outpath+'zero_tilt_outlier_removed.txt',zero_rot_new[1:],fmt="%10.3f")
np.savetxt(outpath+'calculated_ctf_deg_outlier_removed.txt',ctf_degrees_new[:,1:],fmt="%10.3f")


