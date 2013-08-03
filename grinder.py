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

import workerpool

class GruntPool:

	# Initializes a worker pool that grinds courses.
	# @param workers: The number of workers in the worker pool you want.
	def __init__(self, workers):
		self.pool = workerpool.WorkerPool(workers)

class CoarseGrindJob(workerpool.Job):

	# Initializes a job that a worker thread can perform.
	# @param dictionary: A dictionary that allows the job to run.
	def __init__(self, dictionary):
		self.workItems = dictionary

	# See Issue #2 on GitHub, as this function contains a known bug!!
	# Runs the job, endlessly checking to see if a course is ready to add.
	def run(self):
		hasOpenSeat = False

		# Endlessly check for an open seat
		while (hasOpenSeat == False):

			self.browser.submitToTimetable(dictionary["term"], dictionary["crn"])
			results = self.browser.locateAndParseTimetableResults()
			if (results["full"] == None):
				hasOpenSeat == True


		# Quickly try to add the course
		self.browser.jumpToRegAndSch()
		self.browser.navigateToDropAdd(dictionary["term"])
		# BUGGY LINE
		self.browser.submitToDropAdd(dictionary["crn"])

class Grunts:

	# Initializes a collection of Grunts that contain data to help them do work.
	# @param master: A browser that has already navigated to the timetable page.
	# @param rate: The evaluation rate that the grunts run by.
	def __init__(self, master, rate):
		self.checkRate = rate
		self.browser = master
		self.list = []

	# Adds a grunt to the grunt collection.
	# @param crn: The crn the grunt pertains to.
	# @param term: The term the grunt pertains to.
	def addGrunt(self, crn, term):
		thisGrunt = {"crn": crn, "term": term, "rate": self.checkRate}
		self.list.append(thisGrunt)

	# Removes a grunt from the grunt collection.
	# @param grunt: The grunt to remove.
	def removeGrunt(self, grunt):
		self.list.remove(grunt)
