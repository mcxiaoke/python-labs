#!/usr/bin/env python
import os
import sys
import pprint
import traceback
from datetime import datetime
import exiftool

RAW_FORMATS = ('.arw', '.nef', 'nrw', '.cr2', '.cr3', '.dng')
IMG_FORMATS = ('.jpg', '.jpeg', '.png', '.tiff', '.heif', '.heic')
VID_FORMATS = ('.mov', '.mp4', '.m4v', '.mkv')
MEDIA_FORMATS = RAW_FORMATS + IMG_FORMATS + VID_FORMATS

# https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3

EXIF_DATE_TIME = '%Y:%m:%d %H:%M:%S'
EXIF_DATE_TIME_MS = '%Y:%m:%d %H:%M:%S.%f'

_et = None

# batch mode for performance


def exif_begin():
    global _et
    if not _et:
        _et = exiftool.ExifTool()
    if not _et.running:
        _et.start()


def exif_end():
    global _et
    if _et.running:
        _et.terminate()


def get_prefix(filename):
    name = os.path.basename(filename)
    base, ext = os.path.splitext(name)
    ext = ext and ext.lower()
    if ext in IMG_FORMATS:
        return "IMG_"
    elif ext in RAW_FORMATS:
        return "DSC_"
    elif ext in VID_FORMATS:
        return "VID_"
    else:
        return "ERR_"


def is_video(filename):
    name = os.path.basename(filename)
    _, ext = os.path.splitext(name)
    return ext and ext.lower() in VID_FORMATS


def is_raw_image(filename):
    name = os.path.basename(filename)
    _, ext = os.path.splitext(name)
    return ext and ext.lower() in RAW_FORMATS


def is_normal_image(filename):
    name = os.path.basename(filename)
    _, ext = os.path.splitext(name)
    return ext and ext.lower() in IMG_FORMATS


def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)


def get_date_tag(filename):
    exif_begin()
    try:
        tags = _et.get_metadata(filename)
    except Exception as e:
        # print('Error: No Exif {}'.format(os.path.basename(filename)))
        return
    try:
        if not tags:
            return
        # video file
        if is_video(filename):
            # sony ilce-6300 only video tag
            dt_name = "XML:CreationDateValue"
            dt_value = tags.get(dt_name)
            if not dt_value:
                # iphone only video tag
                dt_name = "QuickTime:CreationDate"
                dt_value = tags.get(dt_name)
            if not dt_value:
                # mp4 and mov video common tag
                dt_name = "QuickTime:CreateDate"
                dt_value = tags.get(dt_name)
        # image file
        else:
            # photo exif tag [with millis]
            # iphone and xiaomi and nikon
            dt_name = 'Composite:SubSecDateTimeOriginal'
            dt_value = tags.get(dt_name)
            if not dt_value:
                dt_name = 'Composite:SubSecCreateDate'
                dt_value = tags.get(dt_name)
            if not dt_value:
                dt_name = "EXIF:DateTimeOriginal"
                dt_value = tags.get(dt_name)
            if not dt_value:
                dt_name = "EXIF:DateTimeDigitized"
                dt_value = tags.get(dt_name)
            if not dt_value:
                dt_name = "EXIF:CreateDate"
                dt_value = tags.get(dt_name)
        if dt_value and '0000' in dt_value:
            print('[{}] Invalid TAG:{}'.format(
                os.path.basename(filename), dt_value))
            dt_value = None
        # last using file date
        if not dt_value:
            dt_name = "File:FileModifyDate"
            dt_value = dt_value = tags.get(dt_name)
        if dt_value and '+' in dt_value:
            dt_value = dt_value.split('+')[0]
        # print("[{}] Using TAG '{}':'{}'".format(
        #     os.path.basename(filename), dt_name, dt_value))
        # show_exif(filename, 'date')
        return dt_value
    except Exception as e:
        # print('Error: Unknwon Error {}'.format(os.path.basename(filename)))
        return


def get_date_time(filename):
    tag = get_date_tag(filename)
    return tag and datetime.strptime(tag, EXIF_DATE_TIME_MS
                                     if '.' in tag else EXIF_DATE_TIME)


