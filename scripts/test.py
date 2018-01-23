from __future__ import unicode_literals, division, absolute_import, print_function
import os
import sys
import codecs
import shutil
import traceback
import subprocess

def run_enca(root, dry_run=False):
    root = upath.abspath(root)
    log = codecs.open('../a.txt', 'w', 'utf-8')
    for curdir, subdirs, filenames in os.walk(root, topdown=True):
        for name in filenames:
            try:
                f = os.path.join(curdir,name)
                r = subprocess.check_output(['enca', f], stderr=subprocess.STDOUT)
                r = compat.to_text(r)
                log.write('%s - %s' % (f,r))
                print('%s - %s' % (f,r))
            except Exception as e:
                traceback.print_stack()
                os.remove(f)


if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    from lib import compat, upath
    run_enca(sys.argv[1])