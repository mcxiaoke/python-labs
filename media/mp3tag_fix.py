import mutagen
import mutagen.id3
import sys
import os
'''
File: mp3tag_fix.py
Created: 2021-03-02 14:45:24
Modified: 2021-03-02 14:45:28
Author: mcxiaoke (github@mcxiaoke.com)
License: Apache License 2.0
'''
'''
ID3 v2.3 TAGS
APIC - Picture, COMM - Comment, SYLT - SynLyrics
TALB - Album, TCON - Genre, TCOP - Copyright
TIT1 - Grouping, TIT2 - Title, TIT3 - Subtitle
TPE1 - Artist, TPE2 - Band, TPE3 - Conductor

demo.mp3
'APIC=cover front, thumbnail (image/jpeg, 11693 bytes)\nTALB=album\nTIT2=title\nTPE1=artist'
'''
filename = sys.argv[1]

try:
    tags = mutagen.id3.ID3(filename)
    print(os.path.basename(filename))
    print('Artist:{}, Title:{}, Album:{}'.format(
        tags['TPE1'], tags['TIT2'], tags['TALB']))
except mutagen.id3.ID3NoHeaderError as e:
    print(e)
