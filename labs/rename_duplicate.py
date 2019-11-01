import os
import codecs
import sys
from os import path


def rename_duplicate(top_dir, dry_run=True):
    top = path.normcase(top_dir)
    for root, _, files in os.walk(top):
        for name in files:
            base, ext = path.splitext(name)
            if not ext or ext.lower() not in ['.jpg', 'jpeg', '.tiff']:
                continue
            print(base, ext)
            rel_path = path.join(root, name)
            src_path = path.abspath(rel_path)
            dst_name = "{}_1{}".format(base, ext)
            dst_path = path.join(root, dst_name)
            os.rename(src_path, dst_path)
            print("Rename {} to {}".format(name, dst_name))


if __name__ == "__main__":
    dry_run = len(sys.argv) < 3 or sys.argv[2] != "-e"
    rename_duplicate(sys.argv[1], dry_run)
