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
# Provides a set of "pools" for CoarseGrind to use for jobs and resource recycling.
# Provides multithreaded functionality for concurrent control flow.
#

import workerpool

class GruntPool:

	# Initializes a worker pool that grinds courses.
	# @param workers: The number of workers in the worker pool you want.
	def __init__(self, workers):
		self.pool = workerpool.WorkerPool(workers)
