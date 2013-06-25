#!/usr/bin/env python

#
# CoarseGrind: The automated Virginia Tech course grinding script.
# (C) 2013 All rights reserved. Programmed by Jonathan Ballands.
#
# ATTENTION: DO NOT distribute without my permission!
# This script neither saves nor distributes any information, including:
#	- Usage data
#	- Usernames and passwords
#	- Local user information
#
# CoarseGrind version 0.1
#

from bs4 import BeautifulSoup
import mechanize, sys, re, getpass, time, html5lib, threading

# The global grinding list.
grinds = []
time_check = 30

# Processes input for CoarseGrind.
class CGProcessor:

	def help_prompt(self):

		print '\n<add>: Try to add a class to your schedule.'
		print '<jobs>: View all jobs in the work queue.'
		print '<kill>: Kill a job in the work queue.'
		print '<checkrate>: Change the speed CoarseGrind checks if a class has opened.'
		print '<help>: Display the commands that CoarseGrind understands.'
		print '<quit>: Quits CoarseGrind.\n'

	def quit_prompt(self):

		print '\nThere are ' + str(len(grinds)) + ' job(s) in the queue.'

		while (1):
			answer = raw_input('Quit anyway? (yes or no) ')
			if (answer == 'yes'):
				return 1
			elif (answer == 'no'):
				return 0
			else:
				print 'Please type yes or no.'

	def kill_job(self):

		if (len(grinds) == 0):
			print '\nThere are no jobs to kill.\n'
			return

		while (1):
			answer = raw_input('\nKill which job? (<C> to cancel) ')
			if (answer == 'C'):
				return
			try:
				int_term = int(answer)
				if (int_term > (len(grinds) - 1) or grinds < 0):
					print 'Invalid job ID. Please choose a job ID between 0 and ' + str(len(grinds) - 1) + '.'
					continue
				
				# Remove the job.
				grinds.pop(int_term)
				return

			except ValueError:
				print 'Invalid input. Please type a job ID. (Ex: 2)'
				continue

	def change_rate(self):

		while (1):
			answer = raw_input('\nCheck rate? (seconds) ')

			try:
				int_term = int(answer)
				if (int_term < 10):
					print 'Cannot be less than 10 seconds. (Otherwise VT will catch onto us...)'
					continue

				# Check rate change.
				time_check = int_term
				print 'CoarseGrind will now check for available classes every ' + str(int_term) + ' seconds.\n'
				return

			except ValueError:
				print 'Invalid input. Please type an integer. (Ex: 17)'
				continue

	def print_jobs(self):

		if (len(grinds) == 0):
			print 'No jobs.'

		volitile_len = len(grinds)

		for x in range (0, volitile_len):
			print '[' + str(x) + '] ' + (grinds[x])[0] + ' -> ' + (grinds[x])[3]

			if ((grinds[x])[3] == 'DONE: Check your schedule'):
				grinds.pop(x)
				volitile_len = volitile_len + 1

	def choose_term(self, options):
		
		print '\nPlease select an term:'

		counter = 0
		for item in options:

			# Make a copy that is an int.
			copy = int(item)

			# Determine month.
			n = copy % 10

			# Get the year.
			year = (copy - (copy % 100)) / 100
			if (n == 1):
				print '[' + str(counter) + '] Spring ' + str(year)
			elif (n == 6):
				print '[' + str(counter) + '] Summer I ' + str(year)
			elif (n == 7):
				print '[' + str(counter) + '] Summer II ' + str(year)
			elif (n == 9):
				print '[' + str(counter) + '] Fall ' + str(year)
			counter = counter + 1

		while (1):
			term = raw_input('Option? ')
			try:
				int_term = int(term)
				if (int_term > (len(options) - 1) or int_term < 0):
					print 'Invalid option. Please choose an option number between 0 and ' + str(len(options) - 1) + '.'
					continue
				
				return options[int(term)]

			except ValueError:
				print 'Invalid input. Please type an option number. (Ex: 2)'
				continue

	def choose_crn(self):

		while (1):
			crn = raw_input('CRN? ')
			exp = re.compile('^\d{5}$')
			result = exp.match(crn)
			if (result):
				return crn
			else:
				print 'Invalid class CRN. Please type 5 consecutive integers. (Ex: 12345)'

	def present_results(self, class_num, class_name, prof, location, credits, seats, days, start_time, end_time, is_online):

		print '\n' + class_num + ': ' + class_name
		print 'Instructor: ' + prof + ', Location: ' + location
		if (is_online):
			print 'ONLINE CLASS'
		else:
			print 'Days: ' + days + ', Duration: ' + start_time + ' --> ' + end_time
		print 'Credits awarded: ' + credits
		print 'Seats: ' + seats + '\n'

		# Test for seats using regular expressions.
		regex_seat = re.compile('Full (0|-\d*) / [\d]*')
		test = re.match(regex_seat, seats)
		
		# There are no seats.
		if (test):
			print 'This class is full...'
			while (True):
				answer = raw_input('Start grind? (yes or no) ')
				if (answer == 'yes'):
					return 1
				elif (answer == 'no'):
					return 0
				else:
					print 'Please type yes or no.'

		# There are seats.
		print 'This class has seats available.'
		while (True):
			answer = raw_input('Add class? (yes or no) ')
			if (answer == 'yes'):
				return 2
			elif (answer == 'no'):
				return 0
			else:
				print 'Please type yes or no.'

	def present_login(self):

		# Ask for payload.
	 	name = raw_input('PID? ')
	 	password = getpass.getpass('Password? ')

	 	return [name, password]

	def choose_command(self):

		# Endlessly ask for a command until a valid one is given.
		while (1):

			command = raw_input('CoarseGrind$ ')

			if (command == 'help'):
				return 'help'

			elif (command == 'add'):
				return 'add'

			elif (command == 'quit'):
				return 'quit'

			elif (command == 'jobs'):
				return 'jobs'

			elif (command == 'kill'):
				return 'kill'

			elif (command == 'checkrate'):
				return 'checkrate'
				
			else:
				print 'Invalid command: ' + command + '. Type <help> to see commands that CoarseGrind understands.'

	# Strips HTML tags off of output.
	def strip_tags(self, html):
		if html is None:
			return None
		return ''.join(BeautifulSoup(html).findAll(text = True)) 

