#!/usr/bin/env python

import sys, os

PATH_ANDROGUARD_INSTALL = "/home/pouik/androguard/"

sys.path.append( PATH_ANDROGUARD_INSTALL )
sys.path.append( PATH_ANDROGUARD_INSTALL + "/core")
sys.path.append( PATH_ANDROGUARD_INSTALL + "/core/bytecodes")
sys.path.append( PATH_ANDROGUARD_INSTALL + "/core/predicates")
sys.path.append( PATH_ANDROGUARD_INSTALL + "/core/analysis")
sys.path.append( PATH_ANDROGUARD_INSTALL + "/core/vm")

import androguard, bytecode

def get_classes(path) :
   g_files = []
   for root, dirs, files in os.walk( path ) :
      if files != [] :
         for file in files :
            if ".class" in file :
               g_files.append(root + "/" + file)

   return g_files

def __main__() :
   print sys.argv
   if len( sys.argv ) > 1 :
      files = get_classes( sys.argv[1] )

      a = androguard.Androguard( files )
      a.protect( sys.argv[2] )

__main__()
