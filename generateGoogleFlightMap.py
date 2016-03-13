# -----------------------------------------------------------------------------
# import modules

import urllib
import csv
import argparse
import os


def mark_static_google_map(mapname, center=None, zoom=16,
                           imgsize="640x640", imgformat="png", maptype="satellite",
                           f=None, flightpath2=None, markers=None ):
    
    """
        example url:
        https://maps.googleapis.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=13
        &size=600x300&maptype=roadmap&markers=color:blue%7Clabel:S%7C40.702147,-74.015794
        &markers=color:green%7Clabel:G%7C40.711614,-74.012318
        &path=color:0x0000ff|weight:5|40.737102,-73.990318|40.749825,-73.987963
        """
    
    req = "http://maps.google.com/maps/api/staticmap?" # base URL, parameters seperated by &
    
    # if center and zoom  are not given, the map will show all marker locations
    if center != None:
        req += "center=%s&" % center


    req += "zoom=%i&" % zoom
    req += "size=%s&" % imgsize  # tuple of ints, up to 640 by 640
    req += "format=%s&" % imgformat  # jpeg by default
    req += "maptype=%s&" % maptype  # options: roadmap, satellite, hybrid, terrain

    if f != None:
        req += "&path=color:0xff0000|weight:5"
            for location in f:
                req += "%s" % location


    # add markers (lat and lon)
    if markers != None:
        for marker in markers:
            req += "%s&" % marker
    
    # get remote data and save it to a local path
    req += "&sensor=true"
    server_image = mapname + "."+imgformat
    urllib.urlretrieve(req, server_image)


def parseFlightFile(filename):
    # query location data from input file
    
    if filename == None:
        return None

    path = []
    with open(filename, 'r') as file:
        
        for line in file:
            if not line:
                continue
            gps = line.replace(',',' ').split()
            print(gps)
            path.append("|" + '{0}, {1}'.format(gps[0], gps[1]))
    return path


