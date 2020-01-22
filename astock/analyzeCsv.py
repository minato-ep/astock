import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tqdm
import config
import time
import copy
import os
import json
from datetime import datetime, timedelta
CONFIG = config.CONFIG


def analyze(path):
    start = time.time()

    # Prepare DateList
    dateList = []
    # s = '2000/04/01'
    s = '2006/10/01'
    e = '2018/01/01'
    sD = datetime.strptime(s, '%Y/%m/%d')
    eD = datetime.strptime(e, '%Y/%m/%d')
    diff = (eD - sD).days + 1
    for i in range(diff):
        dateList.append((sD + timedelta(i)).strftime("%Y-%m-%d"))
    countList = [0] * len(dateList)
    dateDf = pd.Series(countList, index=dateList)
    dataSumDf = copy.copy(dateDf)
    print('Prepared: ', round(time.time()-start, 2), ' sec')

    # Process csv data
    csvFileList = glob.glob(os.path.join(path, "*.csv"))
    pbar = tqdm.tqdm(total=len(csvFileList))
    devidedInfo = []
    for file in csvFileList:
        # Prepare Data
        devidedFlag = False
        csvData = pd.read_csv(file).drop(
            ['High', 'Low', 'Close', 'Volume'], axis=1)
        csvNp = csvData.values
        # Detect Stock Division
        diff = np.diff(csvNp[:, 1])
        diff = np.insert(diff, 0, 0)
        ratio = diff/csvNp[:, 1]
        csvNp = np.hstack((csvNp, ratio.reshape(ratio.shape[0], 1)))
        for row in csvNp:
            if row[2] <= -0.90:
                name = os.path.splitext(os.path.basename(file))[0]
                devidedInfo.append((name, row[0], row[1], row[2]))
                devidedFlag = True
        if devidedFlag:
            continue
        # Get sum and count /day
        for val in csvNp:
            dateDf[val[0]] += 1
            dataSumDf[val[0]] += val[1]
        pbar.update(1)
    pbar.close()
    print('Process: ', round(time.time()-start, 2), ' sec')

    # Finalize the result
    if len(devidedInfo) != 0:
        print(json.dumps(devidedInfo, indent=2))

    # remove the market off day
    dataNumListNp = dateDf[dateDf != 0].values
    dataMeanListNp = dataSumDf[dataSumDf != 0].values

    # TODO make market off day removed df and use the columns to make dfS as index

    # calc mean
    s = dataMeanListNp/dataNumListNp
    dfS = pd.Series(s, index=dateDf)
    os.mkdir(os.path.join(path, 'analyse'))
    dfS.to_csv(os.path.join(path, 'analyse', 'result.csv'), index=False)
    with open(os.path.join(path, 'analyse', 'devidedStock.json'), mode='w') as f:
        f.write(json.dumps(devidedInfo, indent=2))
    print('ALL_TIME: ', round(time.time()-start, 2), ' sec')
    # plt.figure()
    # dfS.plot()
    # plt.show()
