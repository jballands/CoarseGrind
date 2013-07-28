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

import cg_io, navigator, copy, gc

# Driver function that decides how CoarseGrind is started via arguments.
# @param args: Arguments provided by the user via the command line.
def main(args):
	import getopt

	try:
		opts, args = getopt.getopt(args, "hnt:",["turbo="])

		for option, arg in opts:
			if option in ("-h"):
				cg_io.printHelpCmdLine()
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
		cg_io.printHelpCmdLine()
		return

	print "Starting normally..."
	runNormally()
	return

# Runs CoarseGrind using a pseudo-BASH shell interface.
def runNormally():
	cg_io.printWelcome()
	print "Preparing. Wait...\n"

	# Get a scraper going
	mainScraper = navigator.Scraper()
	mainScraper.navigateToLoginPage()
	success = False

	# While you cannot login
	while (success != True):
		credentialsList = cg_io.requestCredentials()

		# Check for <q>
		if (credentialsList[0] == "q"):
			print "Terminating...\n"
			return

		cg_io.waitMessage()
		success = mainScraper.submitToLoginPage(credentialsList[0], credentialsList[1])
		if (success != True):
			cg_io.printLoginFailure()

	print "Login successful. Welcome, " + credentialsList[0] + "!"
	print "Ready\n"

	# Run-time loop
	command = -1
	while (command != 0):
		command = cg_io.takeCommand()

		# Add operation
		if (command == 2):
			cg_io.waitMessage()
			print "<q> at any prompt to quit.\n"

			timetableScrapper = copy.copy(mainScraper)

			timetableScrapper.navigateToRegAndSch()
			timetableScrapper.navigateToTimetable()
			result = cg_io.requestTermSelection(timetableScrapper.locateAndParseTerms())

			# Quitting
			if (result == -1):
				print "Caching memory...\n"
				continue

	cg_io.tryQuit()
	return

# Runs CoarseGrind in Turbo mode.
def runTurbo():
	cg_io.printWelcome()
	return