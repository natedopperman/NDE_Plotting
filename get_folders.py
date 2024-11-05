# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 13:38:50 2024

Written with GPT4
Prompt: Write some python code to get the name of all folders in a folder

@author: Nate
"""

import os

def get_folders(directory):
    # List comprehension to filter only directories
    folders = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    return folders

# Example usage
# directory_path = 'G:/Shared drives/GeoD/research/fiber_data/EGS_data/August_24_EGS/frac'
# folders = get_folders_in_directory(directory_path)
# print(folders)