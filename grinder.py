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

import threading, copy

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
	def releaseGrunt(self, dictionary):
		thisGrunt = Job(dictionary, self.checkRate, self.runningJobs, self.doneJobs, self.listSemaphore)
		thisGrunt.start()
		self.grunts.append(thisGrunt)

		self.listSemaphore.acquire()
		self.prettyList.append(dictionary["classNumber"])
		self.listSemaphore.release()

	# Shuts down this Grunt pool.
	def shutdown(self):]
		for grunt in self.readyGrunts:
			grunt.stop()
			grunt.join()

	# Gets a list of all the running Grunts running in a pretty format,
	# suitable for printing.
	def getRunningList(self):
		return self.runningJobs

	def getDoneList(self):
		self.listSemaphore.acquire()
		copyList = copy.copy(doneJobs)
		doneJobs = []
		self.listSemaphore.release()
		return copyList

class Job(threading.Thread):

	# Initializes a job that a worker thread can perform.
	# @param dictionary: A dictionary that allows the job to run.
	# @param rate: The evaluation rate this job adheres to.
	# @param running: A list of all the running jobs.
	# @param done: A list of all the done jobs.
	# @param semaphore: The list semaphore.
	def __init__(self, dictionary, rate, running, done, semaphore):
		self.jobItems = dictionary
		self.stopEvent = threading.Event()
		self.checkRate = rate
		self.runningJobs = running
		self.doneJobs = done
		checkRateSemaphore = threading.Semaphore()
		self.listSemaphore = semaphore

	# See Issue #2 on GitHub, as this function contains a known bug!!
	# Runs the job, endlessly checking to see if a course is ready to add.
	def run(self):
		hasOpenSeat = False

		# Endlessly check for an open seat
		while (hasOpenSeat == False):

			self.browser.submitToTimetable(jobItems["term"], jobItems["crn"])
			results = self.browser.locateAndParseTimetableResults()
			if (results["full"] == None):
				hasOpenSeat == True
			checkRateSemaphore.acquire()
			for (x in range(0, checkRate * 2)):
				time.sleep(0.5)
				if self.stopEvent.isSet():
					return
			checkRateSemaphore.release()

		# Quickly try to add the course
		self.browser.jumpToRegAndSch()
		self.browser.navigateToDropAdd(dictionary["term"])
		# BUGGY LINE
		self.browser.submitToDropAdd(dictionary["crn"])

		self.listSemaphore.acquire()
		self.runningJobs.remove(jobItems["classNumber"])
		self.doneJobs.append(jobItems["classNumber"])
		self.listSemaphore.release()

	# Stops this job.
	def stop(self):
		self.stopEvent.set()

	# Changes the check rate of this job.
	# @param rate: The new rate.
	def changeRate(self, rate):
		self.checkRateSemaphore.acquire()
		self.checkRate = rate
		self.checkRateSemaphore.release()