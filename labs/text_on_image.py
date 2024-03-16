#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke

import os
import sys
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def getTextDimensions(textString, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(textString).getbbox()[2]
    text_height = font.getmask(textString).getbbox()[3] + descent

    return (text_width, text_height)


def drawTextOnImage(imgPath):
    img = Image.open(imgPath)
    imgW, imgH = img.size

    maxWidth = round(imgW * 0.9)
    draw = ImageDraw.Draw(img)
    color = (255, 255, 255)

    titleFontSize = 120
    titleText = "LLMedium2-01"
    # simhei.ttf simsun.ttc simsunb.ttf msyh.ttc msyhbd.ttc
    titleFontName = "msyh.ttc"
    titleFont = ImageFont.truetype(titleFontName, titleFontSize)
    titleW, titleH = getTextDimensions(titleText, titleFont)

    while titleW > maxWidth:
        titleFontSize = titleFontSize - 8
        titleFont = ImageFont.truetype(titleFontName, titleFontSize)
        titleW, titleH = getTextDimensions(titleText, titleFont)
    titleX = (imgW - titleW) / 2
    titleY = (imgH - titleH) / 4 - titleH

    infoText = "2024.03.16"
    infoFontSize = round(titleFontSize * 0.6)
    infoFont = ImageFont.truetype(titleFontName, infoFontSize)
    infoW, infoH = getTextDimensions(infoText, infoFont)
    infoX = (imgW - infoW) / 2
    infoY = imgH - (imgH - infoH) / 4

    # Add Text to an image
    draw.text((titleX, titleY), titleText, font=titleFont, fill=color)
    draw.text((infoX, infoY), infoText, font=infoFont, fill=color)
    return img


if __name__ == "__main__":
    img = drawTextOnImage(os.path.abspath(r"epub\cover\cover_04.jpg"))
    img.show()
    img.save(r"F:\Temp\testimg.jpg")
