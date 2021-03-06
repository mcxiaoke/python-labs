'''
File: ebook_move.py
Created: 2021-03-06 21:13:08
Modified: 2021-03-06 21:13:10
Author: mcxiaoke (github@mcxiaoke.com)
License: Apache License 2.0
'''
import sys
import os
import re
import shutil


def contains_cjk(text):
    cjk_pattern = re.compile('[\u4e00-\u9fa5]+')
    return cjk_pattern.search(text)


def move_no_cjk(src):
    root = src
    no_cjk = os.path.join(os.path.dirname(root), 'no_cjk')
    if not os.path.exists(no_cjk):
        os.makedirs(no_cjk)

    names = [n for n in os.listdir(
        root) if os.path.isfile(os.path.join(root, n))]

    print('Root:', root)
    print('No_CJK:', no_cjk)

    for n in names:
        if not contains_cjk(n):
            old_path = os.path.join(root, n)
            new_path = os.path.join(no_cjk, n)
            print("From:", old_path)
            print("To:", new_path)
            try:
                shutil.move(old_path, new_path)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    root = sys.argv[1]
    move_no_cjk(root)
