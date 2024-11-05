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

def split_array_with_remainder(arr, split_shape):
    """
    Splits a 2D array into smaller arrays of a specified shape and returns any remainder.
    
    Parameters:
        arr (numpy.ndarray): The 2D input array to be split.
        split_shape (tuple): The desired shape of each sub-array (rows, cols).
        
    Returns:
        list: List of sub-arrays of the specified shape.
        tuple: Remainder array (or None if there is no remainder), with remainder rows and columns as separate parts.
    """
    rows, cols = arr.shape
    sub_rows, sub_cols = split_shape

    # Calculate the number of full splits along each dimension
    num_sub_rows = rows // sub_rows
    num_sub_cols = cols // sub_cols

    # Create list to store sub-arrays
    sub_arrays = []

    # Extract the sub-arrays
    for i in range(num_sub_rows):
        for j in range(num_sub_cols):
            sub_array = arr[
                i * sub_rows : (i + 1) * sub_rows,
                j * sub_cols : (j + 1) * sub_cols
            ]
            sub_arrays.append(sub_array)

    # Determine remainders
    remainder_rows = arr[num_sub_rows * sub_rows :, :cols] if rows % sub_rows != 0 else None
    remainder_cols = arr[:rows, num_sub_cols * sub_cols :] if cols % sub_cols != 0 else None
    remainder_corner = None
    
    # Check if there's a remainder in the bottom-right corner
    if remainder_rows is not None and remainder_cols is not None:
        remainder_corner = arr[num_sub_rows * sub_rows :, num_sub_cols * sub_cols :]

    return sub_arrays, (remainder_rows, remainder_cols, remainder_corner)

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams.update({'font.size': 32})

#%% Get data

parent = '/home/nate/Documents/ODiSi/PIRO-pickles'
folders = get_folders(parent)
# save_to = '/home/nate/Documents/ODiSi/PIRO/pickle'
# test_name = 'au_sable_first_half'  

for folder in folders:
    current_folder = f"{parent}/{folder}"
    print(f"Working on {current_folder}\n")
    # get_data(current_folder,save_to,test_name)
      
    # read in .pkl files to dataframes
    # read_dir = os.path.join(save_to,f"{test_name}/",f"{folder}")
    # read_dir = "/home/nate/Documents/ODiSi/pickle/au_sable_first_half/024-09-18_20-2"
    
    # n_fibers = [f for f in os.listdir(current_folder) if f.endswith('full.tsv')]
    # n_fibers = len(n_fibers)
    
    # for x in range(n_fibers): # reads in each channel
    position = pd.read_pickle(f"{parent}/position/lighthouse_2024-09-30_19-36-28_ch{1}_full.tsv-position.pkl")
    values = pd.read_pickle(f"{parent}/values/lighthouse_2024-09-30_19-36-28_ch{1}_full.tsv-values.pkl")
    time = pd.read_pickle(f"{parent}/time/lighthouse_2024-09-30_19-36-28_ch{1}_full.tsv-time.pkl")
               
    # change dataframes to arrays
        
    position = position.values.flatten()
    time = time.values.flatten()
    time = time / (60*60*24) # conversion to minute, hour, or day
    values = values.values.T
        
#%% Split the data into day-sized chunks

n_measurements = int((1/10.4)*60*60*24)*3 # first term accoutns for sampling rate disreprancy. s to min to hour to 3 - day

split_shape = (len(position), n_measurements)

sub_arrays, (remainder_rows, remainder_cols, remainder_corner) = split_array_with_remainder(values, split_shape)

#%% Save each subarray as a .csv file.

for day in range(len(sub_arrays)):
    print(f'working on day {day+1}')
    df = pd.DataFrame(sub_arrays[day])
    df.to_csv(f"/home/nate/Documents/ODiSi/PIRO-days/three day/day {day+13} to {day+15}.csv")
    # if day == len(sub_arrays): # accounts for remainder
    #     df =  df = pd.DataFrame(remainder_cols)
    #     df.to_csv(f"/home/nate/Documents/ODiSi/PIRO-days/three day/day x.csv")