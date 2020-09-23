#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: convert_old_PI_grainSizeDataFiles_2_new_format.py

Purpose: converts the old data/column formatting for te Pea Island Breach
Monitoring Project data to the new, 2020 format [standard] specification.

Created on: Mon Sep 21 17:38:51 2020
Initial coding completed on: Wednesday, Sep 23 11:28:XX 2020

@author: paulp

File Header String: sheet_code	transect_ID	sample_ID	DISH WT (g)	WET WT (g)
DISH+DRY WT (g)	DRY WT (g) (-2.00Φ)+(-1.00Φ)	-2.00Φ	-1.00Φ	-0.50Φ	0Φ
0.5Φ	1.00Φ	1.25Φ	1.50Φ	1.75Φ 2.00Φ	2.50Φ	3.00Φ	3.50Φ	PAN

Header applies to both the xlsx and csv formats
"""

# =============================================================================
# 
# =============================================================================

import os
import pandas as pd
import numpy as np


file_path = '../../../data/2014_data/'
file_names = ['PINWR_201407_GrainSizeWeights.csv',
              'PINWR_201409_GrainSizeWeights.csv',
              'PINWR_201608_GrainSizeWeights.csv',
              'PINWR_201702_GrainSizeWeights.csv',
              'PINWR_201704_GrainSizeWeights.csv',
              'PINWR_201708_GrainSizeWeights.csv']

for file_name in file_names:
    
    print('Processing file:', file_name)
    
    # split the current filename and its extension:
    name, ext = os.path.splitext(file_name)
    
    # build the data frame using the data from the current file:
    df = pd.read_csv(file_path+file_name)

    
    # extract survey date for ss name
    survey_date = df['sample_date'][0]
    month, day, year = survey_date.split('/')
    if(len(month) == 1):
        month = str(0)+month
    if(len(day) == 1):
        day = str(0)+day
        
    
    # replace NaNs in df with 0s:
    df.replace({np.nan: 0.0}, inplace=True)
    
    # create a new, derived column, PAN hat is the sum of phi_4 and remainder:
    df['PAN'] = df['phi_4'] + df['remainder']
    
    # drop the sample_date, phi_4, and remainder fields from df:
    df.drop(['sample_date','phi_4','remainder'], axis=1, inplace=True)
    
    
    # rename fields to match 2020 format:
    try:
        df.rename({'transect_id':'transect_ID',
               'sample_id':'sample_ID',
               'panWT':'DISH WT (g)',
               'pan+wetWT':'WET WT (g)',
               'pan+dryWT':'DISH+DRY WT (g)',
               'phi_-1':'-1.00Φ',
               'phi_-0,5':'-0.50Φ',
               'phi_0':'0Φ',
               'phi_0,5':'0.5Φ',
               'phi_1':'1.00Φ',
               'phi_1,25':'1.25Φ',
               'phi_1,5':'1.50Φ',
               'phi_1,75':'1.75Φ',
               'phi_2':'2.00Φ',
               'phi_2,5':'2.50Φ',
               'phi_3':'3.00Φ',
               'phi_3,5':'3.50Φ'}, axis='columns', inplace=True)
    except Exception as e:
        print('Oops! Trying to remap column names...', e)
 
    
    # add fields that were not a part of the original data;
    try:
        df.insert(loc=6, column='DRY WT (g)', value=df['DISH+DRY WT (g)']-df['DISH WT (g)'])
        df.insert(loc=7, column='(-2.00Φ)+(-1.00Φ)', value=0.0)
        df.insert(loc=8, column='-2.00Φ', value=0.0)
    except Exception as e:
        print('Oops! Trying to compute the DRY WT column values:', e)
        
        
    # adjust any dry weight values < 0 to 0:
    try:
        df.loc[df['DRY WT (g)'] < 0.0, 'DRY WT (g)'] = 0.0
    except Exception as e:
        print('Oops! Trying to reset any dry wts < 0 to 0', e)
        
        
    # create a new Excel spreadsheet with the adjusted df Control Transects Only:
    try:
        df_cntl = df.loc[df['transect_ID'].str[0] == 'C']
    
        # append the impact (treatment) transects to the spreadsheet:
        df_impt = df.loc[df['transect_ID'].str[0] == 'T']
    
        # write the data to the spreadsheet:
        ss_name = file_path+'PINWR_20'+year+'_'+month+day+'_GrainSizeWts.xlsx'
        
        with pd.ExcelWriter(ss_name) as writer:
            df_cntl.to_excel(writer, sheet_name='GrainSize_Control', 
                             index=False, float_format='%.2f')
            df_impt.to_excel(writer, sheet_name='GrainSize_Treatment', 
                             index=False, float_format='%.2f')
    
    except Exception as e:
        print('Oops!, Trying to write resultant data to Excel SSheets...', e)
        
        
    # create a new comma separated values (.csv) file for secondary storage
    # of data in new 2020 format
    try:
        csv_name = file_path+'PINWR_20'+year+'_'+month+day+'_GrainSizeWts.csv'
        df.to_csv(csv_name, index=False, float_format='%.2f')
    except Exception as e:
        print('Oops! Trying to write data to csv file.', e)