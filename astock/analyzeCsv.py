import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tqdm
import config
import time
from datetime import datetime, timedelta
CONFIG = config.CONFIG


start = time.time()
# Prepare DateList
dateList = []
#s = '2000/04/01'
s = '2005/01/01'
e = '2018/01/01'
sD = datetime.strptime(s, '%Y/%m/%d')
eD = datetime.strptime(e, '%Y/%m/%d')
diff = (eD - sD).days + 1
for i in range(diff):
    dateList.append((sD + timedelta(i)).strftime("%Y-%m-%d"))
countList = [0] * len(dateList)
#pre = [dateList, countList]
dataListDf = pd.Series(countList, index=dateList)
print(dataListDf)
#dateListNp = np.array(pre)
# Prepare csv data
csvFileList = glob.glob("/home/minato/stockData/type17_1/*")
pbar = tqdm.tqdm(total=len(csvFileList))
for file in csvFileList:
    dataNp = pd.read_csv(file)['Date'].values
    for val in dataNp:
        dataListDf[val] += 1
    pbar.update(1)
pbar.close()
print('ALL_TIME: ', round(time.time()-start, 2), ' sec')
plt.figure()
dataListDf.plot()
plt.show()