# Interacts with HokieSPA to perform certain functions. Not verbose.
class CGClient:

	def __init__(self):

		self.CAS = 'https://webapps.banner.vt.edu/banner-cas-prod/authorized/banner/SelfService'
		self.SchedulePage = 'https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_DispRequest'

		self.worker = mechanize.Browser()
		self.worker.set_handle_robots(False)
		self.worker.addheaders = [('User-agent', 'Firefox'),]

		self.processor = CGProcessor()
		
		self.ready = False
		self.on_schedule = False
		self.on_dropadd = False

	def attempt_login(self, username, password):
		
		# Open CAS and enter credientials.
		self.worker.open(self.CAS)
		login_dict = list(self.worker.forms())[0]
		login_dict['username'] = username
		login_dict['password'] = password

		# Set form and submit.
		self.worker.form = login_dict
		self.worker.submit()

		# Use BS to see what happened.
		soup = BeautifulSoup(self.worker.response().read())

		# Success?
		if (soup.find('div', attrs={'id' : 'login-error'}) == None):
			
			print '\nSuccess! Welcome, ' + username + '!\nGathering resources...'

			# Navigate.
			this_link = list(self.worker.links(text_regex = 'Hokie Spa'))[0]
			self.worker.follow_link(this_link)
			this_link = list(self.worker.links(text_regex = 'Registration and Schedule'))[0]
			self.worker.follow_link(this_link)

			print 'One moment please...'

			self.ready = True
			return 1

		# Not successful.
		else:

			print '\nOh snap: HokieSPA rejected your request. Please check your credientials.\n'
			return 0

	def navigate_to_schedule(self):

		if (self.ready == False):
			raise CGClientNotLoggedIn('Did you not call CGClient.attempt_login() first?')

		# Jump backwards.
		self.worker.open('https://banweb.banner.vt.edu/ssb/prod/hzskstat.P_DispRegStatPage')

		this_link = list(self.worker.links(text_regex = 'Timetable of Classes'))[0]
		self.worker.follow_link(this_link)

		self.on_schedule = True
		self.on_dropadd = False

	def check_class_status(self, crn, this_raw):

		if (self.on_schedule == False):
			raise CGClientNotOnDropAdd('Did you not call CGClient.navigate_to_schedule() first?')

		# While the crn is not good...
		good = False
		while (good == False):

			# Put info into the form.
			form = list(self.worker.forms())[1]
			self.worker.select_form('ttform')
			term_control = form.find_control('TERMYEAR')

			# Choose a term.
			term_control.value = [this_raw]

			# Choose a crn.
			crn_field = form.find_control('crn')
			crn_field.value = crn

			# Submit and see what came up.
			self.worker.submit()
			html = self.worker.response().read()
			soup = BeautifulSoup(str(html), 'html5lib')

			# Bad crn?
			if (soup.find('li', text = re.compile('NO SECTIONS FOUND FOR THIS INQUIRY.')) != None):
				print '\nThe CRN you provided is not a valid CRN for this term. Please try again.'
				continue

			good = True

		# Get some data from HokieSPA.
		data_left = soup.findAll('td', attrs = {'class' : 'deleft'})
		data_center = soup.findAll('td', attrs = {'class' : 'dedefault'})
		data_right = soup.findAll('td', attrs = {'class' : 'deright'})

		# Strip tags off.
		class_num = self.processor.strip_tags(str(data_left[0])).strip()
		class_name = self.processor.strip_tags(str(data_left[1]))
		prof = self.processor.strip_tags(str(data_left[2]))
		location = self.processor.strip_tags(str(data_left[3]))
		credits = self.processor.strip_tags(str(data_center[2])).strip()
		seats = self.processor.strip_tags(str(data_center[3])).strip()
		days = self.processor.strip_tags(str(data_center[4])).strip()

		# Online classes mess up everything.
		is_online = False

		# Online?
		if (len(data_center) == 7):
			is_online = True
		else:
			start_time = self.processor.strip_tags(str(data_right[0]))
			end_time = self.processor.strip_tags(str(data_right[1]))

		regex_seat = re.compile('Full (0|-\d*) / [\d]*')
		test = re.match(regex_seat, seats)

		# Return 0 if there are no seats and 1 if there are.
		if (test):
			return 0
		else:
			return 1

	def navigate_to_dropadd(self, raw_term):

		if (self.ready == False):
			raise CGClientNotLoggedIn('Did you not call CGClient.attempt_login() first?')

		# Jump backwards.
		self.worker.open('https://banweb.banner.vt.edu/ssb/prod/hzskstat.P_DispRegStatPage')

		# Now we are back at the page we need to be. Try to find the add course button.
		this_link = list(self.worker.links(url_regex = '/ssb/prod/bwskfreg\.P_AddDropCrse\?term_in=' + raw_term))[0]
		self.worker.follow_link(this_link)

		self.on_schedule = False
		self.on_dropadd = True

	def add_class(self, crn):

		if (self.on_dropadd == False):
			raise CGClientNotOnDropAdd('Did you not call CGClient.navigate_to_dropadd() first?')

		# Select the form and control. (Always the second form.)
		add_form = list(self.worker.forms())[1]
		self.worker.form = add_form
		term_control = add_form.find_control(id='crn_id1')
		term_control.value = str(crn)

		# Try and submit.
		self.worker.submit()	

