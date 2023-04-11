#!/usr/bin/env python3
import os
from colorama import init, Fore, Back, Style
inputFile = '/mnt/data/Media/Movies/Spies_Like_Us_(1985)/Spies_Like_Us_(1985).mp4'
outputFile = '/mnt/data/Media/Movies/Spies_Like_Us_(1985)/test.mp4'
cmd = 'ffmpeg -i ' + inputFile + ' -c:v libx265 -vtag hvc1 ' + outputFile
os.system(cmd)