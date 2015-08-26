#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-26 07:50:34
from __future__ import print_function
import os
import sys
import subprocess


def git_pull_all(root):
    '''
    update all git repos in some root dir
    '''
    os.chdir(root)
    print('process repos in dir: {0}'.format(os.path.abspath(root)))
    dirs = os.listdir(root)
    for d in dirs:
        print('process repo:', d)
        os.chdir(os.path.join(root, d))
        if os.path.exists(os.path.join('.', '.git')):
            try:
                subprocess.check_call('git pull origin master')
            except Exception, e:
                print('unable to update repo {0}, error: {1}'.format(d, e))
        else:
            print('{} is not a git repo, skip'.format(d))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {0} repo_root_dir'.format(os.path.basename(sys.argv[0])))
        sys.exit()
    else:
        root = sys.argv[1]
        git_pull_all(root)
