# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:38:03 2024

Reads in ODiSi strain data and creates directories to save data.
Written with GPT assistance

@author: Nate
"""

import os
from quickParseODiSI import parse_data
import pandas as pd


def get_data(my_folder = None,save_to=None):
   # Check if the folder exists
   if my_folder is None:
       my_folder = input("Please specify a folder: ")
   
   if not os.path.isdir(my_folder):
       print(f"The specified folder does not exist: {my_folder}")
       create = input("Would you like to create this folder? (yes/no): ")
       
       if create.lower() == 'yes':
           os.makedirs(my_folder)
           print(f"Folder created: {my_folder}")
       else:
           raise Exception("Invalid folder selected. Exiting.")
    
    # List all .txt files in the folder
   the_files = [f for f in os.listdir(my_folder) if f.endswith('full.tsv')]
    
    # Get the number of files
   num_files = len(the_files)
   print(f"There are {num_files} files to process.")
   while input("Do you want to continue? Type 'y' to continue.\n") == "y":
    
        
        # Loop over the files
        # for k in range(min(100, num_files)): # commented out for dev (add prompt for # of files to process for QC purposes)
       for k in range(num_files):
           base_file_name = the_files[k]
           full_file_name = os.path.join(my_folder, base_file_name)
         
            # Display current progress
           print(f"Working on file {base_file_name} | #{k + 1}")              
             
           data = parse_data(f"{full_file_name}") # make sure there is a tare
                           
           time = data['Time']
           values = data['Data']['Values']
           position = data['Location']['Location_Values']
                    
            # Convert to DataFrames if not already
           time = pd.DataFrame(time)
           position = pd.DataFrame(position)
           values = pd.DataFrame(values)
            
            # Fill NaN with O
           values = values.fillna(0)
            
           # Creates folders for each dataset extracted
           subdirs = ['time', 'position', 'values']
           
           for subdir in subdirs:
               dir_path = os.path.join(save_to, subdir)
               
               if not os.path.exists(dir_path):
                   os.makedirs(dir_path)
                   print(f"Subdirectory created: {dir_path}")
               else:
                   print(f"Subdirectory already exists: {dir_path}")
            
            # Save the files as a pickle
           time.to_pickle(f"{save_to}/time/{base_file_name}-time.pkl")
           position.to_pickle(f'{save_to}/position//{base_file_name}-position.pkl')
           values.to_pickle(f'{save_to}/values/{base_file_name}-values.pkl')
       break
        
get_data(r"/home/nate/Documents/ODiSi/PIRO/second half",'/home/nate/Documents/ODiSi/Test Folder')
        

                
