#!/usr/bin/env python

import sys, os

# CHANGE THE PATH BY THE DIRECTORY WHERE YOU HAVE INSTALL Androguard
PATH_ANDROGUARD_INSTALL = "/home/pouik/androguard/"

sys.path.append( PATH_ANDROGUARD_INSTALL )
sys.path.append( PATH_ANDROGUARD_INSTALL + "/core")
sys.path.append( PATH_ANDROGUARD_INSTALL + "/core/bytecodes")
sys.path.append( PATH_ANDROGUARD_INSTALL + "/core/predicates")
sys.path.append( PATH_ANDROGUARD_INSTALL + "/core/analysis")
sys.path.append( PATH_ANDROGUARD_INSTALL + "/core/vm")
sys.path.append( PATH_ANDROGUARD_INSTALL + "/core/wm")

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
      a.do( sys.argv[2] )
      a.save()

__main__()
