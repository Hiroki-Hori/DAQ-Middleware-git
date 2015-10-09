#!/usr/bin/env python

"""Write xml path for using changed state, daq.py
"""
__author__   = 'Hiroki Hori'
__version__  = '1.0'
__date__     = '1-October-2015'

from mod_python import apache
file = "/var/www/html/daqmw/operatorPanel/xmlPath.txt"

def SaveXmlPath(req, xmlPath):
       """Save run number into the file."""
       fileObj = open(file, "w+")
       fileObj.write(xmlPath)
       req.write("OK")
       return
