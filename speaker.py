#
# CoarseGrind: The automated Virginia Tech course grinding script.
# (C)2013 All rights reserved. Created with love by Jonathan Ballands.
#
# ATTENTION: Distribution of this script via means other than GitHub is
# prohibited. To download, please visit: github.com/jballands/coarsegrind
#
# For more information, visit jonathanballands.me./portfolio/coarsegrind.html
#
# speaker.py
# Contains functions that make CoarseGrind verbose.
#

# Prints the help string onto the command line.
def printHelpCmdLine():
	print "\ncoarsegrind [-h] [-n|--normal] [-t|--turbo <config>]"
	print "-h: See this help prompt."
	print "-n|--normal: Run CoarseGrind normally. Specifying no switches will also run normally."
	print "-t|--turbo: Run CoarseGrind in Turbo mode, with <config> as the configuration file.\n"

