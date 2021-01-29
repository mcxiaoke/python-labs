import os
import sys
import pprint
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import exiftool

RAW_FORMATS = ('.arw', '.nef', 'nrw', '.cr2', '.cr3', '.dng')
IMG_FORMATS = ('.jpg', '.jpeg', '.png', '.tiff','.heif','.heic')

# https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3

EXIF_DATE_TIME = '%Y:%m:%d %H:%M:%S'


def is_raw_image(filename):
    name = os.path.basename(filename)
    base, ext = os.path.splitext(name)
    return ext and ext.lower() in RAW_FORMATS


def is_normal_image(filename):
    name = os.path.basename(filename)
    base, ext = os.path.splitext(name)
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


def get_coordinates(geotags):
    lat = get_decimal_from_dms(
        geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(
        geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat, lon)


def get_img_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image.getexif()


def get_img_labeled_exif(fe):
    '''param: filename or exif object'''
    if isinstance(fe, str):
        exif = get_img_exif(fe)
    else:
        exif = fe
    labeled = {}
    if exif:
        for (key, val) in exif.items():
            labeled[TAGS.get(key)] = val
    return labeled


def get_date_time(filename):
    return get_raw_date_time(filename)
    '''
    name = os.path.basename(filename)
    base, ext = os.path.splitext(name)
    if ext and ext.lower() in IMG_FORMATS:
        return get_img_date_time(filename)
    elif ext and ext.lower() in RAW_FORMATS:
        return get_raw_date_time(filename)
    '''


def get_raw_date_time(filename):
    try:
        with exiftool.ExifTool() as et:
            tags = et.get_metadata(filename)
            dt_tag = tags["EXIF:DateTimeOriginal"] or tags["EXIF:DateTimeDigitized"] or tags["EXIF:DateTime"]
            # print('RAW: {} - {}'.format(dt_tag, filename))
            return datetime.strptime(
                dt_tag, EXIF_DATE_TIME)
    except Exception as e:
        print(e)


def get_img_date_time(filename):
    try:
        tags = get_img_labeled_exif(filename)
        dt_tag = tags.get('DateTimeOriginal') or tags.get(
            'DateTimeDigitized') or tags.get('DateTime')
        # print('IMG: {} - {}'.format(dt_tag, filename))
        return datetime.strptime(
            dt_tag, EXIF_DATE_TIME)
    except Exception as e:
        print(e)


def get_geotagging(fe):
    '''param: filename or exif object'''
    if isinstance(fe, str):
        exif = get_img_exif(fe)
    else:
        exif = fe
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                # raise ValueError("No EXIF geotagging found")
                return geotagging
            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging


def test_exif():
    filename = sys.argv[1]
    exif = get_img_exif(filename)
    labeled = get_img_labeled_exif(exif)
    pprint.pprint(labeled)
    print('------')
    geotags = get_geotagging(exif)
    pprint.pprint(geotags)
    print('------')
    pprint.pprint(get_coordinates(geotags))


if __name__ == "__main__":
    test_exif()
