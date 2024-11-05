# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 11:19:15 2024

Version 0.2
Reads in OTS4 .txt files and extracts temperature, frequency, and amplitude data from all files.
Temperature data is saved as a .pkl file with time and temperature information.

####This line is added by Nate to test things.####

@author: Nate
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime

header = 14 # rows
p_row = 15 - 1 - header  # Adjusting for 0-based index in Python
t_row = 20 - 1 - header
f_row = 22 - 1 - header
a_row = 23 - 1 - header
time_row = 19 - 1 - header

# Specify the folder where the DTS .txt files are
my_folder = r"FOLDER PATH"

# Checks if the folder exists
if not os.path.isdir(my_folder):
    print(f"Error: The following folder does not exist:\n{my_folder}")
    my_folder = input("Please specify a new folder: ")
    if not os.path.isdir(my_folder):
        raise Exception("Invalid folder selected. Exiting.")

# Obtains all .txt files in the folder
the_files = [f for f in os.listdir(my_folder) if f.endswith('.txt')]

# Obtains the number of files
num_files = len(the_files)
print(f"There are {num_files} files to process.")
while input("Do you want to continue? Type 'y' to continue.\n") == "y":

    # Initialize variables
    t_values = []
    f_values = []
    a_values = []
    time_hist = []
    
    # Loop over the files
    # for k in range(min(100, num_files)): # uncomment this to make sure that the script extracts the data properly
    for k in range(num_files): # uncomment this to process all files in the folder.
        base_file_name = the_files[k]
        full_file_name = os.path.join(my_folder, base_file_name)
    
        # Display current progress
        print(f"Working on file {base_file_name} | #{k + 1}")
    
        # Read the file
        data = np.genfromtxt(full_file_name, delimiter='\n', dtype=str, skip_header=14)
    
        # Extract position, temperature, and time for the first file
        if k == 0:
            position = data[p_row].replace('|', ' ').split() # replace | with spaces to create a np array
            position = np.array(position, dtype=float)
            
            temperature = data[t_row].replace('|', ' ').split()[2:]  # Skips the first 2 entries 'Temperature' and 'profile'
            temperature = np.array(temperature, dtype=float)
    
            frequency = data[f_row].replace('|', ' ').split()[782:]  # Skips the first 3 entries 'Peak' 'frequency' 'profile' and internal measurements
            frequency = np.array(frequency, dtype=float)
            
            amplitude = data[f_row].replace('|', ' ').split()[782:]  # Skips the first 2 entries 'Amplitude' and 'profile'
            amplitude = np.array(amplitude, dtype=float)
    
            time_hist.append(data[time_row][1:21])
    
            t_values.append(temperature)
            f_values.append(frequency)
            a_values.append(amplitude)
            
        else:
            # Appends data for subsequent files
            temperature = data[t_row].replace('|', ' ').split()[2:]
            temperature = np.array(temperature, dtype=float)
    
            time_hist.append(data[time_row][1:21])
    
            t_values.append(temperature)
            f_values.append(frequency)
            a_values.append(amplitude)
    
    
    # Convert time history into datetime array
    time_hist = [''.join(row) for row in time_hist]  # Flatten nested lists if necessary
    time_hist = [datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ') for t in time_hist]
    

    
    print("All done.")
    break

# Compute elapsed time in seconds
dt = [(t - time_hist[0]).total_seconds() for t in time_hist]
    
# Combine elapsed time with measurement values
T = np.column_stack((dt, t_values))
F = np.column_stack((dt, f_values))
A = np.column_stack((dt, a_values))
    
# Create a DataFrame for easy manipulation
df_P = pd.DataFrame(position)
df_T = pd.DataFrame(T, columns=["ElapsedTime"] + [f"Temp_{i}" for i in range(1, T.shape[1])])
df_F = pd.DataFrame(F, columns=["ElapsedTime"] + [f"Frequency_{i}" for i in range(1, F.shape[1])])   
df_A = pd.DataFrame(A, columns=["ElapsedTime"] + [f"Amplitude{i}" for i in range(1, A.shape[1])]) 
    
# Saves the dataFrames to pickle files and creates a directory if it doesn't exist
directory = "SAVE DIRECTORY LOCATION"
os.makedirs(directory, exist_ok=True)

df_P_path = os.path.join(directory, "PIRO_DTS_locations.pkl")
df_T_path = os.path.join(directory, "PIRO_DTS.pkl")
df_F_path = os.path.join(directory, "PIRO_DTS_Freq.pkl")
df_A_path = os.path.join(directory, "PIRO_DTS_Amp.pkl")

df_P.to_pickle(df_P_path)
df_T.to_pickle(df_T_path)
df_F.to_pickle(df_F_path)
df_A.to_pickle(df_A_path)
