from __future__ import print_function
import codecs
import base64
import json
import sys
import os
import time
import shutil
import random
import argparse
import traceback

__version__ = '0.1.0'

def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='File Rename Utils v{0}'.format(__version__),
        epilog='''https://github.com/mcxiaoke/python-labs
        ''')
    mode_list = ['clean', 'delete', 'replace', 'prefix', 'suffix', 'extension']
    parser.add_argument('-r', '--regex', action='store_true', help='Enable Regex')
    parser.add_argument('-p', '--pattern', help='Match Pattern')
    parser.add_argument('-m', '--mode', type=str, choices=mode_list)
    parser.add_argument('-o', '--override', action='store_true', help='Override existing file.')
    args = parser.parse_args()
    print(args)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return args

def main():
    args = vars(parse_args())
    if args.get('album'):
        download_by_album(args['album'])
    elif args.get('doulist'):
        download_by_doulist(args['doulist'])
    elif args.get('userid'):
        download_by_user(args['userid'])

if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    main()

