#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#   Print out a named player dat file for research / investigation
#   (added by ProgrammerDan <programmerdan@gmail.com>)
#   Copyright (C) 2011  Alejandro Aguilera (Fenixin)
#   https://github.com/Fenixin/Minecraft-Region-Fixer
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from os.path import split, join
import time

import sys
import traceback

import array
from scan import scan_playerfile
from optparse import OptionParser, OptionGroup
from interactive import interactive_loop
from util import entitle, is_bare_console, parse_player_paths


def main():
    usage = 'usage: %prog <playerdat-path> <playerdat-path> ...'
    epilog = 'Copyright (C) 2011  Alejandro Aguilera (Fenixin) \
    https://github.com/Fenixin/Minecraft-Region-Fixer                                        \
    This program comes with ABSOLUTELY NO WARRANTY; for details see COPYING.txt. This is free software, and you are welcome to redistribute it under certain conditions; see COPYING.txt for details.'

    parser = OptionParser(description='Script to quickly output playerdat files. It uses NBT by twoolie. Author: ProgrammerDan, using work by Alejandro Aguilera (Fenixin)',\
    prog = 'outputplayer', version='0.0.1', usage=usage, epilog=epilog)

    (options, args) = parser.parse_args()

    if is_bare_console():
        print
        print "Minecraft Output Player is a command line aplication, if you want to run it"
        print "you need to open a command line (cmd.exe in the start menu in windows 7)."
        print 
        getpass("Press enter to continue:")
        return 1

    # Args are player files
    if not args:
        parser.error("No player data files specified! Use --help for a complete list of options.")

    player_list = parse_player_paths(args)

    if not player_list:
        print ("Error: No player dat files to scan!")
        return 1

    print "\nWelcome to Output Player!"
    print "(version: {0})".format(parser.version)

    summary_text = ""
    # scan the separate region files
    if len(player_list) > 0:
        print entitle("Scanning separate player dat files", 0)
        for player_file in player_list:
            print entitle(' Scanning player file: {0} '.format(player_file),0)
            summary_text += "\n"
            summary_text += scan_playerfile(player_file)
            summary_text += "\n"
        
        print "\nPrinting log:\n"
        print summary_text
    else:
        print "\nNo valid player dat files provided\n"

    return 0

if __name__ == '__main__':
    value = main()
    sys.exit(value)
