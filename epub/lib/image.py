#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke

import os
import sys
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def get_text_dimensions(textString, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(textString).getbbox()[2]
    text_height = font.getmask(textString).getbbox()[3] + descent

    return (text_width, text_height)


def create_cover(img_path, title, info, cover_file):
    img = Image.open(img_path)
    imgW, imgH = img.size

    maxWidth = round(imgW * 0.85)
    draw = ImageDraw.Draw(img)
    color = (255, 255, 255)

    titleFontSize = 120
    titleText = title
    # simhei.ttf simsun.ttc simsunb.ttf msyh.ttc msyhbd.ttc
    titleFontName = "msyh.ttc"
    titleFont = ImageFont.truetype(titleFontName, titleFontSize)
    titleW, titleH = get_text_dimensions(titleText, titleFont)

    while titleW > maxWidth:
        titleFontSize = titleFontSize - 8
        titleFont = ImageFont.truetype(titleFontName, titleFontSize)
        titleW, titleH = get_text_dimensions(titleText, titleFont)
    titleX = (imgW - titleW) / 2
    titleY = (imgH - titleH) / 4 - titleH

    infoText = info
    infoFontSize = round(titleFontSize * 0.6)
    infoFont = ImageFont.truetype(titleFontName, infoFontSize)
    infoW, infoH = get_text_dimensions(infoText, infoFont)
    infoX = (imgW - infoW) / 2
    infoY = imgH - (imgH - infoH) / 4

    # Add Text to an image
    draw.text((titleX, titleY), titleText, font=titleFont, fill=color)
    draw.text((infoX, infoY), infoText, font=infoFont, fill=color)

    cover_dir = os.path.dirname(cover_file)
    if not os.path.exists(cover_dir):
        os.makedirs(cover_dir)

    img.save(cover_file)
    return cover_file


# if __name__ == "__main__":
#     img = drawTextOnImage(os.path.abspath(r"epub\cover\cover_04.jpg"))
#     img.show()
#     img.save(r"F:\Temp\testimg.jpg")
