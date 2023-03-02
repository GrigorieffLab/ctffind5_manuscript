import matplotlib.pyplot as plt
import numpy as np
import latexipy as lp
import json
from pathlib import Path
import scienceplots
import pandas as pd
from scipy.stats import linregress


plt.style.use(['science','scatter','ieee'])
import utils
my_dict1 = {"NP2-s003": [171,175,173,174,183], 
          "s001": [157,161,143,144,142],
          "s006": [151,131,156,133,160],
          "Y12-s003": [146,157,158,146,154],
          "st003": [87,95,95,94,95],
          "st008": [176,176,166,169,180],
          "st011": [221,175,217,221,219]}

my_dict2 = {"NP2-s003": [203,205,207,216,212], 
          "s001": [187,177,173,184,195],
          "s006": [205,197,196,198,202],
          "Y12-s003": [216,232,204,231,233],
          "st003": [94,93,88,91,116],
          "st008": [217,212,196,188,206],
          "st011": [268,262,272,264,273]}

my_dict3 = {"NP2-s003":  214.7,
            "s001":  186.6,
            "s006":  218.4,
            "Y12-s003":  238.3,
            "st003":  100.2,
            "st008":  221.5,
            "st011":  284.3}

data1 = pd.DataFrame(data=my_dict1)
data_melt1 = data1.melt()
data_melt1["Method"] = "Imod recut contours"

data2 = pd.DataFrame(data=my_dict2)
data_melt2 = data2.melt()
data_melt2["Method"] = "Imod no recut and vectors used for cleaning"

data3 = pd.concat([data_melt1, data_melt2],ignore_index=True)



with lp.figure(f"thickness_by_node_vs_by_tomography",tight_layout=False):
    # Plot using my_dict 3 as the x-acxis position and my_dict 2 as the y-axis
    # position (as a boxplot)
    #plt.scatter(my_dict3.values(), my_dict2.values(), marker="o", color="k")
    print(my_dict2.values())
    plt.boxplot(list(my_dict2.values()), positions=list(my_dict3.values()), showfliers=False)
    # Calculate the R squared value
    medians = [np.median(x) for x in my_dict2.values()]
    slope, intercept, r_value, p_value, std_err = linregress(list(my_dict3.values()),medians)
    print(r_value) 
    print(p_value)
    print(std_err)
    print(slope)
    print(intercept) 

    
    # Set the same ticks and labels for x and y axis (100,150,200,250,300)
    labels = np.arange(100,350,50)
    plt.xticks(labels,labels)
    plt.yticks(labels,labels)
    plt.xlim(80,320)
    plt.ylim(80,320)
    # Plot unity diagonal
    plt.plot([80,320],[80,320],color="k",linestyle="--")
    plt.xlabel("Thickness by Node [nm]")
    plt.ylabel("Thickness by tomography [nm]")



