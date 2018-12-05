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
###DO NOT TOUCH###
CorrectResponse = 'C'
ErrorResponse = 'E'
DesiredErrorRate = 85
TrialTag = ['yes\n', 'no\n']
HeaderTag = 'Participant'
SubHeaderTag = 'Name'
RawData = []
###DO NOT TOUCH###

"""MAIN SCRIPT"""
# Set file paths and import desired files
Path = 'C:\\Users\\Finbar.Duffy\\Desktop\\Fin experiments\\Session 4 Faces\\Experiment\\Data\\'
Files = os.listdir(Path)
DataFiles = []

for f in Files:
    if f.endswith('.txt'):
        DataFiles.append(f)

# Import data from required files    
for f in DataFiles:
    f = os.path.join(Path, f)
    Data = open(f, 'r')
    
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

# Export RawData as csv
os.chdir(Path)
with open('RawData_Exp4.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(RawData)

# Remove header for ease of analysis
RawData.pop(0)

"""Testing Distributions"""

# Pull data and adjust to required dtype
Ratings = np.asarray(RawData)
Ratings = Ratings[:,6]
Ratings = np.asarray(Ratings, dtype=float)
# Display mean and std of all ratings
print('mean=%.3f stdv=%.3f' % (mean(Ratings), std(Ratings)))

# Plot Histogram of ratings
plt.hist(Ratings)
plt.show()

### Calclate mean attractiveness rating for each trial type ###
### and export in a format that can be copied into SPSS file ###