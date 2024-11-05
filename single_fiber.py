# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 11:22:58 2024

@author: Nate
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from get_folders import get_folders
from get_odisi_data_DEV import get_data

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams.update({'font.size': 32})

parent = '/home/nate/Documents/ODiSi/PIRO'
folders = get_folders(parent)
save_to = '/home/nate/Documents/ODiSi/pickle'
test_name = 'au_sable_first_half' 

for folder in folders:
    my_folder = f"{parent}/{folder}"
    print(f"Working on {my_folder}\n")
    get_data(my_folder,save_to,test_name)
      
    # read in .pkl files to dataframes
    # read_dir = os.path.join(save_to,f"{test_name}/",f"{folder}")
    read_dir = "/home/nate/Documents/ODiSi/pickle/au_sable_first_half/024-09-18_20-2"
    
    n_fibers = [f for f in os.listdir(my_folder) if f.endswith('full.tsv')]
    n_fibers = len(n_fibers)
    
    for x in range(n_fibers):
        position = pd.read_pickle(f"{read_dir}/position/lighthouse_2024-09-18_20-21-56_ch{x+1}_full.tsv-position.pkl")
        values = pd.read_pickle(f"{read_dir}/values/lighthouse_2024-09-18_20-21-56_ch{x+1}_full.tsv-values.pkl")
        time = pd.read_pickle(f"{read_dir}/time/lighthouse_2024-09-18_20-21-56_ch{x+1}_full.tsv-time.pkl")
        std = values.values.std(ddof=1)
        
        # # change dataframes to arrays
        
        position = position.values.flatten()
        time = time.values.flatten()
        time = time / (60*60*24) # conversion to minute, hour, or day
        values = values.values.T
        
        # # plot
        
        time = time[::100]
        values = values[:, ::100]
        
        fig = plt.figure(figsize=(16,16))
        gs = gridspec.GridSpec(1, 2, width_ratios=[30, 1])  # 2 rows, 4 columns
        
        X, Y = np.meshgrid(time, position)
        
        ax1 = plt.subplot(gs[0, 0])
        color_plot = ax1.pcolormesh(X, Y, values, cmap='bwr', vmax = 2*std, vmin = -2*std)
        ax1.set_xlabel('Time (sec)')
        ax1.set_ylabel('Position along fiber (m)')
        ax1.set_title(f"Strain in Fiber {x+1}")
        
        cax = plt.subplot(gs[0, 1])
        cbar = plt.colorbar(color_plot, cax=cax, label=r'microstrain ($\mu\varepsilon$)')
        # cbar.set_ticks([-2*std, -600, -300, 0, 300, 600, 2*std])  # Set the positions of the ticks
        # cbar.set_ticklabels(['C(-)', '-600', '-300', '0', '300', '600', 'T(+)'])  # Set the labels corresponding to the ticks
        # Set the position of the ticks and labels
        cbar.ax.xaxis.set_ticks_position('top')
        
        plt.tight_layout() 
        plt.show()

