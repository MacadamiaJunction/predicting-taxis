import numpy as np

class TaxiState(object):
	"""
	Class to maintain the state of all taxis at any time
	"""

	def _build_taxi_status(taxi_locations):
		"""
		create a dictionary that stores the status of each taxi
		each taxi
		NOTE: 
		status = (REST, position coordinates) or
		status = (MOVE, start_time, start_position, end_time, end_position)
		"""
		pass

	def __init__(self, start_time, taxi_locations):
		"""
		initialize state
		"""
		# set your clock!
		self.clock = start_time

		# initialize taxi status
		# status = (MOVE / REST, position coordinates)
		self.taxi_status = _build_taxi_status(taxi_locations)
		

	def update_taxi_status(self, to_time):
		"""
		forward-update the status of taxis for time to_time
		"""
		pass

	def progress_to(self, to_time):
		"""
		simply move the time forward the time
		"""

		if to_time > self.time:
			self.time = to_time
			update_taxi_status(self, to_time)
			

	def call(taxi_id, pickup_time, pickup_loc,
			drop_time, drop_loc):
		"""
		One taxi is called
		"""
		pass

	def get_taxi_locations():
		pass

if __name__ == '__main__':
	pass