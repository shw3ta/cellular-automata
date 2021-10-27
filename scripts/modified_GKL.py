import numpy as np 
import math

"""
generate a large set of initial vectors with densities
close to 0.5 and store them with their correct classification
to form a test set. 

pass that into this and create instances to test on all
these ivs for a number of (j, k) combos (which you have to list too)

"""

class GKL:

	def __init__(self, iv, density):
		
		self.iv = iv
		self.density = density
		

	
	def apply_rule(self, quintuple):

		mk, mj, x, pj, pk = quintuple
		
		if x == 0:
			# maj(mk, mj, x)
			return int(math.floor(0.5 * (mk + mj + x)))
		else:
			# maj(x, pj, pk)
			return int(math.floor(0.5 * (x + pj + pk)))



	def run_automaton(self, j, k):

		prev = self.iv
		
		density = self.density #this will change with evolution
		
		ctr = 0		 
		while (density < 1 and density > 0):
			# not converged yet
			all_quintuples = np.stack(
				[np.roll(prev, -k),
				 np.roll(prev, -j),
				 prev,
				 np.roll(prev, j),
				 np.roll(prev, k)
				]
				)

			arr = []
			for i in np.apply_along_axis(self.apply_rule, 0, all_quintuples):
				arr.append(i)

			prev = np.array(arr, dtype=np.int64)

			#calculate the new density
			density = np.count_nonzero(prev == 1)/len(self.iv)
			ctr += 1			

		return density, ctr



def fetch(file):
	f = open(file)
	array = []
	line = f.readline()

	while (line != EOF):
		array.append(line)
		line = f.readline()

	f.close()
	return array
	


def main():

	# read (j, k) from a file
	# read (iv, density, maj_elmnt) from a file
	# in both cases, the delimiter is assumed to be \n

	param_list = fetch("param_list.txt")
	iv_list = fetch("iv_list.txt")

	trial_log = {"Idx:": "(actual, preds, difference, timesteps)"}

	for param, idx in  enumerate(param_list):
		j, k = param
		actual, preds, difference, timesteps = [], [], [], []

		for iv in iv_list:
			cells, density, maj_elmnt = iv
			actual.append(maj_elmnt)

			instance = GKL(cells, density)
			maj_elmnt_, steps = instance.run_automaton(j, k)

			preds.append(maj_elmnt_)
			timesteps.append(steps)

		actual = np.array(actual, np.int64)
		preds = np.array(preds, np.int64)
		timesteps = np.array(timesteps, np.int64)
		difference = actual - preds

		
		trial_log.update(idx: (actual, preds, difference, timesteps))

	f = open("trial_logs.txt", "r+")
	f.write(trial_log)
	f.close()	

main()