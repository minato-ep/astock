

import argparse
import config

CONFIG = config.CONFIG


def argsToConfig():
    global CONFIG
    parser = argparse.ArgumentParser(description='stoker')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='debug mode')
    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        help='debug mode')
    args = parser.parse_args()

    # update config
    if args.verbose or args.debug:
        CONFIG.debug = True
    CONFIG.finalize()
    return args


def init():
    argsToConfig()


def main():
    init()


if __name__ == '__main__':
    main()
