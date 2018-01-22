#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import math
import logging
import hashlib
import datetime
import socket
import base64
import warnings
import threading

from compat import iteritems, text_type, binary_type, string_types

md5string = lambda x: hashlib.md5(utf8(x)).hexdigest()


class ReadOnlyDict(dict):
    """A Read Only Dict"""

    def __setitem__(self, key, value):
        raise Exception("dict is read-only")


def getitem(obj, key=0, default=None):
    """Get first element of list or return default"""
    try:
        return obj[key]
    except:
        return default

def run_in_thread(func, *args, **kwargs):
    """Run function in thread, return a Thread object"""
    from threading import Thread
    thread = Thread(target=func, args=args, kwargs=kwargs)
    thread.daemon = True
    thread.start()
    return thread

def run_in_subprocess(func, *args, **kwargs):
    """Run function in subprocess, return a Process object"""
    from multiprocessing import Process
    thread = Process(target=func, args=args, kwargs=kwargs)
    thread.daemon = True
    thread.start()
    return thread

def utf8(string):
    """
    Make sure string is utf8 encoded bytes.

    If parameter is a object, object.__str__ will been called before encode as bytes
    """
    if isinstance(string, text_type):
        return string.encode('utf8')
    elif isinstance(string, binary_type):
        return string
    else:
        return text_type(string).encode('utf8')


def text(string, encoding='utf8'):
    """
    Make sure string is unicode type, decode with given encoding if it's not.

    If parameter is a object, object.__str__ will been called
    """
    if isinstance(string, text_type):
        return string
    elif isinstance(string, binary_type):
        return string.decode(encoding)
    else:
        return text_type(string)


def pretty_unicode(string):
    """
    Make sure string is unicode, try to decode with utf8, or unicode escaped string if failed.
    """
    if isinstance(string, text_type):
        return string
    try:
        return string.decode("utf8")
    except UnicodeDecodeError:
        return string.decode('Latin-1').encode('unicode_escape').decode("utf8")


def unicode_string(string):
    """
    Make sure string is unicode, try to default with utf8, or base64 if failed.

    can been decode by `decode_unicode_string`
    """
    if isinstance(string, text_type):
        return string
    try:
        return string.decode("utf8")
    except UnicodeDecodeError:
        return '[BASE64-DATA]' + base64.b64encode(string) + '[/BASE64-DATA]'

def unicode_dict(_dict):
    """
    Make sure keys and values of dict is unicode.
    """
    r = {}
    for k, v in iteritems(_dict):
        r[unicode_obj(k)] = unicode_obj(v)
    return r


def unicode_list(_list):
    """
    Make sure every element in list is unicode. bytes will encode in base64
    """
    return [unicode_obj(x) for x in _list]


def unicode_obj(obj):
    """
    Make sure keys and values of dict/list/tuple is unicode. bytes will encode in base64.

    Can been decode by `decode_unicode_obj`
    """
    if isinstance(obj, dict):
        return unicode_dict(obj)
    elif isinstance(obj, (list, tuple)):
        return unicode_list(obj)
    elif isinstance(obj, string_types):
        return unicode_string(obj)
    elif isinstance(obj, (int, float)):
        return obj
    elif obj is None:
        return obj
    else:
        try:
            return text(obj)
        except:
            return text(repr(obj))


def decode_unicode_string(string):
    """
    Decode string encoded by `unicode_string`
    """
    if string.startswith('[BASE64-DATA]') and string.endswith('[/BASE64-DATA]'):
        return base64.b64decode(string[len('[BASE64-DATA]'):-len('[/BASE64-DATA]')])
    return string


def decode_unicode_obj(obj):
    """
    Decode unicoded dict/list/tuple encoded by `unicode_obj`
    """
    if isinstance(obj, dict):
        r = {}
        for k, v in iteritems(obj):
            r[decode_unicode_string(k)] = decode_unicode_obj(v)
        return r
    elif isinstance(obj, string_types):
        return decode_unicode_string(obj)
    elif isinstance(obj, (list, tuple)):
        return [decode_unicode_obj(x) for x in obj]
    else:
        return obj

# Python 2.X commandline parsing under Windows has been horribly broken for years!
# Use the following code to emulate full unicode commandline parsing on Python 2
# ie. To get  sys.argv arguments and properly encode them as unicode
def unicode_argv():
    if PY3:
        return sys.argv
    if OS_WIN:
        # Versions 2.x of Python don't support Unicode in sys.argv on
        # Windows, with the underlying Windows API instead replacing multi-byte
        # characters with '?'.  So use shell32.GetCommandLineArgvW to get sys.argv
        # as a list of Unicode strings
        from ctypes import POINTER, byref, cdll, c_int, windll
        from ctypes.wintypes import LPCWSTR, LPWSTR

        GetCommandLineW = cdll.kernel32.GetCommandLineW
        GetCommandLineW.argtypes = []
        GetCommandLineW.restype = LPCWSTR

        CommandLineToArgvW = windll.shell32.CommandLineToArgvW
        CommandLineToArgvW.argtypes = [LPCWSTR, POINTER(c_int)]
        CommandLineToArgvW.restype = POINTER(LPWSTR)

        cmd = GetCommandLineW()
        argc = c_int(0)
        argv = CommandLineToArgvW(cmd, byref(argc))
        if argc.value > 0:
            # Remove Python executable and commands if present
            start = argc.value - len(sys.argv)
            return [argv[i] for i in
                    range(start, argc.value)]
        # this should never happen
        return None
    else:
        argv = []
        argvencoding = sys.stdin.encoding
        if argvencoding is None:
            argvencoding = sys.getfilesystemencoding()
        if argvencoding is None:
            argvencoding = 'utf-8'
        for arg in sys.argv:
            if isinstance(arg, text_type):
                argv.append(arg)
            else:
                argv.append(arg.decode(argvencoding))
        return argv