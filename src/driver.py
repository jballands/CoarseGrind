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
				runTurbo(arg)
				return
			elif option in ("-u", "--unsafe"):
				print "Starting in unsafe mode..."
				runNormally(True)
				return
			else:
				continue

	except getopt.GetoptError:
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
			print "Exiting...\n"
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
		evalRegex = re.compile("eval \d+")

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
				term = cg_io.requestTermSelection(mainScraper.locateAndParseTerms()[0])

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

		# Kill operation
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

		# Eval operation
		elif (evalRegex.search(command) != None):
			evalRate = map(int, re.findall("\d+", command))[0]
			if (evalRate < 5):
				print "Cannot use an evaluation rate less than 5 seconds.\n"
			else:
				pool.changeRate(evalRate)
				print "Jobs will check for open seats every " + str(evalRate) + " seconds\n"

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
# @param inputFile: The config file.
def runTurbo(inputFile):
	cg_io.printWelcome()
	print "Reading config file..."
	
	username = ''
	password = ''
	crn = ''
	term = ''

	# Match 0 to many spaces plus sought string.
	username_regex = re.compile('\S*username>')
	password_regex = re.compile('\S*password>')
	crn_regex = re.compile('\S*crn>')
	term_regex = re.compile('\S*term>')
	comment_regex = re.compile('\S*//')

	# Read the file.
	try:
		with open(inputFile) as f:

			content = f.readlines()
			for line in content:
				if (re.match(comment_regex ,line)):
					continue
				elif (re.match(username_regex, line)):
					username = re.split(username_regex, line)
				elif (re.match(password_regex, line)):
					password = re.split(password_regex, line)
				elif (re.match(crn_regex, line)):
					crn = re.split(crn_regex, line)
				elif (re.match(term_regex, line)):
					term = re.split(term_regex, line)
				else:
					continue
	except IOError:
		print "Error: Config file doesn't exist. Consult the README for more information."
		print "Exiting...\n"
		return

	if (username == '' or password == '' or crn == '' or term == ''):
		print "Error: Bad config file. Consult the README for more information."
		print "Exiting...\n"
		return

	# Parse from spliter.
	username = re.split('\n', username[1])[0]
	password = re.split('\n', password[1])[0]
	crn = re.split('\n', crn[1])[0]
	term = re.split('\n', term[1])[0]

	print 'Username: ' + str(username) + ', Term: ' + str(term) + ', CRN: ' + str(crn) + '\n'
	print "Logging in. Wait...\n"

	mainScraper = navigator.Scraper()
	mainScraper.navigateToLoginPage()
	success = mainScraper.submitToLoginPage(username, password)

	if (success == False):
		print "Invalid credentials. Check your config file and try again."
		print "Ending CoarseGrind session...\n"
		return

	print "Login successful. Welcome, " + username + "!"
	print "Preparing to do intense work. Wait...\n"

	# Jump
	mainScraper.jumpToRegAndSch()
	mainScraper.navigateToTimetable()

	# Parse
	rawTerm = cg_io.parseTerm(term)

	# See if term is available
	rawTerms = mainScraper.locateAndParseTerms()[1]
	if ((str(rawTerm) in rawTerms) == False):
		print "Invalid term. The term you provided is not available on HokieSPA."
		print "Ending Turbo session...\n"
		return

	# See if crn is valid
	if (mainScraper.submitToTimetable(rawTerms.index(str(rawTerm)), crn) == False):
		print "Invalid CRN. The CRN you provided is not a valid CRN."
		print "Ending Turbo session...\n"
		return

	# Get results for Grunt
	dictionary = mainScraper.locateAndParseTimetableResults()

	print "CoarseGrind is working furiously to add you."
	print "Turbo mode will quit automatically once CoarseGrind has added you."
	print "Job info will now be displayed."
	print "<return> at any time to stop.\n"

	# Work furiously
	pool = grinder.GruntPool(6)
	pool.releaseGrunt(dictionary, rawTerms.index(str(rawTerm)), crn, mainScraper)
	pool.broadcastDebug(True)
	raw_input("")
	pool.broadcastDebug(False)

	# Stop
	print "Ending Turbo session...\n"
	pool.shutdown()

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