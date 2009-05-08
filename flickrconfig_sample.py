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

# Config

# Your flickr api key
apiKey = "YOUR FLICKR API KEY HERE"

# The xfce backdrop list
xfce4BackgroundList = "FULL PATH TO YOUR DESKTOP BACKDROP LIST (XFCE ONLY)"

# Where to store the wallpapers
wallpaperDir = "FULL PATH"

# The location of this file
localDir = "FULL PATH"

# the wallpaper prefix
wallpaperPrefix = "wallpaper"

# your screen size (w,h)
wallpaperSize = (1440,900)

# the fontsize for the text
fontsize = 25

# Max errors before quitting
maxErrors = 10

# how to sort the pics (choose [0,1,2])
sortType = ["interestingness-desc",
            "interestingness-asc",
            "relevance"][2]

noiseWords = ["shakespeare",
              "william",
              "twain",
              "wodehouse",
              "ocasey",
              "george",
              "gobel",
              "carlsverre"]
