###############################################################################

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
NoReponseTag = 'NR'
Alpha = .05
Conditions = ['GP Short', 'GP Long', 'NonGP Short', 'NonGP Long']
###DO NOT TOUCH###

###############################################################################

"""MAIN SCRIPT""" 
# Set dir and desired import files
# Insert required path
Path = 'C:\\Users\\Finbar.Duffy\\Desktop\\Fin experiments\\Session 1 GP13\\Experiment\\Data'
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
with open('RawData_Exp1.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(RawData)

# Pop Header and no responses for analysis
RawData.pop(0)    
RawData = [line for line in RawData if line[10] != NoReponseTag]

"""Testing Distributions"""
# Pull data and adjust to required dtype
RTs = np.asarray(RawData)
RTs = RTs[:,11]
RTs = np.asarray(RTs, dtype=float)
# Display mean and std of all RTs
print('Overall RTs: mean=%.3f stdv=%.3f' % (mean(RTs), std(RTs)))

# Plot hist and qq of RTs
plt.hist(RTs)
plt.show()
qqplot(RTs, line='s')
plt.show()

# K2 test for skewness and kurtosis
print ('Testing skewness & kurtosis')
stat, p = normaltest(RTs)
print('K2 Statistics=%.3f, p=%.3f' % (stat, p))
if p > Alpha:
	print('Sample Gaussian')
else:
	print('Sample not Gaussian')

# Log transform RTs
logRTs = RTs
np.log(RTs, out=logRTs)

# qq plot log transformed RTs
print ('qq plot of log transformed RTs:')
qqplot(logRTs, line='s')
plt.show()

"""Main Anlayisis"""

# Split data into conditions and reduce to RT & error values
GPShortRTs = [row[11] for row in RawData if row[13]=='GP' and row[12]=='750']
GPLongRTs = [row[11] for row in RawData if row[13]=='GP' and row[12]=='1500']
nonGPShortRTs = [row[11] for row in RawData if row[13]=='non-GP' and row[12]=='750']
nonGPLongRTs = [row[11] for row in RawData if row[13]=='non-GP' and row[12]=='1500']
GPShortRTs = np.asarray(GPShortRTs, dtype=float)
GPLongRTs = np.asarray(GPLongRTs, dtype=float)
nonGPShortRTs = np.asarray(nonGPShortRTs, dtype=float)
nonGPLongRTs = np.asarray(nonGPLongRTs, dtype=float)

# Plot RT means  and stds
ConditionRTstds = [std(GPShortRTs), std(GPLongRTs), std(nonGPShortRTs), std(nonGPLongRTs)]
ConditionRTMeans = [mean(GPShortRTs), mean(GPLongRTs), mean(nonGPShortRTs), mean(nonGPLongRTs)]
plt.bar(Conditions, ConditionRTMeans, yerr=ConditionRTstds)
plt.xlabel('Condition')
plt.ylabel('RT Means')
plt.show()

# Print RT means and stds for each condition
print('GP Short: mean=%.3f stdv=%.3f' % (mean(GPShortRTs), std(GPShortRTs)))
print('GP Long: mean=%.3f stdv=%.3f' % (mean(GPLongRTs), std(GPLongRTs)))
print('nonGP Short: mean=%.3f stdv=%.3f' % (mean(nonGPShortRTs), std(nonGPShortRTs)))
print('nonGP Long: mean=%.3f stdv=%.3f' % (mean(nonGPLongRTs), std(nonGPLongRTs)))

# Levene's test for homogeneity
stat, p = levene(GPShortRTs, GPLongRTs, nonGPShortRTs, nonGPLongRTs)
print('Levene Statistics=%.3f, p=%.3f' % (stat, p))
if p > Alpha:
	print('Sample looks Gaussian')
else:
	print('Sample does not look Gaussian')
