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
# @throws urllib2.URLError exception when connection times out.
class Scraper:

	def __init__(self):
		# Make a browser
		self.browser = mechanize.Browser()
		self.browser.set_handle_robots(False)
		self.browser.addheaders = [("User-agent", "Firefox"),]

		# Constants, do not modify
		self.LOGIN_PAGE = "login_page"
		self.REGISTRATION_AND_SCHEDULE = "registration_and_schedule"
		self.TIMETABLE = "timetable"
		self.LANDING_PAGE = "landing_page"
		self.DROP_ADD = "drop_add"
		self.CASLink = "https://webapps.banner.vt.edu/banner-cas-prod/authorized/banner/SelfService"
		self.timetableLink = "https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_DispRequest"
		self.regAndSchLink = "https://banweb.banner.vt.edu/ssb/prod/hzskstat.P_DispRegStatPage"
		self.currentPage = -1

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
			exit(-1)
		result = _attemptLogin(username, password, self.browser)
		if (result == True):
			self.currentPage = self.LANDING_PAGE
		return result

	# From the landing_page sends scraper to registration and schedule page.
	def navigateToRegAndSch(self):
		if (self.currentPage != self.LANDING_PAGE):
			cg_io.printError(5)
			print "Terminating...\n"
			exit(-1)

		this_link = list(self.browser.links(text_regex = 'Hokie Spa'))[0]
		self.browser.follow_link(this_link)
		this_link = list(self.browser.links(text_regex = 'Registration and Schedule'))[0]
		self.browser.follow_link(this_link)
		self.currentPage = self.REGISTRATION_AND_SCHEDULE

	# Deprecated: This function is too slow and prone to error. Use 'jumpToRegAndSch()' instead.
	# Navigates the scrapper to the timetable.
	def navigateToTimetable(self):
		if (self.currentPage != self.REGISTRATION_AND_SCHEDULE):
			cg_io.printError(3)
			print "Terminating...\n"
			exit(-1)

		this_link = list(self.browser.links(text_regex = 'Timetable of Classes'))[0]
		self.browser.follow_link(this_link)
		self.currentPage = self.TIMETABLE

	# See Issue #3 on GitHub. This function is causing unexpected behavior!!
	# If on the registration and schedule page, returns a parsed list of acceptable terms.
	# @return An array with a parsed list of terms and the corresponding raw items.
	def locateAndParseTerms(self):
		if (self.currentPage != self.TIMETABLE):
			cg_io.printError(4)
			print "Terminating...\n"
			exit(-1)
			
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

		return [parsedItems, rawItems]

	# Submits data to the timetable and tries to get a result.
	# @param term: The term to select.
	# @param crn: The crn to submit with.
	# @return True if HokieSPA took the data, false if HokieSPA rejected it.
	def submitToTimetable(self, term, crn):
		if (self.currentPage != self.TIMETABLE):
			cg_io.printError(4)
			print "Terminating...\n"
			exit(-1)

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
		self.currentPage = self.TIMETABLE
		return True

	# If on the registration and schedule page, returns a parsed dictionary of timetable results.
	# @return A dictionary of timetable results. If the value of 'isOnline' is True, then the 
	# value of 'startTime' and 'endTime' will be -1.
	def locateAndParseTimetableResults(self):
		if (self.currentPage != self.TIMETABLE):
			cg_io.printError(6)
			print "Terminating..."

		html = self.browser.response().read()
		soup = BeautifulSoup(str(html), 'html5lib')

		data_left = soup.findAll('td', attrs = {'class' : 'deleft'})
		data_center = soup.findAll('td', attrs = {'class' : 'dedefault'})
		data_right = soup.findAll('td', attrs = {'class' : 'deright'})

		class_num = _stripTags(str(data_left[0])).strip()
		class_name = _stripTags(str(data_left[1]))
		prof = _stripTags(str(data_left[2]))
		location = _stripTags(str(data_left[3]))
		credits = _stripTags(str(data_center[2])).strip()
		seats = _stripTags(str(data_center[3])).strip()
		days = _stripTags(str(data_center[4])).strip()

		# Declare
		isOnline = False
		startTime = -1
		endTime = -1

		# Online?
		if (len(data_center) == 7):
			isOnline = True
		else:
			startTime =_stripTags(str(data_right[0]))
			endTime = _stripTags(str(data_right[1]))

		regexSeat = re.compile('Full (0|-\d*) / [\d]*')
		classFull = re.match(regexSeat, seats)

		return {"classNumber": class_num, "className": class_name, "professor": prof, 
			    "location": location, "credits": credits, "seats": seats, "days": days, 
			    "isOnline": isOnline, "startTime": startTime, "endTime": endTime, 
			    "full": classFull}

	# Jumps scraper to the registration and schedule page.		    
	def jumpToRegAndSch(self):
		self.browser.open(self.regAndSchLink)
		self.currentPage = self.REGISTRATION_AND_SCHEDULE

	# Jumps scraper to the timetable page. Should be used after logging in.
	def jumpToTimetable(self):
		self.browser.open(self.timetableLink)
		self.currentPage = self.TIMETABLE

	# Navigates to the drop/add page on HokieSPA.
	# @param term: The term to enter on drop/add.
	# @returns -1 if drop/add isn't open.
	def navigateToDropAdd(self, term):
		if (self.currentPage != self.REGISTRATION_AND_SCHEDULE):
			cg_io.printError(3)
			print "Terminating..."
			exit(-1)

		# Try to find the add course button
		theseLinks = list(self.browser.links(url_regex = '/ssb/prod/bwskfreg\.P_AddDropCrse\?term_in=' + str(term)))

		self.browser.follow_link(these_links[0])
		self.currentPage = self.DROP_ADD

	# Simply checks the existance of drop/add.
	# @param term: The term to enter on drop/add.
	# @returns False if drop/add is no available, true if it is.
	def checkDropAddExists(self):
		if (self.currentPage != self.REGISTRATION_AND_SCHEDULE):
			cg_io.printError(3)
			print "Terminating..."
			exit(-1)

		# Try to find the add course button
		theseLinks = list(self.browser.links(text_regex = 'Drop/Add'))

		# If drop/add isn't open
		if (len(theseLinks) == 0):
			return False
		return True

	# Submits to the drop/add page.
	# @param crn: The crn to submit with.
	def submitToDropAdd(self, crn):
		if (self.currentPage != self.DROP_ADD):
			cg_io.printError(7)
			print "Terminating..."
			exit(-1)

		# Select the form and control
		addForm = list(self.browser.forms())[1]
		self.browser.form = addForm
		termControl = addForm.find_control(id='crn_id1')
		termControl.value = str(crn)

		# Try and submit
		self.browser.submit()

# Creates a clone of a scraper.
# @param scraper: The scraper to clone.
# @return The clone.
def clone(scraper):
	if (scraper.browser.response() != None):
		newScraper = Scraper()
		theCookieJar = scraper.browser._ua_handlers['_cookies'].cookiejar

		newScraper.browser.set_response(scraper.browser.response())
		newScraper.browser._ua_handlers['_cookies'].cookiejar = theCookieJar

		return newScraper
		

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

# Private function
# Strips HTML tags off of output.
# @param html: The HTML to strip.
# @returns Only text that resided in the HTML with no tags.
def _stripTags(html):
	if html is None:
		return None
	return ''.join(BeautifulSoup(html).findAll(text = True)) 