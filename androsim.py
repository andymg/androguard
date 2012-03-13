#!/usr/bin/env python

# This file is part of Androguard.
#
# Copyright (C) 2012, Anthony Desnos <desnos at t0t0.fr>
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

import sys

from optparse import OptionParser

from androguard.core import androconf
from androguard.core.bytecodes import apk, dvm
from androguard.core.analysis import analysis

sys.path.append("./elsim")
from elsim import elsim
from elsim.elsim_dalvik import ProxyDalvik, FILTERS_DALVIK, FILTERS_DALVIK_SIM
from elsim.elsim_dalvik import ProxyDalvikStringOne, FILTERS_DALVIK_SIM_STRING

option_0 = { 'name' : ('-i', '--input'), 'help' : 'file : use these filenames', 'nargs' : 2 }
option_1 = { 'name' : ('-t', '--threshold'), 'help' : 'define the threshold', 'nargs' : 1 }
option_2 = { 'name' : ('-c', '--compressor'), 'help' : 'define the compressor', 'nargs' : 1 }
option_3 = { 'name' : ('-f', '--filter'), 'help' : 'select the filter', 'nargs' : 1 }
option_4 = { 'name' : ('-d', '--display'), 'help' : 'display the file in human readable format', 'action' : 'count' }
option_5 = { 'name' : ('-v', '--version'), 'help' : 'version of the API', 'action' : 'count' }

options = [option_0, option_1, option_2, option_3, option_4, option_5]

############################################################
def main(options, arguments) :
    if options.input != None :
        ret_type = androconf.is_android( options.input[0] )
        if ret_type == "APK" :
            a = apk.APK( options.input[0] )
            d1 = dvm.DalvikVMFormat( a.get_dex() )
        elif ret_type == "DEX" :
            d1 = dvm.DalvikVMFormat( open(options.input[0], "rb").read() )
        
        dx1 = analysis.VMAnalysis( d1 )
       
        ret_type = androconf.is_android( options.input[1] )
        if ret_type == "APK" :
            a = apk.APK( options.input[1] )
            d2 = dvm.DalvikVMFormat( a.get_dex() )
        elif ret_type == "DEX" :
            d2 = dvm.DalvikVMFormat( open(options.input[1], "rb").read() )
        
        dx2 = analysis.VMAnalysis( d2 )

        print d1, dx1, d2, dx2
        sys.stdout.flush()
        
        threshold = None
        if options.threshold != None :
            threshold = float(options.threshold)

        filter_sim = 0
        if options.filter != None :
            filter_sim = int(options.filter)

        FS = { 0 : FILTERS_DALVIK_SIM, 1 : FILTERS_DALVIK }
        el = elsim.Elsim( ProxyDalvik(d1, dx1), ProxyDalvik(d2, dx2), FS[filter_sim], threshold, options.compressor )
        el.show()
        print "\t--> methods: %f%% of similarities" % el.get_similarity_value()
        
        els = elsim.Elsim( ProxyDalvikStringOne(d1, dx1), ProxyDalvikStringOne(d2, dx2), FILTERS_DALVIK_SIM_STRING, threshold, options.compressor )
        els.show()
        print "\t--> strings: %f%% of similarities" % els.get_similarity_value()

        if options.display :
            print "SIMILAR methods:"
            diff_methods = el.get_similar_elements()
            for i in diff_methods :
                el.show_element( i )
            
            print "IDENTICAL methods:"
            new_methods = el.get_identical_elements()
            for i in new_methods :
                el.show_element( i )

            print "NEW methods:"
            new_methods = el.get_new_elements()
            for i in new_methods :
                el.show_element( i, False )

            print "DELETED methods:"
            del_methods = el.get_deleted_elements()
            for i in del_methods :
                el.show_element( i )
            
            print "SKIPPED methods:"
            skipped_methods = el.get_skipped_elements()
            for i in skipped_methods :
                el.show_element( i )

    elif options.version != None :
        print "Androsim version %s" % androconf.ANDROGUARD_VERSION

if __name__ == "__main__" :
    parser = OptionParser()
    for option in options :
        param = option['name']
        del option['name']
        parser.add_option(*param, **option)

    options, arguments = parser.parse_args()
    sys.argv[:] = arguments
    main(options, arguments)
