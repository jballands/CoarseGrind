#
# CoarseGrind: The automated Virginia Tech course grinding script.
# (C)2013 All rights reserved. Created with love by Jonathan Ballands.
#
# ATTENTION: Distribution of this script via means other than GitHub is
# prohibited. To download, please visit: github.com/jballands/coarsegrind
#
# For more information, visit jonathanballands.me./portfolio/coarsegrind.html
#
# cg_io.py
# Contains functions that allow for I/O functionality in CoarseGrind.
#

import getpass, re

# Takes a command from the command line, displaying a prompt.
def takeCommand():
	command = raw_input("CG-v0.2-B$ ")
	return command

# Prints the help string onto the command line.
def printHelpCmdLine():
	print "\ncoarsegrind [-h] [-n|--normal] [-t|--turbo <config>] [-u|--unsafe]"
	print "-h: See this help prompt."
	print "-n|--normal: Run CoarseGrind normally. Specifying no switches\nwill also run normally."
	print "-t|--turbo: Run CoarseGrind in Turbo mode, with <config> as\nthe configuration file."
	print "-u|--unsafe: Run CoarseGrind in unsafe mode, disabling some\nsafety features. Use at your own risk. Running in unsafe mode\nmay cause undefined behavior.\n"

def printHelp():
	print "add: Try to add a class to your schedule."
	print "jobs: View a list of all the jobs CoarseGrind is running."
	print "kill <job_num>: Kills <job_num>."
	print "eval <rate>: Specifies a new class evaluation rate <rate> in seconds."
	print "help: See this help prompt."
	print "debug: Displays debugging information that reveals background activities."
	print "quit: Quits CoarseGrind.\n"

# Tries to quit CoarseGrind.
def printQuitting():
	print "Ending CoarseGrind session...\n"

# Prints the welcome message.
def printWelcome():
	print "\n~ COARSEGRIND ~\nThe automated Virginia Tech course grinding script.\n---------------------------------------------------\n(C)2013 Jonathan Ballands, v0.2 Beta\n"

# Asks for user credientials on the command line. Returns a list with the username at
# element 0 and the password at element 1.
def requestCredentials():
	print "Enter your Virginia Tech credientials. <q> at PID prompt to quit."
	name = raw_input("PID? ")
	if (name == "q"):
		return [name, "0"]
	password = getpass.getpass("Password? ")
	return [name, password]

# Prints a term selection prompt given a list of things to display.
# @param possibleTerms: A list of terms that you want to display.
# @return The selected option's value or -1 if quitting.
def requestTermSelection(possibleTerms):
	print "Choose a term. <q> to quit."
	for i in range(0, len(possibleTerms)):
		print "[" + str(i) + "]: " + possibleTerms[i]

	# Ask until valid	
	while(True):
		term = raw_input("Term? ")

		# Quit?
		if (term == "q"):
			return -1

		try:
			intTerm = int(term)
			if (intTerm > (len(possibleTerms) - 1) or intTerm < 0):
				print "Only choose a valid option number."
				continue
				
			return intTerm

		except ValueError:
			print "You must type an integer."
			continue

# Prints a CRN input.
# @return A valid CRN or -1 if quitting.
def requestCrn():
	print "Type CRN of desired class. <q> to quit."

	# Ask until valid
	while(True):
		crn = raw_input("CRN? ")

		# Quit?
		if (crn == "q"):
			return -1

		exp = re.compile('^\d{5}$')
		result = exp.match(crn)
		
		if (result):
			return crn
		else:
			print "You must type 5 consecutive integers."

# Prints an input dialog that asks to either add a class or grind a class.
# @param dictionaryL The timetable results dictionary.
# @return True if the user answered yes, false if answered no.
def requestAddAction(dictionary):
	if (dictionary["full"]):
		while (True):
			answer = raw_input("Begin grinding " + dictionary["classNumber"] + "? (y or n) ")
			if (answer == "y"):
				return True
			elif (answer == "n"):
				return False
			else:
				print "Please type y or n."
	else:
		while (True):
			answer = raw_input("Quickly add " + dictionary["classNumber"] + "? (y or n) ")
			if (answer == "y"):
				return True
			elif (answer == "n"):
				return False
			else:
				print "Please type y or n."

# Prints the timetable results dictionary provided by 
# Scraper.locateAndParseTimetableResults().
# @param dictionary: The timetable results dictionary.
def printTimetableResultDictionary(dictionary):

	print "\nQuery results:"
	print dictionary["classNumber"] + ": " + dictionary["className"]
	if (dictionary["isOnline"] == True):
		print "Online class"
	else:
		print "Days: " + dictionary["days"] + ", Duration: " + dictionary["startTime"] + " -> " + dictionary["endTime"]
	print "Credits: " + dictionary["credits"] + ", Seats: " + re.sub('Full ', '', dictionary["seats"])

def printLoginFailure():
	print "Invalid credientials. Please try again.\n"

def printNoDropAdd():
	print "\nError: CoarseGrind can't seem to find drop/add. Check to see if drop/add is online."
	print "If this is incorrect, start CoarseGrind in unsafe mode to override this error."
	print "CoarseGrind will now exit."

# Prints an error message to the console given an error number.
# @param errno: The error number.
def printError(errno):
	if (errno == 1):
		print "ERROR: Not on login page."
		print "Did you call 'scraper.navigateToLoginPage()' first?"
	elif (errno == 2):
		print "Invalid CoarseGrind command. Type <help> to see commands that CoarseGrind understands.\n"
	elif (errno == 3):
		print "ERROR: Not on registration and schedule page."
		print "Did you call 'scraper.navigateToRegAndSch()' first?"
	elif (errno == 4):
		print "ERROR: Not on timetable."
		print "Did you call 'scraper.navigateToTimetable()' first?"
	elif (errno == 5):
		print "ERROR: Not on landing page."
		print "Did you login by calling 'scraper.submitToLoginPage()' first?"
	elif (errno == 6):
		print "Invalid CRN. Verify that the CRN you provided is valid.\n"
	elif (errno == 7):
		print "ERROR: Not on drop-add page."
		print "Did you call 'scraper.navigateToDropAdd()' first?"

# Prints a wait message.
def waitMessage():
	print "Communicating with HokieSPA. Wait..."