# Interacts with the class schedule only. Verbose.
class CGDumbClient:

	def __init__(self):
		
		self.CAS = 'https://webapps.banner.vt.edu/banner-cas-prod/authorized/banner/SelfService'

		self.worker = mechanize.Browser()
		self.worker.set_handle_robots(False)
		self.worker.addheaders = [('User-agent', 'Firefox'),]

		self.processor = CGProcessor()

		self.ready = False

	def inititalize(self, username, password):

		# Open CAS and enter credientials.
		self.worker.open(self.CAS)
		login_dict = list(self.worker.forms())[0]
		login_dict['username'] = username
		login_dict['password'] = password

		# Set form and submit.
		self.worker.form = login_dict
		self.worker.submit()

		print 'Almost there...\n'

		# Navigate.
		this_link = list(self.worker.links(text_regex = 'Hokie Spa'))[0]
		self.worker.follow_link(this_link)
		this_link = list(self.worker.links(text_regex = 'Registration and Schedule'))[0]
		self.worker.follow_link(this_link)
		this_link = list(self.worker.links(text_regex = 'Timetable of Classes'))[0]
		self.worker.follow_link(this_link)

		print '...done\n'

		self.ready = True

	def check_availability(self):

		# Error check.
		if (self.ready == False):
			raise CGDumbClientNotReady('Did you not call CGDumbClient.inititalize() first?')

		# While the crn is not good...
		good = False
		this_raw = 0
		crn = 0
		while (good == False):

			# Put info into the form.
			form = list(self.worker.forms())[1]
			self.worker.select_form('ttform')
			term_control = form.find_control('TERMYEAR')

			# Choose a term.
			this_raw = self.processor.choose_term(term_control.possible_items())
			term_control.value = [str(this_raw)]

			# Choose a crn.
			crn = self.processor.choose_crn()
			crn_field = form.find_control('crn')
			crn_field.value = crn

			# Submit and see what came up.
			self.worker.submit()
			html = self.worker.response().read()
			soup = BeautifulSoup(str(html), 'html5lib')

			# Bad crn?
			if (soup.find('li', text = re.compile('NO SECTIONS FOUND FOR THIS INQUIRY.')) != None):
				print '\nThe CRN you provided is not a valid CRN for this term. Please try again.'
				continue

			good = True

		# Get some data from HokieSPA.
		data_left = soup.findAll('td', attrs = {'class' : 'deleft'})
		data_center = soup.findAll('td', attrs = {'class' : 'dedefault'})
		data_right = soup.findAll('td', attrs = {'class' : 'deright'})

		# Strip tags off.
		class_num = self.processor.strip_tags(str(data_left[0])).strip()
		class_name = self.processor.strip_tags(str(data_left[1]))
		prof = self.processor.strip_tags(str(data_left[2]))
		location = self.processor.strip_tags(str(data_left[3]))
		credits = self.processor.strip_tags(str(data_center[2])).strip()
		seats = self.processor.strip_tags(str(data_center[3])).strip()
		days = self.processor.strip_tags(str(data_center[4])).strip()

		# Online classes mess up everything.
		is_online = False

		# Online?
		if (len(data_center) == 7):
			is_online = True
		else:
			start_time = self.processor.strip_tags(str(data_right[0]))
			end_time = self.processor.strip_tags(str(data_right[1]))

		# Present information and act on it.
		choice = self.processor.present_results(class_num, class_name, prof, location, credits, seats, days, start_time, end_time, is_online)

		# 0 means do nothing. 1 means to grind. 2 means to add.
		if (choice == 0):
			print 'Cleaning...\n'
		elif (choice == 1):
			grinds.append([class_num, crn, this_raw, 'Grinding...'])
			print '\nAdded ' + class_num + ' to work queue.\nType <jobs> to view work queue.\n'
		elif (choice == 2):
			grinds.append([class_num, crn, this_raw, 'Adding...'])
			print '\nAdding ' + class_num + ' on next pass...\n'

