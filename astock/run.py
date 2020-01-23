import argparse
import config
import getStock
import analyzeCsv
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
    for i in range(10, 18):
        print(i)
        id17 = i
        getStock.getDataFrom17Type(id17)
        analyzeCsv.analyze('/home/minato/stockData/type17_'+str(id17))


if __name__ == '__main__':
    main()
