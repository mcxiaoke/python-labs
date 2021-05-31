#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-07-10 08:42:07

# 一张iPhone拍摄的照片的EXIF信息

f=open('20150301_031903425_iOS.jpg','rb')
tags=exifread.process_file(f)
for tag in tags:
     if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
         print tag,'=',tags[tag]
'''
GPS GPSDate = 2015:03:01
EXIF ApertureValue = 7983/3509
Image ExifOffset = 208
EXIF LensMake = Apple
GPS GPSDestBearingRef = T
MakerNote Tag 0x0001 = 2
MakerNote Tag 0x0002 = [179, 0, 158, 0, 252, 0, 225, 0, 31, 1, 33, 1, 209, 0, 130, 0, 162, 0, 232, 0, ... ]
MakerNote Tag 0x0003 = [6, 7, 8, 85, 102, 108, 97, 103, 115, 85, 118, 97, 108, 117, 101, 85, 101, 112, 111, 99, ... ]
MakerNote Tag 0x0004 = 1
GPS GPSLatitudeRef = N
MakerNote Tag 0x0006 = 218
GPS GPSAltitudeRef = 0
Image DateTime = 2015:03:01 11:19:03
EXIF ShutterSpeedValue = 3833/350
EXIF ColorSpace = sRGB
EXIF MeteringMode = Pattern
EXIF ExifVersion = 0221
Image Software = 8.1.3
MakerNote Tag 0x000C = [64/83, 20/83]
EXIF ISOSpeedRatings = 32
Thumbnail YResolution = 72
GPS GPSSpeed = 0
GPS GPSLongitude = [116, 23, 289/25]
Image Orientation = Rotated 90 CCW
EXIF DateTimeOriginal = 2015:03:01 11:19:03
Image YCbCrPositioning = Centered
MakerNote Tag 0x0005 = 225
Thumbnail JPEGInterchangeFormat = 2042
EXIF ComponentsConfiguration = YCbCr
MakerNote Tag 0x0008 = [902/425, 5861/13, 64/33]
GPS GPSSpeedRef = K
Image Model = iPhone 6 Plus
EXIF ExifImageLength = 2448
EXIF SceneType = Directly Photographed
Image ResolutionUnit = Pixels/Inch
MakerNote Tag 0x000D = 0
EXIF ExposureTime = 1/1980
Thumbnail XResolution = 72
GPS GPSDestBearing = 21649/1480
MakerNote Tag 0x0010 = 1
Image GPSInfo = 1658
EXIF ExposureProgram = Program Normal
Thumbnail JPEGInterchangeFormatLength = 8161
EXIF Flash = Flash did not fire, compulsory flash mode
Thumbnail Compression = JPEG (old-style)
GPS GPSImgDirectionRef = T
EXIF ExposureMode = Auto Exposure
EXIF FocalLengthIn35mmFilm = 29
EXIF FlashPixVersion = 0100
EXIF ExifImageWidth = 3264
GPS GPSLatitude = [40, 0, 287/20]
EXIF SceneCaptureType = Standard
GPS GPSTimeStamp = [3, 19, 31/10]
EXIF SubjectArea = [1631, 1223, 1795, 1077]
EXIF LensSpecification = [83/20, 83/20, 11/5, 11/5]
EXIF SubSecTimeOriginal = 410
EXIF BrightnessValue = 7121/663
EXIF LensModel = iPhone 6 Plus back camera 4.15mm f/2.2
EXIF DateTimeDigitized = 2015:03:01 11:19:03
EXIF FocalLength = 83/20
GPS GPSImgDirection = 44959/231
Image XResolution = 72
Image Make = Apple
EXIF WhiteBalance = Auto
EXIF SubSecTimeDigitized = 410
Thumbnail ResolutionUnit = Pixels/Inch
Image YResolution = 72
MakerNote Tag 0x0007 = 1
GPS GPSLongitudeRef = E
EXIF FNumber = 11/5
MakerNote Tag 0x000E = 4
EXIF ExposureBiasValue = 0
EXIF SensingMethod = One-chip color area
GPS GPSAltitude = 41084/755
MakerNote Tag 0x000F = 3
'''
