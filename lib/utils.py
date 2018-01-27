#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-25 08:45:45
from __future__ import unicode_literals, division, absolute_import, print_function
from datetime import datetime
import codecs
import os
import sys
import requests
import shutil
import string
import time
import json
import collections
import json
from collections import OrderedDict
from compat import urlparse, unquote, unicode_str, to_text, to_binary
from const import FILENAME_UNSAFE_CHARS


def import_src(name, fpath):
    import os
    import imp
    p = fpath if os.path.isabs(fpath) \
        else os.path.join(os.path.dirname(__file__), fpath)
    return imp.load_source(name, p)


def now():
    format_str = to_binary('%Y-%m-%d %H:%M:%S')
    return datetime.now().strftime(format_str)


def translator(from='', to='', delete='', keep=None):
    if len(to) == 1:
        to = to * len(from)
    trans = string.maketrans(from, to)
    if keep is not None:
        allchars = string.maketrans('', '')
        delete = allchars.translate(allchars, keep.translate(allchars, delete))

    def translate(s):
        return s.translate(trans, delete)
    return translate


def aes_encrypt(data, secret='P2wH6eFqd8x4abnf'):
    # https://pypi.python.org/pypi/pycrypto
    from Crypto.Cipher import AES
    aes = AES.new(secret, AES.MODE_CBC, b'2017011720370117')
    if isinstance(data, unicode):
        data = data.encode('utf-8')
    if len(data) % 16 != 0:
        data = data + str((16 - len(data) % 16) * '\0')
    return aes.encrypt(data)


def aes_decrypt(data, secret='P2wH6eFqd8x4abnf'):
    # https://pypi.python.org/pypi/pycrypto
    from Crypto.Cipher import AES
    aes = AES.new(secret, AES.MODE_CBC, b'2017011720370117')
    return aes.decrypt(data).rstrip('\0')


def load_json_preserve_order(s):
    return json.loads(s, object_pairs_hook=OrderedDict)

############################################################
#
# OS and System Functions
#
############################################################


def check_port_open(port, addr='127.0.0.1'):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((addr, port))
    if result == 0:
        return True
    else:
        return False


def get_user_home():
    home = os.curdir
    if 'HOME' in os.environ:
        home = os.environ['HOME']
    elif os.name == 'posix':
        home = os.path.expanduser("~/")
    elif os.name == 'nt':
        if 'HOMEPATH' in os.environ and 'HOMEDRIVE' in os.environ:
            home = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
    else:
        import pwd
        home = pwd.getpwuid(os.getuid()).pw_dir
    return home


def get_current_user():
    for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
        user = os.environ.get(name)
        if user:
            return user
    # If not user from os.environ.get()
    import pwd
    return pwd.getpwuid(os.getuid())[0]


def sanitize_filename(s, restricted=False, is_id=False):
    """Sanitizes a string so it could be used as part of a filename.
    If restricted is set, use a stricter subset of allowed characters.
    Set is_id if this is not an arbitrary string, but an ID that should be kept
    if possible.
    """
    def replace_insane(char):
        if restricted and char in ACCENT_CHARS:
            return ACCENT_CHARS[char]
        if char == '?' or ord(char) < 32 or ord(char) == 127:
            return ''
        elif char == '"':
            return '' if restricted else '\''
        elif char == ':':
            return '_-' if restricted else ' -'
        elif char in '\\/|*<>':
            return '_'
        if restricted and (char in '!&\'()[]{}$;`^,#' or char.isspace()):
            return '_'
        if restricted and ord(char) > 127:
            return '_'
        return char

    # Handle timestamps
    s = re.sub(r'[0-9]+(?::[0-9]+)+',
               lambda m: m.group(0).replace(':', '_'), s)
    result = ''.join(map(replace_insane, s))
    if not is_id:
        while '__' in result:
            result = result.replace('__', '_')
        result = result.strip('_')
        # Common case of "Foreign band name - English song title"
        if restricted and result.startswith('-_'):
            result = result[2:]
        if result.startswith('-'):
            result = '_' + result[len('-'):]
        result = result.lstrip('.')
        if not result:
            result = '_'
    return result


