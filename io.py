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

# Takes a command from the command line, displaying a prompt.
def takeCommand():
	command = raw_input("CG-v0.2$ ")
	if (command == QUIT_CMD):
		return 0
	elif (command == HELP_CMD):
		printHelp()
		return 1
	else:
		printError(2)
		return 1

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

def printLoginFailure():
	print "Invalid credientials. Please try again.\n"

# Prints an error message to the console given an error number.
def printError(errno):
	if (errno == 1):
		print "ERROR: Not on login page. Scrapper is on page: " + self.currentPage
		print "Did you call 'scraper.navigateToLoginPage() first?"
	elif (errno == 2):
		print "Invalid CoarseGrind command. Type 'help' to see commands that CoarseGrind understands.\n"

# Prints a wait message.
def waitMessage():
	print "Communicating with HokieSPA. Wait..."