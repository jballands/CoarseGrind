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

import io, navigator

# Driver function that decides how CoarseGrind is started via arguments.
# @param args: Arguments provided by the user via the command line.
def main(args):
	import getopt

	try:
		opts, args = getopt.getopt(args, "hnt:",["turbo="])

		for option, arg in opts:
			if option in ("-h"):
				io.printHelpCmdLine()
				return
			elif option in ("-n", "--normal"):
				print "Starting normally..."
				runNormally()
				return
			elif option in ("-t", "--turbo"):
				print "Starting in Turbo mode..."
				runTurbo()
				return
			else:
				continue

	except getopt.GetoptError:
		print "Illegal arguments..."
		io.printHelpCmdLine()
		return

	print "Starting normally..."
	runNormally()
	return

# Runs CoarseGrind using a pseudo-BASH shell interface.
def runNormally():
	io.printWelcome()

	# Get a scraper going
	mainScraper = navigator.Scraper()
	mainScraper.navigateToLoginPage()
	success = False

	# While you cannot login
	while (success != True):
		credentialsList = io.requestCredentials()

		# Check for <q>
		if (credentialsList[0] == "q"):
			print "Terminating..."
			return

		io.waitMessage()
		success = mainScraper.submitToLoginPage(credentialsList[0], credentialsList[1])
		if (success != True):
			io.printLoginFailure()

	print "Login successful. Welcome, " + credentialsList[0] + "!"
	io.waitMessage()

	# Navigate to the correct page
	mainScraper.navigateToRegAndSch()
	print "Ready\n"

	while (io.takeCommand != 0):
		continue

	io.tryQuit()
	return

# Runs CoarseGrind in Turbo mode.
def runTurbo():
	io.printWelcome()
	return