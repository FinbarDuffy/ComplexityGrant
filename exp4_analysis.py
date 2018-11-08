"""Import Modules"""
import os
import numpy as np
import os.path as path
import matplotlib.pyplot as plt
import csv

"""Coded Variables"""
CorrectResponse = 'C'
ErrorResponse = 'E'
DesiredErrorRate = 85

"""Main Script"""
# Set file paths and import desired files
Path = '' # Insert path as required
Files = [os.listdir(Path)]
DataFiles = []

for f in Files:
    if f.endswith('.txt'):
        DataFiles.append(f)

# Import data from required files    
for f in DataFiles:
    f = path.join(Path, f)
    Data = open(f, 'r')
    
    