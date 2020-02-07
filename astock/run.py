import argparse
import config
import getStock
import analyzeCsv
from mutils import stockutil, fileutil, kaggleutil, graphutil
CONFIG = config.CONFIG


def argsToConfig():
    global CONFIG
    parser = argparse.ArgumentParser(description='stoker')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='debug mode')
    args = parser.parse_args()

    # update config
    if args.verbose:
        CONFIG.debug = True
    return args


def main():
    argsToConfig()
    fp = '/home/minato/stockData/type17_3/1433.csv'
    df1 = fileutil.readCsvAsDf(fp, header=['Date', 'Open'])
    graphutil.linePlot(df1, xName='Date', yNameList=['Open'])
    df2 = stockutil.removeDiv(df1)
    graphutil.linePlot(df2, xName='Date', yNameList=['Open'])


if __name__ == '__main__':
    main()
