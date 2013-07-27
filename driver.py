#
# CoarseGrind: The automated Virginia Tech course grinding script.
# (C)2013 All rights reserved. Created with love by Jonathan Ballands.
#
# ATTENTION: Distribution of this script via means other than GitHub is
# prohibited. To download, please visit: github.com/jballands/coarsegrind
#
# For more information, visit jonathanballands.me./portfolio/coarsegrind.html
#
# driver.py
# Contains functions that drive CoarseGrind.
#

import speaker

# Driver function that decides how CoarseGrind is started via arguments.
# @param args: Arguments provided by the user via the command line.
def main(args):
	import getopt

	try:
		opts, args = getopt.getopt(args, "hnt:",["turbo="])

		for option, arg in opts:
			if option in ("-h"):
				speaker.printHelpCmdLine()
				return
			elif option in ("-n", "--normal"):
				print "Run normally."
				return
			elif option in ("-t", "--turbo"):
				print "Run in turbo mode."
				return
			else:
				continue

	except getopt.GetoptError:
		speaker.printHelpCmdLine()
		return

	print "Run normally."
	return

# Runs CoarseGrind using a pseudo-BASH shell interface.
def runNormally():
	return

# Runs CoarseGrind in Turbo mode.
def runTurbo():
	return