def sanitize_path(s):
    """Sanitizes and normalizes path on Windows"""
    if sys.platform != 'win32':
        return s
    drive_or_unc, _ = os.path.splitdrive(s)
    if sys.version_info < (2, 7) and not drive_or_unc:
        drive_or_unc, _ = os.path.splitunc(s)
    norm_path = os.path.normpath(remove_start(
        s, drive_or_unc)).split(os.path.sep)
    if drive_or_unc:
        norm_path.pop(0)
    sanitized_path = [
        path_part if path_part in ['.', '..'] else re.sub(
            r'(?:[/<>:"\|\\?\*]|[\s.]$)', '#', path_part)
        for path_part in norm_path]
    if drive_or_unc:
        sanitized_path.insert(0, drive_or_unc + os.path.sep)
    return os.path.join(*sanitized_path)

############################################################
#
# String/List/Dict Functions
#
############################################################


def slice_list(l, n):
    """Yield successive n-sized chunks from l."""
    # for i in xrange(0, len(l), n):
    #     yield l[i:i + n]
    return [l[i:i + n] for i in range(0, len(l), n)]


def distinct_list(source_list, sort=False, reverse=False):
    result_list = collections.OrderedDict(
        (x, True) for x in source_list).keys()
    return sorted(result_list, reverse=reverse) if sort else result_list


def flatten_list(source_list):
    result_list = []
    for item in source_list:
        if isinstance(item, list):
            result_list.extend(item)
        else:
            result_list.append(item)
    return [r for r in result_list if r]


############################################################
#
# File Functions
#
############################################################


def write_list(name, ls):
    if not ls:
        return
    with codecs.open(name, 'w', 'utf-8') as f:
        for s in ls:
            f.write(s + '\n')


def read_list(name):
    if not os.path.isfile(name):
        return []
    with codecs.open(name, 'r', 'utf-8') as f:
        return list(filter(bool, [line.strip() for line in f]))


def write_file(name, data):
    if not data:
        return
    with codecs.open(name, 'w', 'utf-8') as f:
        f.write(to_text(data))


def read_file(name):
    if not os.path.isfile(name):
        return None
    with codecs.open(name, 'r', 'utf-8') as f:
        return to_text(f.read())


def file_size(src):
    total_size = 0
    if os.path.isdir(src):
        for f in os.listdir(src):
            if os.path.isfile(f):
                total_size += os.path.getsize(f)
    elif os.path.isfile(src):
        total_size = os.path.getsize(src)
    return total_size


def files_size(files):
    return sum([os.path.getsize(f) for f in files])


def write_dict(name, dt):
    if not dt:
        return
    with codecs.open(name, 'w', 'utf-8') as f:
        json.dump(dt, f)


def read_dict(name):
    if not os.path.isfile(name):
        return {}
    with codecs.open(name, 'r', 'utf-8') as f:
        return json.load(f)

def humanize_bytes(n, precision=2):
    # Author: Doug Latornell
    # Licence: MIT
    # URL: http://code.activestate.com/recipes/577081/
    abbrevs = [
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'kB'),
        (1, 'B')
    ]

    if n == 1:
        return '1 B'

    for factor, suffix in abbrevs:
        if n >= factor:
            break

    # noinspection PyUnboundLocalVariable
    return '%.*f %s' % (precision, n / factor, suffix)

############################################################
#
# HTTP Functions
#
############################################################


def get_safe_filename(text):
    # text = text.replace(':', 'x')
    trans = translator(from=FILENAME_UNSAFE_CHARS, to='_')
    return trans(text).strip()


def url_to_filename(url):
    return get_safe_filename(urlparse(url).path)


def unquote_url(url):
    return unquote(url)


def requests_to_curl(r):
    req = r.request
    method = req.method
    uri = req.url
    ct = req.headers.get('Content-Type')
    data = '[multipart]' if ct and 'multipart/form-data' in ct else (
        req.body or '')
    headers = ["'{0}: {1}'".format(k, v) for k, v in req.headers.items()]
    headers = " -H ".join(headers)
    command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
    return command.format(method=method, headers=headers, data=data, uri=uri)
