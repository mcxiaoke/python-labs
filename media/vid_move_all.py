import os
import sys
import shutil
import click
from os import path

VIDEO_EXTENSIONS = ('.mkv', '.mov', '.mp4', '.avi', '.wmv', '.m4v', '.flv')


def is_video(fp):
    base, ext = path.splitext(fp)
    return ext and ext.lower() in VIDEO_EXTENSIONS


@click.command()
@click.option('-r', '--real', default=False, show_default=True, is_flag=True,
              help='Execute command in real mode')
@click.argument('source', required=True, type=click.Path(exists=True, resolve_path=True, dir_okay=True, file_okay=False))
@click.argument('destination', type=click.Path(resolve_path=True, dir_okay=True, file_okay=False))
def move_videos(source, destination, real=False):
    '''Move all video files in source dir to destination dir.'''
    src = path.abspath(path.normpath(source))
    dst = destination or path.join(path.dirname(src), 'videos')
    if not path.exists(dst):
        os.mkdir(dst)
    dst = path.abspath(path.normpath(dst))
    print('SRC: {}'.format(src))
    print('DST: {}'.format(dst))
    for root, dirs, files in os.walk(src):
        for name in files:
            src_file = path.join(root, name)
            if is_video(src_file):
                # print('Process: {}'.format(src_file))
                print('Move {} to {}'.format(src_file, dst))
                if real:
                    shutil.move(src_file, dst)
            # else:
            # print('Not video {}'.format(src_file))


if __name__ == "__main__":
    move_videos()
