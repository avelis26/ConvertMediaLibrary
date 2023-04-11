#!/usr/bin/env python3
import os
from colorama import init, Fore, Back, Style
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("input", help="Full path to video file to convert to h265.")
args = parser.parse_args()
inputFile = '/mnt/data/Media/Movies/Spies_Like_Us_\(1985\)/Spies_Like_Us_\(1985\).mp4'
outputFile = '/mnt/data/Media/Movies/Spies_Like_Us_\(1985\)/test.mp4'
cmd = 'ffmpeg -i ' + inputFile + ' -c:v libx265 -vtag hvc1 ' + outputFile
print(Style.BRIGHT + Back.BLACK + Fore.GREEN + outputFile)
os.system(cmd)