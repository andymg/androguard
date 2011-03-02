#!/usr/bin/env python                                                                                                                                                                                                             

# This file is part of Androguard.
#
# Copyright (C) 2010, Anthony Desnos <desnos at t0t0.org>
# All rights reserved.
#
# Androguard is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Androguard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of  
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Androguard.  If not, see <http://www.gnu.org/licenses/>.

import sys, hashlib, os
from optparse import OptionParser
from xml.dom import minidom

PATH_INSTALL = "./"                                                                                                                                                                                                               
sys.path.append(PATH_INSTALL + "./")

import androguard, analysis, dvm
from misc import VERSION

option_0 = { 'name' : ('-i', '--input'), 'help' : 'filename input (APK or android\'s binary xml)', 'nargs' : 1 }
option_1 = { 'name' : ('-o', '--output'), 'help' : 'filename output of the xml', 'nargs' : 1 }
option_2 = { 'name' : ('-v', '--version'), 'help' : 'version of the API', 'action' : 'count' }
options = [option_0, option_1, option_2]

def main(options, arguments) :
   if options.input != None and options.output != None :

      buff = ""
      if ".apk" in options.input :
         a = dvm.APK( options.input )
         buff = a.xml[ "AndroidManifest.xml" ].toprettyxml()
      elif ".xml" in options.input :
         ap = dvm.AXMLPrinter( open(options.input, "r").read() )
         buff = minidom.parseString( ap.getBuff() ).toprettyxml()         
      else :
         print "Unknown file type"
         return

      fd = open(options.output, "w")
      fd.write( buff )
      fd.close()
   elif options.version != None :
      print "Androaxml version %s" % VERSION

if __name__ == "__main__" :
   parser = OptionParser()
   for option in options :
      param = option['name']
      del option['name']
      parser.add_option(*param, **option)
      
   options, arguments = parser.parse_args()
   sys.argv[:] = arguments
   main(options, arguments)    
