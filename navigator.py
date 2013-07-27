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

import mechanize, html5lib
from bs4 import BeautifulSoup

# The scraper class that you should instantiate in order to crawl HokieSPA.
class Scraper:

	# Constants, do not modify
	LOGIN_PAGE = "login_page"
	REGISTRATION_AND_SCHEDULE = "registration_and_schedule"
	CAS = "https://webapps.banner.vt.edu/banner-cas-prod/authorized/banner/SelfService"
	browseSchForm = "https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_DispRequest"
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
		self.browser.open(self.CAS)
		self.currentPage = self.LOGIN_PAGE

	# Submits login data to the login page.
	# @param username: The username.
	# @param password: The password.
	# @return True on success, False on failure.
	def submitToLoginPage(self, username, password):
		# On login page?
		if (self.currentPage != self.LOGIN_PAGE):
			io.printError(1)
			exit(1)
		return _attemptLogin(username, password, self.browser)

	def navigateToRegAndSch(self):
		this_link = list(self.browser.links(text_regex = 'Hokie Spa'))[0]
		self.browser.follow_link(this_link)
		this_link = list(self.browser.links(text_regex = 'Registration and Schedule'))[0]
		self.browser.follow_link(this_link)
		self.currentPage = self.REGISTRATION_AND_SCHEDULE

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