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

import cg_io, navigator, copy, gc, threading, grinder, time, re

# Driver function that decides how CoarseGrind is started via arguments.
# @param args: Arguments provided by the user via the command line.
def main(args):
	import getopt

	try:
		opts, args = getopt.getopt(args, "hnut:",["turbo="])

		for option, arg in opts:
			if option in ("-h"):
				cg_io.printHelpCmdLine()
				return
			elif option in ("-n", "--normal"):
				print "Starting normally..."
				runNormally(False)
				return
			elif option in ("-t", "--turbo"):
				print "Starting in Turbo mode..."
				runTurbo()
				return
			elif option in ("-u", "--unsafe"):
				print "Starting in unsafe mode..."
				runNormally(True)
				return
			else:
				continue

	except getopt.GetoptError:
		print "Illegal arguments..."
		cg_io.printHelpCmdLine()
		return

	print "Starting normally..."
	runNormally(False)
	return

# Runs CoarseGrind using a pseudo-BASH shell interface.
def runNormally(unsafe):

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
			print "Stopping...\n"
			return

		cg_io.waitMessage()
		success = mainScraper.submitToLoginPage(credentialsList[0], credentialsList[1])
		if (success != True):
			cg_io.printLoginFailure()

	pool = 0
	setupThread = ThreadWithReturnValue(target=_setupResources, args=[mainScraper, unsafe])
	setupThread.start()

	print "Login successful. Welcome, " + credentialsList[0] + "!"
	print "Ready\n"

	# Run-time loop
	command = -1
	while (command != "quit"):
		command = cg_io.takeCommand()
		killRegex = re.compile("kill \d+")

		# Quit operation
		if (command == "quit"):
			break

		# Help operation
		elif (command == "help"):
			cg_io.printHelp()
			continue

		# Debug operation
		elif (command == "debug"):
			print "<return> key at any time to leave debugging context."
			pool.broadcastDebug(True)
			crn = raw_input("")
			pool.broadcastDebug(False)

		# Add operation
		elif (command == "add"):
			cg_io.waitMessage()

			# Pool ready?
			if (pool == 0):
				pool = grinder.GruntPool(30)

			# Wait to join
			result = setupThread.join()
			if (result == -1):
				cg_io.printNoDropAdd()
				break

			# This loop is here because we have to make sure that the CRN is valid
			# You only know if the CRN is valid after submitting, so the loop goes here
			backingOut = False
			while(True):
				term = cg_io.requestTermSelection(mainScraper.locateAndParseTerms())

				# Quitting
				if (term == -1):
					print "Backing out...\n"
					backingOut = True
					break

				crn = cg_io.requestCrn()

				# Quitting
				if (crn == -1):
					print "Backing out...\n"
					backingOut = True
					break

				cg_io.waitMessage()
				if (mainScraper.submitToTimetable(term, crn) == True):
					break

				cg_io.printError(6)


			if (backingOut == True):
				continue

			# Report results
			dictionary = mainScraper.locateAndParseTimetableResults()
			cg_io.printTimetableResultDictionary(dictionary)
			answer = cg_io.requestAddAction(dictionary)

			# Add a job to the grinder
			if (answer == True):
				# BUG: Shallow copies only do references, and deep copy doesn't work...
				copyScraper = navigator.clone(mainScraper)
				pool.releaseGrunt(dictionary, term, crn, copyScraper)
				print "Job added\n"
				continue
			else:
				print "Backing out...\n"
				continue

		# Job reporting
		elif (command == "jobs"):
			allJobs = pool.getRunningList()
			somethingToDisplay = False
			if (len(allJobs) > 0):
				somethingToDisplay = True
				print "Busy:"
				for i in range(0, len(allJobs)):
					if (i == len(allJobs) - 1 and len(pool.getDoneList()) == 0):
						print "[" + str(i) + "]: " + allJobs[i] + "\n"
					else:
						print "[" + str(i) + "]: " + allJobs[i]
			
			allJobs = pool.getDoneList()
			if (len(allJobs) > 0):
				somethingToDisplay = True
				print "Done:"
				for i in range(0, len(allJobs)):
					if (i == len(allJobs) - 1):
						print allJobs[i] + "\n"
					else:
						print allJobs[i]
				pool.doneJobs = []

			if (somethingToDisplay == False):
				print "No jobs to display\n"
			continue

		# Kill
		elif (killRegex.search(command) != None):
			jobNum = map(int, re.findall("\d+", command))[0]
			if (len(pool.getRunningList()) <= 0):
				print "No jobs to kill\n"
				continue
			if (jobNum < 0 or jobNum >= len(pool.getRunningList())):
				print "Only type a valid job number.\n"
				continue
			print "Killing job number " + str(jobNum) + "\n"
			pool.stopGrunt(jobNum)
			continue

		# Cannot understand command
		else:
			cg_io.printError(2)
			continue

	# Try to quit, shutting down the pool
	cg_io.printQuitting()
	if (pool != 0):
		pool.shutdown()
	return

# Runs CoarseGrind in Turbo mode.
def runTurbo():
	cg_io.printWelcome()

	# Temporary
	print "Turbo mode is not yet implemented. Terminating..."
	return

# Sets up resources for CoarseGrind on startup.
# @param theScraper: The scraper to setup.
# @param unsafe: True if CoarseGrind is running in unsafe mode.
# @returns -1 if drop/add didn't exist, 0 if it did.
def _setupResources(theScraper, unsafe):
	# These operations take a long time
	theScraper.jumpToRegAndSch()
	# Unsafe?
	if (unsafe == False and theScraper.checkDropAddExists() == False):
		return -1
			
	theScraper.navigateToTimetable()
	return 0

# Stolen for StackOverflow because it's awesome :)
class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs, Verbose)
        self._return = None
    def run(self):
        if self._Thread__target is not None:
            self._return = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)
    def join(self):
        threading.Thread.join(self)
        return self._return