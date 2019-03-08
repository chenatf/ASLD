#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 06:13:44 2018

@author: chenrui
"""

import sys
import pandas as pd
from collections import defaultdict

bed_path = sys.argv[1]
output_path = sys.argv[2]

depth = pd.read_table(bed_path,header=None,names=['chr','start','end','depth'])
table = defaultdict(int)
for i in range(len(depth['chr'])):
    chromosome = depth['chr'][i]
    table[chromosome] += depth['depth'][i]
table = pd.Series(table)
table.to_csv(output_path)