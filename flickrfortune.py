#!/usr/bin/python
#
# Copyright 2009 Carl Sverre
#
# This file is part of FlickrFortune.
#
# FlickrFortune is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FlickrFortune is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FlickrFortune.  If not, see <http://www.gnu.org/licenses/>.

import flickrapi
import xml.etree.ElementTree as ET
import urllib2
import datetime
import os
from PIL import Image
import ImageDraw
import ImageFont
import re
import sys
import getopt

from flickrconfig import *

# Globals

c_norm = "\033[0m"
c_bold = c_norm+"\033[1m"
c_bred = "\033[1;31m"
c_bgreen = "\033[1;32m"

defaultBackgroundText = "# xfce backdrop list\n"
flickrUnavailableImage = "unavailable.gif"

errorRetrievingPhoto = "ERROR: Cannot retrieve photo"
errorNoPhotosForTag = "ERROR: Cannot find photo for tag, trying again"
imageUnavailableError = "ERROR: Image Unavailable, trying again"
errorTooManyErrors = "ERROR: Too many errors occured, quitting"

errorRetrievingPhoto_c = c_bred+"ERROR:"+c_bold+" Cannot retrieve photo"+c_norm
errorNoPhotosForTag_c = c_bred+"ERROR:"+c_bold+" Cannot find photo for tag, trying again"+c_norm
imageUnavailableError_c = c_bred+"ERROR:"+c_bold+" Image Unavailable, trying again"+c_norm
errorTooManyErrors_c = c_bred+"ERROR:"+c_bold+"Too many errors occured, quitting"+c_norm

optsString = "hn:sc"
optsList = ["help", "number="]

usageString = """Usage:
    -n (--number) => number of wallpapers to generate
    -s => update the background with the last generated wallpaper
    -c => use colors
    -h => this message"""

finishedWallpaperString = "FINISHED: %s"
finishedWallpaperString_c = c_bgreen+"FINISHED: "+c_bold+"%s"+c_norm

photoUrlFormat = "http://farm%s.static.flickr.com/%s/%s_%s_b.jpg"

timeStampFormat = "%d%m%y%H%M%S"
timeStamp = datetime.datetime.now().strftime(timeStampFormat)

tagRegexPattern = re.compile("[^A-Za-z ]")

flickrPrefix = "flickr"

colors = False

# Functions
def cleanUp():
    os.system("rm "+localDir+"*.jpg")

def getFortune():
    f = os.popen("fortune -s");
    fortune = f.read()
    f.close()
    return fortune

def getTag(fortune):
    fortune = tagRegexPattern.sub("", fortune)
    fortune = fortune.split(" ")
    word = fortune[0]
    for w in fortune:
        if (len(w) >= len(word)) and (not w.lower() in noiseWords):
            word = w

    return word

def loadPhotoURL(tag):
    flickr = flickrapi.FlickrAPI(apiKey)
    photos = flickr.photos_search(tags=tag,
                              sort=sortType,
                              per_page='1')

    if not photos.attrib['stat'] == "ok":
        if colors: print errorRetrievingPhoto_c
        else: print errorRetrievingPhoto
        return 0

    photos = photos.find('photos').findall('photo')
    if not photos:
        if colors: print errorNoPhotosForTag_c
        else: print errorNoPhotosForTag
        return 0

    photo = photos[0]

    photoID = photo.attrib['id']
    photoSECRET = photo.attrib['secret']
    photoFARM = photo.attrib['farm']
    photoSERVER = photo.attrib['server']

    return photoUrlFormat % (photoFARM, photoSERVER, photoID, photoSECRET)

def getImageData(url):
    try:
        return urllib2.urlopen(url).read()
    except urllib2.URLError:
        print urlib2_URLError
        exit(1)

def createWallpaper(flickrImage, fortune, prefix):
    wallpaper = Image.new("RGB", wallpaperSize, "black")
    draw = ImageDraw.Draw(wallpaper)

    flickrImage = Image.open(localDir + flickrImage)
    x,y = flickrImage.size

    x0 = (wallpaperSize[0]-x) / 2
    y0 = (wallpaperSize[1]-y) / 2

    x1 = x0+x
    y1 = y0+y

    wallpaper.paste(flickrImage, (x0,y0,x1,y1))

    boxMargin = 10

    font = ImageFont.truetype(localDir + "Sugo.ttf", fontsize)
    textSize = draw.textsize(fortune, font=font)
    textTopLeft = (wallpaperSize[0]/2 - textSize[0]/2, wallpaperSize[1]-textSize[1]*4)

    boxTopLeft = (textTopLeft[0]-boxMargin, textTopLeft[1])
    boxBottomRight = (wallpaperSize[0]/2 + textSize[0]/2 + boxMargin, wallpaperSize[1]-textSize[1]*3+boxMargin)

    draw.rectangle([boxTopLeft, boxBottomRight], fill="white")

    draw.text(textTopLeft, fortune, font=font, fill="black")

    del draw

    filename = wallpaperDir + prefix+"_"+wallpaperPrefix+".jpg"
    wallpaper.save(filename, "JPEG")
    return filename

def saveFlickrImage(imageData, prefix):
    fileName = prefix+"_"+flickrPrefix+".jpg"

    try:
        f = open(localDir + fileName, 'w')
    except IOError:
        print IOError
        exit(1)

    f.write(imageData)
    f.close()

    return fileName

def setWallpaper(fileName):
    try:
        backgroundList = open(xfce4BackgroundList, "w")
        backgroundList.write(defaultBackgroundText)
    except IOError:
        print IOError
        exit(1)

    backgroundList.write(fileName + "\n")
    backgroundList.close()
    os.system("xfdesktop -reload")

def checkUnavailable(flickrImage):
    if os.path.getsize(localDir + flickrImage) == os.path.getsize(localDir + flickrUnavailableImage):
        if colors: print imageUnavailableError_c
        else: print imageUnavailableError
        return True
    return False

def usage():
    print usageString
    sys.exit(2)

def main(argv):
    global colors
    print

    numWallpapers = 1
    updateBackground = False
   
    try:
        opts, args = getopt.getopt(argv, optsString, optsList)
    except getopt.GetoptError:
        usage()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ('-n', "--number"):
            numWallpapers = int(arg)
        elif opt == '-s':
            updateBackground = True
        elif opt == '-c':
            colors = True

    numErrors = 0
    counter = 0
    while True:
        if numErrors >= maxErrors:
            if colors: print errorTooManyErrors_c
            else: print errorTooManyErrors
            break

        fortune = getFortune()
        tag = getTag(fortune)
        photoUrl = loadPhotoURL(tag)
        if photoUrl == 0:
            numErrors += 1
            continue

        flickrImage = saveFlickrImage(getImageData(photoUrl), tag)

        if checkUnavailable(flickrImage):
            numErrors += 1
            continue
        
        wallpaperFile = createWallpaper(flickrImage, fortune, tag)
        if colors: print finishedWallpaperString_c % wallpaperFile
        else: print finishedWallpaperString % wallpaperFile

        counter += 1
        if counter == numWallpapers:
            if updateBackground:
                setWallpaper(wallpaperFile)
            break

        numErrors = 0

    cleanUp()
    print

if __name__ == "__main__":
    main(sys.argv[1:])
