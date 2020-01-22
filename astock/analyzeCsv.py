import quandl as QD
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from os.path import join
import tqdm
import config
import time
CONFIG = config.CONFIG


start = time.time()
# Prepare API
QD.ApiConfig.api_key = "1ZghpHge9grykJ9Sygjt"
# Prepare Data
brandDf = pd.read_csv(
    join(CONFIG.resourceDir, 'brand.csv'), encoding="UTF-8")
brandNp = brandDf.values
# Clean up Data
brandNp = brandNp[brandNp[:, 3] != '-']
brandNp = brandNp[brandNp[:, 4] != '-']
# Select only 1st one
# marketList = (np.unique(brandNp[:, 2]))
jp1stBrNp = brandNp[brandNp[:, 2] == '市場第一部（内国株）']
# Select by 17types
typedJp1stBrNp = jp1stBrNp[jp1stBrNp[:, 4] == str(type17)]
print(typedJp1stBrNp.shape)
getData(typedJp1stBrNp)

print('ALL_TIME: ', round(time.time()-start, 2), ' sec')
