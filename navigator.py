#
# CoarseGrind: The automated Virginia Tech course grinding script.
# (C)2013 All rights reserved. Created with love by Jonathan Ballands.
#
# ATTENTION: Distribution of this script via means other than GitHub is
# prohibited. To download, please visit: github.com/jballands/coarsegrind
#
# For more information, visit jonathanballands.me./portfolio/coarsegrind.html
#
# navigator.py
# Allows CoarseGrind to crawl HokieSPA.
#

import mechanize, html5lib, cg_io, re
from bs4 import BeautifulSoup

# The scraper class that you should instantiate in order to crawl HokieSPA.
class Scraper:

	# Constants, do not modify
	LOGIN_PAGE = "login_page"
	REGISTRATION_AND_SCHEDULE = "registration_and_schedule"
	TIMETABLE = "timetable"
	LANDING_PAGE = "landing_page"
	CASLink = "https://webapps.banner.vt.edu/banner-cas-prod/authorized/banner/SelfService"
	timetableLink = "https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_DispRequest"
	currentPage = -1

	def __init__(self):
		# Make a browser
		self.browser = mechanize.Browser()
		self.browser.set_handle_robots(False)
		self.browser.addheaders = [("User-agent", "Firefox"),]

	# Returns a string that describes where this scraper exists. Mostly
	# used for debugging purposes.
	def whereAmI(self):
		return currentPage

	# Sends scraper to login page.
	def navigateToLoginPage(self):
		self.browser.open(self.CASLink)
		self.currentPage = self.LOGIN_PAGE

	# Submits login data to the login page.
	# @param username: The username.
	# @param password: The password.
	# @return True on success, False on failure.
	def submitToLoginPage(self, username, password):
		# On login page?
		if (self.currentPage != self.LOGIN_PAGE):
			cg_io.printError(1)
			print "Terminating...\n"
			exit(1)
		result = _attemptLogin(username, password, self.browser)
		if (result == True):
			self.currentPage = self.LANDING_PAGE
		return result

	# From the landing_page sends scraper to registration and schedule page.
	def navigateToRegAndSch(self):
		if (self.currentPage != self.LANDING_PAGE):
			cg_io.printError(5)
			print "Terminating...\n"
			exit(5)

		this_link = list(self.browser.links(text_regex = 'Hokie Spa'))[0]
		self.browser.follow_link(this_link)
		this_link = list(self.browser.links(text_regex = 'Registration and Schedule'))[0]
		self.browser.follow_link(this_link)
		self.currentPage = self.REGISTRATION_AND_SCHEDULE

	# Jumps the scrapper to the timetable.
	def navigateToTimetable(self):
		if (self.currentPage != self.REGISTRATION_AND_SCHEDULE):
			cg_io.printError(3)
			print "Terminating...\n"
			exit(3)
		this_link = list(self.browser.links(text_regex = 'Timetable of Classes'))[0]
		self.browser.follow_link(this_link)
		self.currentPage = self.TIMETABLE

	# If on the registration and schedule page, returns a parsed list of acceptable terms.
	# @return A parsed list of terms.
	def locateAndParseTerms(self):
		if (self.currentPage != self.TIMETABLE):
			cg_io.printError(4)
			print "Terminating...\n"
			exit(4)

		rawItems = list(self.browser.forms())[1].find_control("TERMYEAR").possible_items()
		parsedItems = []
		for item in rawItems:
			item = int(item)

			# Math
			month = item % 10
			year = (item - (item % 100)) / 100

			if (month == 1):
				month = "Spring"
			elif (month == 6):
				month = "Summer I"
			elif (month == 7):
				month = "Summer II"
			elif (month == 9):
				month = "Fall"

			parsedItems.append(month + " " + str(year))

		return parsedItems

	# Submits data to the timetable and tries to get a result.
	# @param term: The term to select.
	# @param crn: The crn to submit with.
	# @return True if HokieSPA took the data, false if HokieSPA rejected it.
	def submitToTimetable(self, term, crn):
		self.browser.select_form('ttform')
		form = list(self.browser.forms())[1]
		termYear = form.find_control("TERMYEAR")
		termYear.value = [str(termYear.possible_items()[term])]
		form.find_control('crn').value = crn

		# Submit
		self.browser.submit()

		# Check validity
		html = self.browser.response().read()
		soup = BeautifulSoup(str(html), 'html5lib')

		# Bad crn?
		if (soup.find('li', text = re.compile('NO SECTIONS FOUND FOR THIS INQUIRY.')) != None):
			return False

		# Ok
		return True

# Private function
# Attempts to login to HokieSPA.
# @param username: The username.
# @param password: The password.
# @param browser: The browser to navigate with.
# @return True on success, False on failure.
def _attemptLogin(username, password, browser):
	
	# Get the first form
	login_dict = list(browser.forms())[0]
	login_dict['username'] = username
	login_dict['password'] = password
		
	# Set form and submit
	browser.form = login_dict
	browser.submit()

	# Use BS to see what happened
	soup = BeautifulSoup(browser.response().read())

	# Success?
	if (soup.find('div', attrs={'id' : 'login-error'}) == None):
		return True

	# Failure	
	return False