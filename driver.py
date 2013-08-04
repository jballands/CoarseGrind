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

import cg_io, navigator, copy, gc, threading, grinder

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

	setupSemaphore = threading.Semaphore()
	pool = 0
	setupThread = threading.Thread(target=_setupResources, args=[mainScraper, setupSemaphore])
	setupThread.start()

	print "Login successful. Welcome, " + credentialsList[0] + "!"
	print "Ready\n"

	# Run-time loop
	command = -1
	while (command != 0):
		command = cg_io.takeCommand()

		# Add operation
		if (command == 2):
			cg_io.waitMessage()

			# Semaphore down
			setupSemaphore.acquire()

			# Pool ready?
			if (pool == 0):
				pool = grinder.GruntPool(30, copy.copy(mainScraper))
			
			# This loop is here because we have to make sure that the CRN is valid
			# You only know if the CRN is valid after submitting, so the loop goes here
			while(True):
				term = cg_io.requestTermSelection(mainScraper.locateAndParseTerms())

				# Quitting
				if (term == -1):
					print "Backing out...\n"
					break

				crn = cg_io.requestCrn()

				# Quitting
				if (term == -1):
					print "Backing out...\n"
					break

				cg_io.waitMessage()
				if (mainScraper.submitToTimetable(term, crn) == True):
					break

				cg_io.printError(6)

			# Semaphore up
			setupSemaphore.release()

			# Report results
			dictionary = mainScraper.locateAndParseTimetableResults()
			cg_io.printTimetableResultDictionary(dictionary)
			cg_io.requestAddAction(dictionary)

			# Add a job to the grinder
			pool.releaseGrunt(dictionary, term, crn)

		# Job reporting
		elif (command == 3):
			allJobs = pool.getRunningList()
			for i in range(0, len(allJobs)):
				if (i == len(allJobs) - 1):
					print "[" + str(i) + "]: " + allJobs[i] + "\n"
				else:
					print "[" + str(i) + "]: " + allJobs[i]

	# Try to quit, shutting down the pool
	cg_io.printQuitting()
	pool.shutdown()
	return

# Runs CoarseGrind in Turbo mode.
def runTurbo():
	cg_io.printWelcome()

	# Temporary
	print "Turbo mode is not yet implemented. Terminating..."
	return

# Private function
# Sets up resources for use in CoarseGrind. Runs in a seperate thread.
# @param theScrapper: The main scrapper.
# @param setupSemaphore: The mutex lock for the scrapers.
def _setupResources(theScraper, setupSemaphore):
	# These operations take a long time
	setupSemaphore.acquire()
	theScraper.jumpToRegAndSch()
	theScraper.navigateToTimetable()
	setupSemaphore.release()
