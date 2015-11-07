import sys
import heapq

class Error(Exception):
	pass

"""
Methods and script to assign taxis to locations
"""

def euclidean_dist(coords_a, coords_b):
	pass

def assign emd():
	pass

def assign_naive(activity_centers, taxi_locations):
	"""
	Return a matching between activity centers and taxi locations as
	a list of tuples (center_idx, taxi_idx) -- each index (center_idx or 
	taxi_idx) refers to the imput parameters.
	
	Parameters
	----------

	activity_centers: 2d-array, shape: (num of centers x 2)
	taxi_locations: 2d-array, shape: (num of free taxis x 2)

	Return a list of index tuples.

	Requirement
	-----------
	len(activity_centers) == len(taxi_locations)
	"""

	try:
		assert(len(activity_centers) == len(taxi_locations))
	except:
		raise(Error("Number of activity centers does"
								"not match number of taxis"))

	# initialize heap
	match_heap = []

	# for each pair of center...
	for center_idx, center in enumerate(activity_centers):
		# ... and free taxi...
		for taxi_idx, taxi in enumerate(taxi_locations):
			# ... calculate their distance
			distance = euclidean_dist(center, taxi)
			heapq.heappush(match_heap, (distance, center_idx, taxi_idx))

	solution = []
	matched_taxis = set()
	while match_heap and len(matched_taxis) < len(taxi_locations):
		# pop
		distance, center_idx, taxi_idx = heapq.heappop(match_heap)

		# if taxi is not matched, add to solution
		if not taxi_idx in matched_taxis:
			solution.append(taxi_idx, center_idx)

		# add taxi index to matched taxis
		matched_taxis.add(taxi_idx)

	return solution


if __name__ == '__main__':
	pass