'''
File: ebook_move.py
Created: 2021-03-06 21:13:08
Modified: 2021-03-06 21:13:10
Author: mcxiaoke (github@mcxiaoke.com)
License: Apache License 2.0
'''
import sys
import re
import shutil
from pathlib import Path


def contains_cjk(text):
    cjk_pattern = re.compile('[\u4e00-\u9fa5]+')
    return cjk_pattern.search(text)


def move_no_cjk(src):
    root = Path(src)
    no_cjk = Path(root).parent.joinpath('no_cjk')
    if not no_cjk.exists():
        no_cjk.mkdir(exist_ok=True)

    print('Root:', root)
    print('No_CJK:', no_cjk)

    for old_path in root.iterdir():
        if not old_path.is_file():
            continue
        if not contains_cjk(old_path.name):
            new_path = no_cjk.joinpath(old_path.name)
            print("From:", old_path)
            print("To:", new_path)
            try:
                old_path.rename(new_path)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    root = sys.argv[1]
    move_no_cjk(root)
