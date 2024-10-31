# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:40:48 2024

Version 0.1
Plots DTS data in a "heatmap" format

@author: Nate
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib import colors


# Text parameters - adjust as needed
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams.update({'font.size': 48})

# # normalizing colormap so 0 ue is unshaded - use if working with DSS data
# divnorm =  colors.TwoSlopeNorm(0)

# select the file you want to plot
filepath_or_buffer = "C:/Users/natha/Documents/PhD/research/MMV/Au Sable/OTS4/pickle/PIRO_DSS_Freq.pkl"
p_file_path_or_buffer = "C:/Users/natha/Documents/PhD/coding/OTS/Lighthouse_DSS_locations.pkl"

# reads in data and converts to np array
df = pd.read_pickle(filepath_or_buffer)
loc = pd.read_pickle(p_file_path_or_buffer)
time = df["ElapsedTime"]
strain = df.iloc[:,1:df.shape[1]]

# convert df to np array
time = time.values.flatten() / (60*60*24) # converts seconds to days
strain = strain.values.T
loc = loc.values.flatten()

# # create tare - use for DSS only
# tare = strain[:,7500]
# tare = tare[:,np.newaxis]
# tare = np.repeat(tare,15508,axis=1)
# strain = strain - tare

# create plot
fig = plt.figure(figsize=(48,24))
gs = gridspec.GridSpec(1, 2, width_ratios=[30, 1])  # 2 rows, 4 columns

X, Y = np.meshgrid(time, loc)

ax1 = plt.subplot(gs[0, 0])
color_plot = ax1.pcolormesh(X, Y, strain, cmap='Reds') # use for raw measurement
# color_plot = ax1.pcolormesh(X, Y, strain, cmap='seismic',norm = divnorm) # use for tare measurements
ax1.invert_yaxis()
ax1.set_xlabel('Time (days)')
ax1.set_ylabel('Position along fiber (m)')
ax1.set_title("Lighthouse Frequency")

cax = plt.subplot(gs[0, 1])
cbar = plt.colorbar(color_plot, cax=cax, label=r'Frequency (GHz)')
# cbar.set_ticks([-2*std, -600, -300, 0, 2*std])  # Set the positions of the ticks
# cbar.set_ticklabels(['C(-)', '-600', '-300', '0', '300', '600', 'T(+)'])  # Set the labels corresponding to the ticks
# Set the position of the ticks and labels
cbar.ax.xaxis.set_ticks_position('top')

plt.tight_layout() 
plt.show()