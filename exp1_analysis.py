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

"""USER DEFINED FUNCTIONS"""

"""USEFULL VARIABLES"""
###DO NOT TOUCH###
CorrectResponse = 'C'
ErrorResponse = 'E'
DesiredErrorRate = 85
RawData = []
TrialTag = 'Main Group'
HeaderTag = 'Participant'
SubHeaderTag = 'Group'
Alpha = .05
###DO NOT TOUCH###

"""MAIN SCRIPT"""
# Set dir and desired import files
# Insert required path
Path = 'H:\\University of Roehampton\\Small grant GPs\\Experiments\\Session 1 GP13\\Experiment\\Data\\'
Files = [os.listdir(Path)]
DataFiles = []

# Open files and import data into variables
for f in Files[0]:
    if f.endswith('.txt'):
        DataFiles.append(f)

for f in DataFiles:
    File = os.path.join(Path, f)
    Data = open(File, 'r')
    # Filters imported data into different variables
    for line in Data.readlines():
        if line.startswith(TrialTag):
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

# Split rows into cells
RawData = [line.splitlines() for line in RawData]
RawData = [cell.split('\t') for line in RawData for cell in line]
Header = [Header.splitlines()]
Header = [word.split('\t') for line in Header for word in line]
SubHeader = [SubHeader.splitlines()]
SubHeader = [word.split('\t') for line in SubHeader for word in line]

# Merge headers for csv file
NewHeader = []

for a, b in zip(Header[0], SubHeader[0]):
    NewHeader.append(a+b)    

for a in SubHeader[0][12:]:
    NewHeader.append(a)

RawData.insert(0, NewHeader)
del Header, SubHeader
    
# Export and save rawdata set as excel worksheet
os.chdir(Path)
CsvOutput = np.asarray(RawData)
with open('RawData.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(CsvOutput)

# Pop Header and no responses for analysis
RawData.pop(0)    

"""Testing Distributions"""

# Pull data and adjust to required dtype
RTs = np.asarray(RawData)
RTs = RTs[:,11]
RTs = np.asarray(RTs, dtype=float)
# Display mean and std of all RTs
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

# Split data into GP/non-GP data sets and reduce to acc + error values
GPData = [row for row in RawData if row[13] == 'GP']
nonGPData = [row for row in RawData if row[13] == 'non-GP']
GPRTs = [row[11] for row in GPData]
nonGPRTs = [row[11] for row in nonGPData]
GPRTs = np.asarray(GPRTs, float)
nonGPRTs = np.asarray(nonGPRTs,float)

# Levene's test for homogeneity
stat, p = levene(GPRTs, nonGPRTs)
print('Statistics=%.3f, p=%.3f' % (stat, p))
if p > Alpha:
	print('Sample looks Gaussian')
else:
	print('Sample does not look Gaussian')

# Calculate and store error rate

"""Main Analysis"""

# Calculate and store means
GPRTMean = np.mean(GPRTs)
nonGPRTMean = np.mean(nonGPRTs)
print ("GP Mean RT: %.3f" % (GPRTMean))
print ("non GP MEan RT: %.3f" % (nonGPRTMean))

"""Plotting Main Analysis"""
