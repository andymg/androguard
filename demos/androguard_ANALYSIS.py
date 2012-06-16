#!/usr/bin/env python

import sys, hashlib
PATH_INSTALL = "./"
sys.path.append(PATH_INSTALL + "./")

from androguard.core.androgen import AndroguardS
from androguard.core.analysis import analysis

OUTPUT = "./output/"
#TEST  = 'examples/java/test/orig/Test1.class'
#TEST  = 'examples/java/Demo1/orig/DES.class'
#TEST  = 'examples/java/Demo1/orig/Util.class'
#TEST = "apks/DroidDream/tmp/classes.dex"
TEST = "./examples/android/TCDiff/bin/classes.dex"
#TEST = "apks/iCalendar.apk"
#TEST = "apks/adrd/5/8370959.dex"

def display_CFG(a, x, classes) :
    for method in a.get_methods() :
        g = x.get_method( method )

        print method.get_class_name(), method.get_name(), method.get_descriptor()
        for i in g.basic_blocks.get() :
            print "\t %s %x %x" % (i.name, i.start, i.end), '[ CHILDS = ', ', '.join( "%x-%x-%s" % (j[0], j[1], j[2].get_name()) for j in i.childs ), ']', '[ FATHERS = ', ', '.join( j[2].get_name() for j in i.fathers ), ']'


def display_STRINGS(a, x, classes) :
    print "STRINGS"
    for s, _ in x.get_tainted_variables().get_strings() :
        print "String : ", repr(s.get_info())
        analysis.show_PathVariable( a, s.get_paths() )

def display_FIELDS(a, x, classes) :
    print "FIELDS"
    for f, _ in x.get_tainted_variables().get_fields() :
        print "field : ", repr(f.get_info())
        analysis.show_PathVariable( a, f.get_paths() )

def display_PACKAGES(a, x, classes) :
    print "CREATED PACKAGES"
    for m, _ in x.get_tainted_packages().get_packages() :
        print "package : ", repr(m.get_info())
        for path in m.get_paths() :
            if path.get_access_flag() == analysis.TAINTED_PACKAGE_CREATE :
                print "\t\t =>", path.get_method().get_class_name(), path.get_method().get_name(), path.get_method().get_descriptor(), path.get_bb().get_name(), "%x" % (path.get_bb().start + path.get_idx() )


def display_PACKAGES_II(a, x, classes) :
# Internal Methods -> Internal Methods
    print "Internal --> Internal"
    for j in x.get_tainted_packages().get_internal_packages() :
        print "\t %s %s %s %x ---> %s %s %s" % (j.get_method().get_class_name(), j.get_method().get_name(), j.get_method().get_descriptor(), \
                                                j.get_bb().start + j.get_idx(), \
                                                j.get_class_name(), j.get_name(), j.get_descriptor())

def display_PACKAGES_IE(a, x, classes) :
# Internal Methods -> External Methods
    print "Internal --> External"
    for j in x.get_tainted_packages().get_external_packages() :
        print "\t %s %s %s %x ---> %s %s %s" % (j.get_method().get_class_name(), j.get_method().get_name(), j.get_method().get_descriptor(), \
                                                j.get_bb().start + j.get_idx(), \
                                                j.get_class_name(), j.get_name(), j.get_descriptor())

def display_SEARCH_PACKAGES(a, x, classes, package_name) :
    print "Search package", package_name
    analysis.show_Path( x.get_tainted_packages().search_packages( package_name ) )

def display_SEARCH_METHODS(a, x, classes, package_name, method_name, descriptor) :
    print "Search method", package_name, method_name, descriptor
    analysis.show_Path( x.get_tainted_packages().search_methods( package_name, method_name, descriptor) )

def display_PERMISSION(a, x, classes) :
    # Show methods used by permission
    perms_access = x.get_tainted_packages().get_permissions( [] )
    for perm in perms_access :
        print "PERM : ", perm
        analysis.show_PathP( perms_access[ perm ] )

def display_OBJECT_CREATED(a, x, class_name) :
    print "Search object", class_name
    analysis.show_Path( x.get_tainted_packages().search_objects( class_name ) )

a = AndroguardS( TEST )
x = analysis.uVMAnalysis( a.get_vm() )

#print a.get_vm().get_strings()
#print a.get_vm().get_regex_strings( "access" )
#print a.get_vm().get_regex_strings( "(long).*2" )
#print a.get_vm().get_regex_strings( ".*(t\_t).*" )

classes = a.get_vm().get_classes_names()

#display_CFG( a, x, classes )
display_STRINGS( a.get_vm(), x, classes )
display_FIELDS( a.get_vm(), x, classes )
display_PACKAGES( a, x, classes )
display_PACKAGES_IE( a, x, classes )
display_PACKAGES_II( a, x, classes )
display_PERMISSION( a, x, classes )

#display_SEARCH_PACKAGES( a, x, classes, "Landroid/telephony/" )
#display_SEARCH_PACKAGES( a, x, classes, "Ljavax/crypto/" )
#display_SEARCH_METHODS( a, x, classes, "Ljavax/crypto/", "generateSecret", "." )

display_OBJECT_CREATED( a, x, "." )
