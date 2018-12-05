"""IMPORTS"""
import os
import matplotlib.pyplot as plt
import numpy as np
from numpy import mean
from  numpy import std
import csv
from statsmodels.graphics.gofplots import qqplot
from scipy.stats import shapiro
from scipy.stats import levene
from scipy.stats import normaltest

"""USEFUL VARIABLES"""
###DO NOT TOUCH
CorrectResponse = 'C'
IncorrectResponse = 'E'
DesiredError = 85
RawData = []
TrialTag = ['yes\n', 'no\n']
HeaderTag = 'Participant'
SubHeaderTag = 'Name'
NoReponseTag = 'NR'
Alpha = .05
###DO NOT TOUCH###

"""MAIN SCRIPT"""
# Set dir and import files
Path = 'C:\\Users\\Finbar.Duffy\\Desktop\\Fin experiments\\Session 2 1D\\Experiment\\Data\\'
Files = os.listdir(Path)
DataFiles = []

for f in Files:
    if f.endswith('.txt'):
        DataFiles.append(f)

# Open files and import data into variables
for f in DataFiles:
    File = os.path.join(Path, f)
    Data = open(File, 'r')
    # Filters imported data into different variables    
    for line in Data.readlines():
        if line.endswith(TrialTag[0]) or line.endswith(TrialTag[1]):
            RawData.append(line)
        elif line.startswith(HeaderTag):
            Header = line
        elif line.startswith(SubHeaderTag):
            SubHeader = line
        else:
            pass

# Reset and close file    
    Data.seek(0)
    Data.close
    
# Convert strings to lists 
RawData = [line.splitlines() for line in RawData]
RawData = [cell.split('\t') for line in RawData for cell in line]
Header = [Header.splitlines()]
Header = [word.split('\t') for line in Header for word in line]
SubHeader = [SubHeader.splitlines()]
SubHeader = [word.split('\t') for line in SubHeader for word in line]

# Mearge headers for csv export
NewHeader = []

for a, b in zip(Header[0], SubHeader[0]):
    NewHeader.append(a+b)    

for a in SubHeader[0][12:]:
    NewHeader.append(a)

RawData.insert(0, NewHeader)
del Header, SubHeader

# Convert Raw Data into np array 
# and export RawData as csv
os.chdir(Path)
with open('RawData_Exp2.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(RawData)

# Remove Header and no response trils for analysis
RawData.pop(0)
RawData = [line for line in RawData if line[10] != NoReponseTag]

"""Testing Distributions"""

# Pull required data and adjust dtype
RTs = np.asarray(RawData)
RTs = RTs[:,11]
RTs = np.asarray(RTs, dtype=float)
print('mean=%.3f stdv=%.3f' % (mean(RTs), std(RTs)))

# Plot hist and qq of RTs then run homogineity tests
plt.hist(RTs)
plt.show()
qqplot(RTs, line='s')
plt.show()

# Shapiro test of homogeneity
stat, p = shapiro(RTs)
print('Statistics=%.3f, p=%.3f' % (stat, p))
if p > Alpha:
	print('Sample looks Gaussian')
else:
	print('Sample does not look Gaussian')
    
# K2 test for skewness and kurtosis
stat, p = normaltest(RTs)
print('Statistics=%.3f, p=%.3f' % (stat, p))
if p > Alpha:
	print('Sample looks Gaussian')
else:
	print('Sample does not look Gaussian')

"""Main Analysis"""