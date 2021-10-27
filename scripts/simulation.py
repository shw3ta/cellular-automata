import numpy as np
import math

random_seed = np.random.RandomState(242976)

class GKL_CA:

	def __init__(self):
		self.length = 0
		self.cells = []
		self.limit_evolution = 0
		# density => density of 1s in the state array
		self.density = 0

	def trials_set_up(self, density):
		self.length = 150
		self.limit_evolution = 400
		self.density = density

	def set_properties(self):
		self.length = int(input("\nEnter the length of your GKL state array: "))

		# here, we don't want to set the number of generations beforehand because we need it to run till convergence
		self.limit_evolution = int(input("\nEnter the max number of evolutions you want to observe: "))

		self.density = float(input("\nEnter the density of 1s in the initialization vector (make sure to enter values between [0,1]): "))


	def init_cells(self):
		# here we want the exact proportion of 1s to 0s as is specified by user input density
		K = int(self.length * self.density)
		arr = np.array([1] * K  +  [0] * (self.length - K))
		np.random.shuffle(arr)
		self.cells = arr

		#print(self.cells)

	def apply_rule(self, quintuple):
		m3, m1, x, p1, p3 = quintuple
		x_ = 0

		if x == 0:
			# maj(m3, m1, x)
			x_ = int(math.floor(0.5 * (m3 + m1 + x)))
		else:
			# maj(x, p1, p3)
			x_ = int(math.floor(0.5 * (x + p1 + p3)))

		return x_

	def run_automaton(self):
		history = np.zeros((self.limit_evolution, self.length)) # 2D array
		#print(history.shape)
		history[0, :] = self.cells # start here

		density = self.density #this will change with evolution
		if density == 1 or density == 0:
			# all ones already
			print("Not interesting behaviour, exeunt.\nIt will be homogeneous from the start to end.\n")
			exit(1)

		ctr = 1		 
		while (density < 1 and density > 0 and ctr < self.limit_evolution):
			# not converged yet
			all_quintuples = np.stack(
				[np.roll(history[ctr-1, :], -3),
				 np.roll(history[ctr-1, :], -1),
				 history[ctr-1, :],
				 np.roll(history[ctr-1, :], 1),
				 np.roll(history[ctr-1, :], 3)
				]
				)
			arr = []
			for i in np.apply_along_axis(self.apply_rule, 0, all_quintuples):
				arr.append(i)

			history[ctr, :] = np.array(arr, dtype=np.int64)

			#calculate the new density
			density = np.count_nonzero(history[ctr, :] == 1)/self.length
			ctr += 1			

		return history, density, ctr			

	

class E_CA:

	def __init__(self):
		self.ruleset = []
		self.length = 0
		self.cells = []
		self.generations = 0

	def set_properties(self):
		self.length = int(input("\nEnter the length of the 1-D CA: "))

		self.generations = int(input("\nEnter the number of generations of CA you want to observe: "))
	
		rule_num = int(input("\nEnter integer rule number for this automaton: "))

		f = open("rules.txt", "r")
		ruleset_str = f.readlines()[rule_num][: : -1] #reversing to avoid incorrect mapping
		#print(ruleset_str)
		self.ruleset = [char for char in ruleset_str][1:] # first char in this list is '\n' so reading from char 2 on
		#print(self.ruleset)
		f.close()	
		

	def init_cells(self):
		"""
		Cases to add:

		1. to check the additive property
		2. to probe the behaviour of ideal rules
		
		"""
		type_init = input("\nEnter a for random initialization.\nEnter b to initialize only the middle cell to '1'.\nEnter c to invert case b.\n\nEnter your choice here:")

		ctr = 0
		while type_init not in "abcmj":
			if ctr > 4:
				print("\nToo many wrong tries, bubye.\n")
				exit(1)

			type_init = input("\nInvalid input! Choose from a, b or c: ")

		if type_init == "a":
			self.cells = random_seed.randint(0, 2, self.length)

		elif type_init == "b":
			self.cells = np.zeros(self.length, dtype=np.int64)
			m = (self.length//2) - 1
			self.cells[m] = 1

		elif type_init == "c":
			self.cells = np.ones(self.length, dtype=np.int64)
			m = (self.length//2) - 1
			self.cells[m] = 0

		elif type_init == "mj":
			string = "0110100001101001001000000111011101100101001000000110110001101111011101100110010100100000011110010110111101110101"
			self.length = len(string)
			self.cells = np.ones(len(string), dtype=np.int64)
			for i,char in enumerate(string):
				if char == "0": self.cells[i] = 0
		else:
			print("\nThe matrix just glitched?\n")
			exit(1)

		#print(self.cells)

	def rule_id(self, triple):
		L, C, R = triple
		s = str(int(L)) + str(int(C)) + str(int(R))
		index = int(s, 2) # parse a binary number not decimal

		return index

	def run_automaton(self):
		ruleset = self.ruleset

		history = np.zeros((self.generations, self.length)) # 2D array
		#print(history.shape)
		history[0, :] = self.cells # start here

		for gen in range(1, self.generations):
			all_triples = np.stack(
				[
				np.roll(history[gen - 1, :], 1),
				history[gen - 1, :],
				np.roll(history[gen - 1, :], -1)
				]
				)
			#print(np.apply_along_axis(self.rule_id, 0, all_triples))

			temp = []
			for i in np.apply_along_axis(self.rule_id, 0, all_triples):
				temp.append(ruleset[i])

			temp = np.array(temp, dtype=np.int64)

			history[gen, :] = temp

		return history, None, None	


def run_trials(n = 100):

	actual, predicted, time = [], [], []

	for trial in range(n):
		density = np.random.uniform(0,1)
		if density > 0.5:
			majority = 1
		elif density < 0.5:
			majority = 0
		else: 
			majority = None
		actual.append(majority)

		instance = GKL_CA()
		instance.trials_set_up(density)
		instance.init_cells()

		data, density_, steps = instance.run_automaton()
		predicted.append(int(density_))
		time.append(steps)

	return actual, predicted, time
	

def plot_sim(data):
	import matplotlib.pyplot as plt 
	plt.rcParams['image.cmap'] = 'binary'

	fig, ax = plt.subplots(figsize=(16, 9))
	ax.matshow(data)
	ax.axis(False)

	plt.show()

def main():

	CA = None
	mode = input("\nWelcome to CASa Blanka - Everything is black and white but that's only the beginning.\
		\nTo explore Elementary CAs, enter 'E'.\
		\nTo explore the GKL CA, enter 'GKL' \
		\nEnter: ")
	
	if mode == "E":
		print("\nYou have chosen to explore elementary cellular automata.\n")
		CA = E_CA()	

	if mode == "GKL":
		choice = input("\nYou have chosen to explore the Gacs-Kurdyumov-Levin Density Classifier.\nDo you want to run trials or simply run the classifier? \nEnter 'trial' for trials or 'run' otherwise: \n")

		if choice == "run":
			CA = GKL_CA()

		elif choice == "trial":
			num_trials = int(input("\nEnter the number of trials you want to run: "))
			print("\nRunning trials...\n")
			actual, predicted, time = run_trials(num_trials)

			# print(actual)
			# print(predicted)
			res = np.array(actual) - np.array(predicted)
			# print(res)
			success_rate = 100 * (len(res) - np.count_nonzero(res))/len(res)

			print(f"The success rate for this set of trials is {success_rate}%.\n")

			exit(1)


	CA.set_properties()
	CA.init_cells()
	data, density, steps = CA.run_automaton()
	
	if density != None:
		print(f"The majority element is {int(density)} and the automaton converged in {steps} steps.\n")

	plot_sim(data)


main()	