def show_exif(source, tag_filter=None):
    exif_begin()
    if os.path.isdir(source):
        filenames = os.listdir(source)
    elif os.path.isfile(source):
        filenames = [source]
    else:
        return
    try:
        for filename in filenames:
            print('====== {} ======'.format(os.path.basename(filename)))
            tags = _et.get_metadata(filename)
            if tag_filter:
                for k in tags.keys():
                    if tag_filter.lower() in k.lower():
                        print("  '{}': '{}'".format(k, tags[k]))
            else:
                pprint.pprint(tags)
    except Exception as e:
        print(e)
    exif_end()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} file_path tag_filter'.format(sys.argv[0]))
        sys.exit(1)
    if len(sys.argv) > 2:
        tag_filter = sys.argv[2]
    else:
        tag_filter = None
    print(sys.argv)
    show_exif(sys.argv[1], tag_filter)


'''
ExifTool Date Time Sample

========== IMG_20210128_102436.HEIC 2021:01:28 10:24:36 ==========
File:FileModifyDate: 2021:01:28 10:24:34+08:00
File:FileAccessDate: 2021:02:18 13:31:58+08:00
File:FileInodeChangeDate: 2021:02:18 13:31:54+08:00
EXIF:ModifyDate: 2021:01:28 10:24:36
EXIF:DateTimeOriginal: 2021:01:28 10:24:36
EXIF:CreateDate: 2021:01:28 10:24:36
EXIF:GPSDateStamp: 2021:01:28
ICC_Profile:ProfileDateTime: 2017:07:07 13:22:32
Composite:SubSecCreateDate: 2021:01:28 10:24:36.095+08:00
Composite:SubSecDateTimeOriginal: 2021:01:28 10:24:36.095+08:00
Composite:SubSecModifyDate: 2021:01:28 10:24:36+08:00
------------------------------
========== _DSC1751.NEF 2021:02:17 10:26:35 ==========
File:FileModifyDate: 2021:02:17 10:26:36+08:00
File:FileAccessDate: 2021:02:18 13:29:03+08:00
File:FileInodeChangeDate: 2021:02:18 13:29:01+08:00
EXIF:ModifyDate: 2021:02:17 10:26:35
EXIF:CreateDate: 2021:02:17 10:26:35
EXIF:DateTimeOriginal: 2021:02:17 10:26:35
MakerNotes:DateDisplayFormat: 0
Composite:SubSecCreateDate: 2021:02:17 10:26:35.30
Composite:SubSecDateTimeOriginal: 2021:02:17 10:26:35.30
Composite:SubSecModifyDate: 2021:02:17 10:26:35.30
------------------------------
========== _DSC7970.ARW 2021:02:17 09:53:46 ==========
File:FileModifyDate: 2021:02:17 09:53:46+08:00
File:FileAccessDate: 2021:02:18 13:28:43+08:00
File:FileInodeChangeDate: 2021:02:18 13:28:41+08:00
EXIF:DateTimeOriginal: 2021:02:17 09:53:46
EXIF:CreateDate: 2021:02:17 09:53:46
EXIF:ModifyDate: 2021:02:17 09:53:46
MakerNotes:SonyDateTime: 2021:02:17 09:53:46
========== VID_20210125_093918.MOV 2021:01:25 09:39:18 ==========
File:FileModifyDate: 2021:01:25 17:39:18+08:00
File:FileAccessDate: 2021:02:13 20:41:15+08:00
File:FileInodeChangeDate: 2021:02:18 13:31:26+08:00
QuickTime:CreateDate: 2021:01:25 09:39:18
QuickTime:ModifyDate: 2021:01:25 09:39:35
QuickTime:TrackCreateDate: 2021:01:25 09:39:18
QuickTime:TrackModifyDate: 2021:01:25 09:39:35
QuickTime:MediaCreateDate: 2021:01:25 09:39:18
QuickTime:MediaModifyDate: 2021:01:25 09:39:35
QuickTime:CreationDate: 2021:01:25 17:39:18+08:00
------------------------------
========== VID_20210216_013703.MP4 2021:02:16 01:37:03 ==========
File:FileModifyDate: 2021:02:16 09:37:24+08:00
File:FileAccessDate: 2021:02:18 10:39:08+08:00
File:FileInodeChangeDate: 2021:02:18 13:30:06+08:00
QuickTime:CreateDate: 2021:02:16 01:37:03
QuickTime:ModifyDate: 2021:02:16 01:37:03
QuickTime:TrackCreateDate: 2021:02:16 01:37:03
QuickTime:TrackModifyDate: 2021:02:16 01:37:03
QuickTime:MediaCreateDate: 2021:02:16 01:37:03
QuickTime:MediaModifyDate: 2021:02:16 01:37:03
XML:LastUpdate: 2021:02:16 09:37:03+08:00
XML:CreationDateValue: 2021:02:16 09:37:03+08:00
------------------------------
'''
