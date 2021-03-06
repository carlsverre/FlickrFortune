FlickrFortune
=============
FlickrFortune combines the wonderfully insightful (sometimes) power of
the standard "fortune" program on most *nix systems with the Flickr
API to create wallpapers!  To see some examples visit its [homepage] [1].

Usage
-----
    flickrfortune [-s] [-c] [-n #] [-h]

    -n (--number) => number of wallpapers to generate
    -s => update the background with the last generated wallpaper
        (Note -s requires XFCE4 for now)
        (And you need to set the background file option)
    -c => use colors
    -h => this message

*PLEASE CONFIGURE VARIABLES IN flickrconfig_sample.py
and rename it as flickrconfig.py*

Requirements
------------
- python 2.5 (version 1 requires 2.5, development and above works on 2.6)
- [flickrapi] [2]
- [PIL] [3]

Configuration
-------------
+ Rename flickrconfig_sample.py to flickrconfig.py and modify all variables.
+ If you want to be able to use -s, set the setWallpaperCommand variable
to a program/script which takes the path to the wallpaper and sets your
wallpaper.  %s will be replaced with the filename.

**Copyright 2009 Carl Sverre**
[1]: http://thelab.carlsverre.com/2009/03/31/flickrfortune	"FlickrFortune's Homepage"
[2]: http://stuvel.eu/projects/flickrapi
[3]: http://www.pythonware.com/products/pil/
