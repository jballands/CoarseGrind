#
# CoarseGrind: The automated Virginia Tech course grinding script.
# (C)2013 All rights reserved. Created with love by Jonathan Ballands.
#
# ATTENTION: Distribution of this script via means other than GitHub is
# prohibited. To download, please visit: github.com/jballands/coarsegrind
#
# For more information, visit jonathanballands.me./portfolio/coarsegrind.html
#
# io.py
# Contains functions that allow for I/O functionality in CoarseGrind.
#

import getpass

QUIT_CMD = "quit"
HELP_CMD = "help"
ADD_CMD = "add"

# Takes a command from the command line, displaying a prompt.
def takeCommand():
	command = raw_input("CG-v0.2$ ")
	if (command == QUIT_CMD):
		return 0
	elif (command == HELP_CMD):
		printHelp()
		return 1
	elif (command == ADD_CMD):
		return 2
	else:
		printError(2)
		return 7

# Prints the help string onto the command line.
def printHelpCmdLine():
	print "\ncoarsegrind [-h] [-n|--normal] [-t|--turbo <config>]"
	print "-h: See this help prompt."
	print "-n|--normal: Run CoarseGrind normally. Specifying no switches will also run normally."
	print "-t|--turbo: Run CoarseGrind in Turbo mode, with <config> as the configuration file.\n"

def printHelp():
	print "add: Try to add a class to your schedule."
	print "jobs: View a list of all the jobs CoarseGrind is running."
	print "kill <job_num>: Kills <job_num>."
	print "checkrate <rate>: Specifies a new grinding rate <rate> in seconds."
	print "help: See this help prompt."
	print "quit: Quits CoarseGrind.\n"

# Tries to quit CoarseGrind.
def tryQuit():
	print "Ending CoarseGrind session...\n"

# Prints the welcome message.
def printWelcome():
	print "\n~ COARSEGRIND ~\nThe automated Virginia Tech course grinding script.\n---------------------------------------------------\n(C)2013 Jonathan Ballands, v0.2\n"

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
# @return The index of the option selected or -1 if quitting.
def requestTermSelection(possibleTerms):
	print "Available terms:"
	for i in range(0, len(possibleTerms)):
		print "[" + str(i) + "]: " + possibleTerms[i]

	# Ask until valid	
	while(True):
		term = raw_input("Term? ")

		# Quit?
		if (term == "q"):
			return -1

		try:
			int_term = int(term)
			if (int_term > (len(possibleTerms) - 1) or int_term < 0):
				print "Only choose an option number between 0 and " + str(len(possibleTerms) - 1) + "."
				continue
				
			return possibleTerms[int_term]

		except ValueError:
			print "You must type an integer."
			continue

def printLoginFailure():
	print "Invalid credientials. Please try again.\n"

# Prints an error message to the console given an error number.
def printError(errno):
	if (errno == 1):
		print "ERROR: Not on login page."
		print "Did you call 'scraper.navigateToLoginPage()' first?"
	elif (errno == 2):
		print "Invalid CoarseGrind command. Type 'help' to see commands that CoarseGrind understands.\n"
	elif (errno == 3):
		print "ERROR: Not on registration and schedule page."
		print "Did you call 'scraper.navigateToRegAndSch()' first?"
	elif (errno == 4):
		print "ERROR: Not on timetable."
		print "Did you call 'scraper.navigateToTimetable()' first?"
	elif (errno == 5):
		print "ERROR: Not on landing page."
		print "Did you login by calling 'scraper.submitToLoginPage()' first?"

# Prints a wait message.
def waitMessage():
	print "Communicating with HokieSPA. Wait..."