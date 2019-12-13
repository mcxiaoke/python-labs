import os
import sys
import pprint
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3

_EXIF_DATE_TIME = '%Y:%m:%d %H:%M:%S'


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


def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image.getexif()


def get_labeled_exif(fe):
    '''param: filename or exif object'''
    if isinstance(fe, str):
        exif = get_exif(fe)
    else:
        exif = fe
    labeled = {}
    if exif:
        for (key, val) in exif.items():
            labeled[TAGS.get(key)] = val
    return labeled


def get_date_time(filename):
    try:
        tags = get_labeled_exif(filename)
        dt_tag = tags.get('DateTimeOriginal') or tags.get(
            'DateTimeDigitized') or tags.get('DateTime')
        return datetime.strptime(
            dt_tag, _EXIF_DATE_TIME)
    except Exception as e:
        pass
        # print(e)


def get_geotagging(fe):
    '''param: filename or exif object'''
    if isinstance(fe, str):
        exif = get_exif(fe)
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
    exif = get_exif(filename)
    labeled = get_labeled_exif(exif)
    pprint.pprint(labeled)
    print('------')
    geotags = get_geotagging(exif)
    pprint.pprint(geotags)
    print('------')
    pprint.pprint(get_coordinates(geotags))


if __name__ == "__main__":
    test_exif()
