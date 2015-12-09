#!/usr/bin/env python

"""daqmwcom : commnication tool for DAQ Operator

This daqmwcom class is used for communicating to DAQ Operator
via HTTP protocol.
There are two ways to use:
One is used in python script by 'import'ing daqmwcom.
Another is used as command.
When DAQ Operator does not run,
all methods except contructor and getLog occur error.
Thus, user should check the status by using getLog method
if DAQ Operator runs or not.
getLog('status') will return 'NG'.
"""

__author__   = 'Yoshiji Yasu and Hiroshi Sendai'
__version__  = '0.95'
__date__ = '9-April-2012'

import urllib
import httplib2
import getopt, sys
from xml.dom.minidom import parseString

class daqmwcom:

    def __init__(self, urlbase=None):
        if urlbase != None:
            self.urlbase = urlbase + "/daq.py/"
        self.http = httplib2.Http()

    def setURLBase(self, urlbase):
        self.urlbase = urlbase + "/daq.py/"

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value
    
    def configure(self):
        self.url = self.urlbase + "Params"
        self.body = {"cmd":"<?xml version='1.0' encoding='UTF-8' standalone='no' ?><request><params>config.xml</params></request>"}
        self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self.response, self.content = self.http.request(self.url, 'POST', headers=self.headers, body=urllib.urlencode(self.body))
#        print self.response
        return self.content

    def start(self, runNo):
        self.url = self.urlbase + "Begin"
        self.body= {"cmd":"<?xml version='1.0' encoding='UTF-8' ?><request><runNo>" + runNo + "</runNo></request>"}
        self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self.response, self.content = self.http.request(self.url, 'POST', headers=self.headers, body=urllib.urlencode(self.body))
        return self.content

    def stop(self):
        self.url = self.urlbase + "End"
        self.body ={"cmd":" " }
        self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self.response, self.content = self.http.request(self.url, 'POST', headers=self.headers, body=urllib.urlencode(self.body))
        return self.content

    def pause(self):
        self.url = self.urlbase + "Pause"
        self.body ={"cmd":" " }
        self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self.response, self.content = self.http.request(self.url, 'POST', headers=self.headers, body=urllib.urlencode(self.body))
        return self.content

    def unconfigure(self):
        self.url = self.urlbase + "ResetParams"
        self.body ={"cmd":" " }
        self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self.response, self.content = self.http.request(self.url, 'POST', headers=self.headers, body=urllib.urlencode(self.body))
        return self.content

    def resume(self):
        self.url = self.urlbase + "Restart"
        self.body ={"cmd":" " }
        self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self.response, self.content = self.http.request(self.url, 'POST', headers=self.headers, body=urllib.urlencode(self.body))
        return self.content

    def change(self, xmlPath):
        self.url = self.urlbase + "Change"
        self.body= {"cmd":"<?xml version='1.0' encoding='UTF-8' ?><request><xmlPath>" + xmlPath + "</xmlPath></request>"}
        self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self.response, self.content = self.http.request(self.url, 'POST', headers=self.headers, body=urllib.urlencode(self.body))
        return self.content

    def revConfigure(self):
        self.url = self.urlbase + "revConfigure"
        self.body ={"cmd":" " } 
        self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self.response, self.content = self.http.request(self.url, 'POST', headers=self.headers, body=urllib.urlencode(self.body))
        return self.content

    def revPause(self):
        self.url = self.urlbase + "revPause"
        self.body ={"cmd":" " } 
        self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self.response, self.content = self.http.request(self.url, 'POST', headers=self.headers, body=urllib.urlencode(self.body))
        return self.content

    def setXmlPath(self, xmlPath):
        self.url = self.urlbase + "../writexmlpath.py/SaveXmlPath"
        self.body ={"xmlPath": xmlPath }
        self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self.response, self.content = self.http.request(self.url, 'POST', headers=self.headers, body=urllib.urlencode(self.body))
        return self.content

    def getLog(self, tag):
        self.url = self.urlbase + "Log"
        self.response, self.content = self.http.request(self.url, 'GET')
#        print self.content
        dom = parseString(self.content)
        if tag == "all":
            return self.content
        else:
            nodes = dom.getElementsByTagName(tag)
            if len(nodes) == 0:
                return 'NG'
            return nodes[0].firstChild.data

    def setRunNumber(self, runNo):
        self.url = self.urlbase + "../writedata.py/SaveRunNumber"
        self.body ={"RunNumber": runNo }
        self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self.response, self.content = self.http.request(self.url, 'POST', headers=self.headers, body=urllib.urlencode(self.body))
        return self.content

    def cli(self):
        argc = len(sys.argv)
        if argc != 3 and argc != 4:
            print "usage: %s urlbase options" % sys.argv[0]
            print "       urlbase:"
            print "       http://localhost/daqmw/operatorPanel/ for SL(C)5 or earlier"
            print "       http://localhost/daqmw/scripts/ for SL(C)6 or later"
            print "       options:"
            print "       -c or --configure   : configure command"
            print "       -b runNum or --start runNum : start(begin) command"
            print "          for example, -b 100"
            print "       -e or --stop        : stop(end) command"
            print "       -u or --unconfigure : unconfigure command"
            print "       -p or --pause       : pause command"
            print "       -r or --resume      : resume command"
            print "       -n or --change      : change command"
            print "       -f or --revconfigure: revconfigure command"
            print "       -s or --revpause    : revpause command"
            print "       -g tag or --getLog tag : getLog command"
            print "          for example, -g state or -g all"
            print "            all means all of tags"
            sys.exit()

        urlbase = sys.argv[1]
        com = daqmwcom(urlbase)
        opts, args = getopt.getopt(sys.argv[2:],'cb:euprg:fsn:s', ['configure', 'start=', 'stop', 'unconfigure', 'pause', 'resume', 'change=', 'revconfigure', 'revpause', 'getLog=', 'getLogSecure'] )
        # print opts, args
        for o, a in opts:
            if o == "--configure" or o == "-c":
                print com.configure()
            elif o == "--start" or o == "-b":
                runNo = a
                print com.setRunNumber(runNo)
                print com.start(runNo)
            elif o == "--stop" or o == "-e":
                print com.stop()
            elif o == "--unconfigure" or o == "-u":
                print com.unconfigure()
            elif o == "--pause" or o == "-p":
                print com.pause()
            elif o == "--resume" or o == "-r":
                print com.resume()

            elif o == "--change" or o == "-c":
                xmlPath = a
                print com.setXmlPath(xmlPath)
                print com.change(xmlPath)
            elif o == "--revconfigure" or o == "-f":
                print com.revConfigure()
            elif o == "--revpause" or o == "-s":
                print com.revPause()
            elif o == "--getLog" or o == "-g":
                tag = a
                print com.getLog(tag)
            else:
                print "invalid command"
                break
