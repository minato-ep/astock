

import argparse
import config
import getStock

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


if __name__ == '__main__':
    main()