# Grinds HokieSPA to find classes.
class CGGrinder(threading.Thread):

	def __init__(self, cli):

		threading.Thread.__init__(self)
		self.stop_event = threading.Event()
		self.client = cli

	def stop(self):
		self.stop_event.set()

	def run(self):

		# While the thread is alive...
		while not self.stop_event.isSet():

			for x in range (0, time_check):
				time.sleep(1)

				# Quit?
				if self.stop_event.isSet():
					break
			
			# Check the grinding list.
			for x in range (0, len(grinds)):

				# Done?
				if ((grinds[x])[3] == 'DONE: Check your schedule'):
					continue

				self.client.navigate_to_schedule()
				status = self.client.check_class_status((grinds[x])[1], (grinds[x])[2])

				if (status == 1):
					self.client.navigate_to_dropadd((grinds[x])[2])
					self.client.add_class((grinds[x])[1])
					(grinds[x])[3] = 'DONE: Check your schedule'

				# Quit?
				if self.stop_event.isSet():
					break

# MAIN
def main():

	print '\n~ COARSEGRIND ~\nThe automated Virginia Tech course grinding script.\n---------------------------------------------------\n(C)2013 Jonathan Ballands, Version 0.1\n'

	print 'COARSEGRIND MAY STILL CONTAIN BUGS.\nIf you encounter a bug, email jballands@gmail.com\n'

	# Init.
	client = CGClient()
	processor = CGProcessor()

	# Try and login.
	ok = 0
	credientials = 0
	while (ok == 0):

		credientials = processor.present_login()
		ok = client.attempt_login(credientials[0], credientials[1])

	# More init.
	dumb_client = CGDumbClient()
	dumb_client.inititalize(credientials[0], credientials[1])
	grinding_thread = CGGrinder(client)
	grinding_thread.start()

	# Runtime loop.
	ok = 0
	while (ok == 0):

		option = processor.choose_command()

		if option == 'add':
			dumb_client.check_availability()

		elif option == 'jobs':
			print '\n'
			processor.print_jobs()
			print '\n'

		elif option == 'quit':
			if (len(grinds) > 0):
				answer = processor.quit_prompt()
				if (answer == 0):
					continue
			grinding_thread.stop()
			ok = 1

		elif option == 'help':
			processor.help_prompt()

		elif option == 'kill':
			processor.kill_job()

		elif option == 'checkrate':
			processor.change_rate()

	# Done.
	return

if __name__ == "__main__":
    main()
