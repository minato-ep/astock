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
    # Prepare Output Dir
    if not os.path.exists(os.path.join(path, 'analyse')):
        os.mkdir(os.path.join(path, 'analyse'))
    if not os.path.exists(os.path.join(path, 'analyse', 'irregular')):
        os.mkdir(os.path.join(path, 'analyse', 'irregular'))
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
    countSr = pd.Series(countList, index=dateList)
    sumSr = copy.copy(countSr)
    print('Prepared: ', round(time.time()-start, 2), ' sec')

    # Process csv data
    csvFileList = glob.glob(os.path.join(path, "*.csv"))
    pbar = tqdm.tqdm(total=len(csvFileList))
    devidedInfo = []
    for file in csvFileList:
        # Prepare Data
        devidedFlag = False
        csvData = pd.read_csv(file, usecols=('Date', 'Open'))
        csvNp = csvData.values
        # Detect Stock Division
        diff = np.diff(csvNp[:, 1])
        diff = np.insert(diff, 0, 0)
        ratio = diff/csvNp[:, 1]
        csvNp = np.hstack((csvNp, ratio.reshape(ratio.shape[0], 1)))
        for row in csvNp:
            if abs(row[2]) >= 0.90:
                name = os.path.splitext(os.path.basename(file))[0]
                devidedInfo.append(
                    {'id': name, 'date': row[0],
                     'value': row[1], 'ratio': row[2]})
                plt.figure()
                csvData.plot(x='Date')
                plt.title(row[0])
                plt.savefig(os.path.join(path, 'analyse',
                                         'irregular', name+'_'+row[0]+'.jpg'))
                devidedFlag = True
        if devidedFlag:
            pbar.update(1)
            continue
        # Get sum and count /day
        for val in csvNp:
            countSr[val[0]] += 1
            sumSr[val[0]] += val[1]
        pbar.update(1)
    pbar.close()
    print('Process: ', round(time.time()-start, 2), ' sec')

    # Finalize the result

    irregular = len(devidedInfo)
    if irregular != 0:
        pass
        print('Detected stock division. N=', irregular)
    print('Prcessed data: {}/{}'.format(len(csvFileList)-irregular,
                                        len(csvFileList)))
    # remove the market off day
    countSr = countSr[countSr != 0]
    countNp = countSr[countSr != 0].values
    sumNp = sumSr[sumSr != 0].values

    # calc mean
    meanNp = sumNp/countNp
    dfS = round(pd.Series(meanNp, index=countSr.index), 4)

    dfS.to_csv(os.path.join(path, 'analyse', 'result.csv'))
    with open(os.path.join(path, 'analyse', 'report.json'), mode='w') as f:
        report = {'total': len(csvFileList),
                  'processed': len(csvFileList)-irregular,
                  'irregular': devidedInfo}
        f.write(json.dumps(report, indent=2))
    print('ALL_TIME: ', round(time.time()-start, 2), ' sec')
    plt.figure(figsize=(16, 9), dpi=200)
    dfS.plot(x=dfS.index)
    #plt.plot(419, 1000, marker='|', color="red", markersize=200)
    plt.plot([419, 419], [1, 5000], "red", linestyle='dashed')
    title = os.path.splitext(os.path.basename(path))[0]
    plt.title('title')
    plt.savefig(os.path.join(path, 'analyse', title+'.jpg'))
