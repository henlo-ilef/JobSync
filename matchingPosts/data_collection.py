# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 13:17:09 2023

@author: henloIlef
"""

import glassdoor_scraper as gs
import pandas as pd
path = "D:/HenloIlef/SUMMER 2K23/Internship SFS/matching_proj/app/operadriver_win64/operadriver.exe"

df = gs.get_jobs("software engineer", 1000, False, path, 14)
df.to_csv('glassdoor_jobs.csv', index = False)
df
