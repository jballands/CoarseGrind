#
# CoarseGrind: The automated Virginia Tech course grinding script.
# (C)2013 All rights reserved. Created with love by Jonathan Ballands.
#
# ATTENTION: Distribution of this script via means other than GitHub is
# prohibited. To download, please visit: github.com/jballands/coarsegrind
#
# For more information, visit jonathanballands.me./portfolio/coarsegrind.html
#
# grinder.py
# Eagerly provides a pool of worker threads that endlessly try to add a course
# to a student's schedule.
#

import threading, copy, time

class GruntPool:

	# Initializes a grunt pool that grinds courses.
	# @param size: The number of grunts in the pool.
	# @param rate: The evaluation rate that all Grunts in the pool should adhere to.
	def __init__(self, rate):
		self.listSemaphore = threading.Semaphore()
		self.grunts = []
		self.runningJobs = []
		self.doneJobs = []
		self.checkRate = rate

	# Adds a grunt to the pool.
	# @param dictionary: A dictionary that allows the Grunt to do work.
	# @param term: The index of the chosen term in the term control.
	# @param crn: The crn of the course you want to the Grunt to act on.
	# @param browser: A scraper that this Grunt can use.
	def releaseGrunt(self, dictionary, term, crn, scraper):
		thisGrunt = Job(dictionary, term, crn, self.checkRate, self.runningJobs, self.doneJobs, self.grunts, self.listSemaphore, scraper)
		thisGrunt.start()
		self.grunts.append(thisGrunt)

		self.listSemaphore.acquire()
		self.runningJobs.append(dictionary["classNumber"])
		self.listSemaphore.release()

	# Shuts down this Grunt pool.
	def shutdown(self):
		for i in range(0, len(self.grunts)):
			self.grunts[i].stop()
			self.grunts[i].join()

	# Stops a specific Grunt.
	# @param index: The index of the Grunt to stop.
	def stopGrunt(self, index):
		self.grunts[index].stop()
		self.grunts.remove(self)

	# Gets a list of all the running Grunts running in a pretty format,
	# suitable for printing.
	def getRunningList(self):
		return self.runningJobs

	# Gets a list of all the done Grunts running in a pretty format,
	# suitable for printing.
	def getDoneList(self):
		return self.doneJobs

	# Changes the evaluation rate for all jobs in the pool.
	# @param rate: The new rate.
	def changeRate(self, rate):
		for grunt in self.grunts:
			grunt.changeRate(rate)
		self.checkRate = rate

	# Broadcasts a debug message to all Grunts, such that they print debug info.
	# @param on: True to turn debugging on, false to turn it off.
	def broadcastDebug(self, on):
		for grunt in self.grunts:
			grunt.setDebug(on)

class Job(threading.Thread):

	# Initializes a job that a worker thread can perform.
	# @param dictionary: A dictionary that allows the job to run.
	# @param term: The index of the term selected in the term control.
	# @param crn: The crn you want this Grunt to act on.
	# @param rate: The evaluation rate this job adheres to.
	# @param running: A list of all the running jobs.
	# @param done: A list of all the done jobs.
	# @param grunts: A list of all the grunts.
	# @param semaphore: The list semaphore.
	# @param scrapper: The scrapper that this job will use.
	def __init__(self, dictionary, term, crn, rate, running, done, grunts, semaphore, scraper):
		super(Job, self).__init__()

		# Set constants
		self.jobItems = dictionary
		self.stopEvent = threading.Event()
		self.checkRate = rate
		self.runningJobs = running
		self.doneJobs = done
		self.listSemaphore = semaphore
		self.scraper = scraper
		self.term = term
		self.crn = crn
		self.grunts = grunts
		self.debug = False
		self.debugSemaphore = threading.Semaphore()

	# See Issue #2 on GitHub, as this function contains a known bug!!
	# Runs the job, endlessly checking to see if a course is ready to add.
	def run(self):
		hasOpenSeat = False

		# Endlessly check for an open seat
		while (hasOpenSeat == False):
			self.debugSemaphore.acquire()
			if (self.debug == True):
				print "Job " + self.jobItems["classNumber"] + " checking timetable..."
			self.debugSemaphore.release()

			self.scraper.jumpToTimetable()
			self.scraper.submitToTimetable(self.term, self.crn)
			results = self.scraper.locateAndParseTimetableResults()
			if (results["full"] == None):
				hasOpenSeat = True
			else:
				self.debugSemaphore.acquire()
				if (self.debug == True):
					print "Job " + self.jobItems["classNumber"] + " was full. Going to sleep..."
				self.debugSemaphore.release()

				# Sleeping loop
				copyRate = copy.deepcopy(self.checkRate)
				for x in range(0, copyRate):
					time.sleep(1)
					if self.stopEvent.isSet():
						return

				self.debugSemaphore.acquire()
				if (self.debug == True):
					print "Job " + self.jobItems["classNumber"] + " woke up!"
				self.debugSemaphore.release()

		self.debugSemaphore.acquire()
		if (self.debug == True):
			print "Job " + self.jobItems["classNumber"] + " had seats open!!! Quickly adding..."
		self.debugSemaphore.release()

		# Quickly try to add the course
		self.scraper.jumpToRegAndSch()
		self.scraper.navigateToDropAdd(self.term)

		# BUGGY LINE
		self.scraper.submitToDropAdd(self.crn)

		self.listSemaphore.acquire()
		self.runningJobs.remove(self.jobItems["classNumber"])
		self.doneJobs.append(self.jobItems["classNumber"])
		self.grunts.remove(self)
		self.listSemaphore.release()

		self.debugSemaphore.acquire()
		if (self.debug == True):
			print "Job " + self.jobItems["classNumber"] + " finished"
		self.debugSemaphore.release()

	# Stops this job.
	def stop(self):
		self.stopEvent.set()
		self.listSemaphore.acquire()
		self.runningJobs.remove(self.jobItems["classNumber"])
		self.doneJobs.append(self.jobItems["classNumber"] + " - stopped by user")
		self.listSemaphore.release()

	# Changes the check rate of this job.
	# @param rate: The new rate.
	def changeRate(self, rate):
		self.checkRate = rate

	# Turns on debugging mode for this Grunt.
	# @param on: True to turn on debugging, false to turn it off.
	def setDebug(self, on):
		self.debugSemaphore.acquire()
		self.debug = on
		self.debugSemaphore.release()