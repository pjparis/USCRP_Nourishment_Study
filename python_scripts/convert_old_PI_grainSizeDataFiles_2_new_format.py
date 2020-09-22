#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 17:38:51 2020

@author: paulp
"""

# =============================================================================
# sheet_code	transect_ID	sample_ID	DISH WT (g)	WET WT (g)	DISH+DRY WT (g)	DRY WT (g)	
# 
# (-2.00Φ)+(-1.00Φ)	-2.00Φ	-1.00Φ	-0.50Φ	0Φ	0.5Φ	1.00Φ	1.25Φ	1.50Φ	1.75Φ	
# 
# 2.00Φ	2.50Φ	3.00Φ	3.50Φ	PAN
# 
# =============================================================================

import pandas as pd

file_path = '/Users/paulp/OneDrive - East Carolina University/Projects/USCRP_Pea_Island_2020_2021/data/2020_data/'
file_names = ['PINWR_201407_GrainSizeWeights.csv']     #PINWR_201608_GrainSizeWeights.csv

for file_name in file_names:
    df = pd.read_csv(file_path+file_name)
    
    # map values from old file to new format
    # open new excel file
    # write control sheet
    # write treatment or impact sheet
    cols = df.columns
    print(cols)