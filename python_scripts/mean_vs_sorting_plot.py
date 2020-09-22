# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data_path = '../../../data/'

file = 'PINWR_201407_GrainSizeStatistics.csv'


df= pd.read_csv(data_path+file, usecols=[0,1,2,3,4,5,6])


# Create a scatter plot of mean vs sorting:
plt.scatter(df['FWLogMean'], df['FWLogSort'])
plt.xlabel('Mean (phi)')
plt.ylabel('Sorting (phi)')
    

# assign group (control vs treatment) to each transect record:
df.loc[df['Transect'].str[0] == 'C', 'group'] = 'Control'
df.loc[df['Transect'].str[0] == 'T', 'group'] = 'Treatment'

# plot a new scatter plot of mean vs sorting,differentiating on
# group
sns.scatterplot(x='FWLogMean', y='FWLogSort', data=df,hue='group')

# can we see anything if we further parse the data in our plots
# based on beach position (e.g., lower swash, upper swash, dune toe)?

sns.catplot(x='FWLogMean', y='FWLogSort', hue='group', col='Sample', data=df)
plt.xlim(-1.0,2.0)
plt.xticks(rotation=90)
