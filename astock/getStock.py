import quandl as QD
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from os.path import join, exists
from os import mkdir
import tqdm
import config
import time
CONFIG = config.CONFIG
gType17 = None
# QUANDL ##### DATA IS LIMITED ~2017
# API DOCUMENT
# https://docs.quandl.com/docs/parameters-2
#
# QD.ApiConfig.api_key = "1ZghpHge9grykJ9Sygjt"
# quandl_data = QD.get()
# data = QD.get("EIA/PET_RWTC_D", start_date="2001-12-31", end_date="2001-12-31")
# print(type(data))
# print(data)

# Get Data


def getData(brandNp, type17):
    # Prepare
    number = brandNp.shape[0]
    estTime = [number*2, 'sec']
    estSize = [number * 50, number*120, 'kb']
    if estTime[0] >= 60:
        estTime[0] = round(estTime[0]/60, 2)
        estTime[1] = 'min'
    if estSize[1] >= 1000:
        estSize[0] = round(estSize[0]/1000, 2)
        estSize[1] = round(estSize[1]/1000, 2)
        estSize[2] = 'Mb'
    print('ESTIMATION')
    print('Num : {}'.format(number))
    print('Time: {} {}'.format(estTime[0], estTime[1]))
    print('Size: {}~{} {}'.format(estSize[0], estSize[1], estSize[2]))
    # yn = input('\nAre you sure? (y/n): ')
    # exit() if yn != 'y' else print('')
    pbar = tqdm.tqdm(total=number)

    for row in brandNp:
        try:
            data = QD.get("TSE/"+str(row[0]),
                          start_date="2000-04-01",
                          end_date="2018-04-02")
            p = join(CONFIG.outputDir, 'type17_' +
                     str(type17), str(row[0])+'.csv')
            # print(p)
            data.to_csv(p)
            pbar.update(1)
        except Exception:
            # print('id:{} has skipped. data does not exist.'.format(str(row[0])))
            pbar.update(1)
            continue
    pbar.close()


# Time
def getDataFrom17Type(type17):
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
    if not exists(join(CONFIG.outputDir, 'type17_'+str(type17))):
        mkdir(join(CONFIG.outputDir, 'type17_'+str(type17)))
    getData(typedJp1stBrNp, type17)
    print('ALL_TIME: ', round(time.time()-start, 2), ' sec')
