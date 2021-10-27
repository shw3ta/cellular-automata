import streamlit as st
import pandas as pd 
import numpy as np 
from PIL import Image
import base64
import random
import math 
import os 

def app():
	class E_CA:

		def __init__(self, length, IV, ruleset, gens):
			self.ruleset = ruleset
			self.length = length
			self.cells = IV
			self.generations = gens
			
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

	class GKL_CA:

		def __init__(self, length, IV, density):
			self.length = length
			self.cells = IV
			# self.limit_evolution = 0
			# density => density of 1s in the state array
			self.density = density


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


		def run_automaton(self, j = 1, k = 3):
			history = np.zeros((600, self.length)) # 2D array
			#print(history.shape)
			history[0, :] = self.cells # start here

			density = self.density #this will change with evolution
			
			ctr, step_ctr = 1, 0		 
			while (ctr < 600):
				# not converged yet
				all_quintuples = np.stack(
					[np.roll(history[ctr-1, :], -k),
					 np.roll(history[ctr-1, :], -j),
					 history[ctr-1, :],
					 np.roll(history[ctr-1, :], j),
					 np.roll(history[ctr-1, :], k)
					]
					)
				arr = []
				for i in np.apply_along_axis(self.apply_rule, 0, all_quintuples):
					arr.append(i)

				history[ctr, :] = np.array(arr, dtype=np.int64)


				#calculate the new density
				density = np.count_nonzero(history[ctr, :] == 1)/self.length
				ctr += 1	

				if (density != 1 and density != 0): step_ctr += 1		

			return history, density, step_ctr			


	def plot_sim(data):
		import matplotlib.pyplot as plt 
		plt.rcParams['image.cmap'] = 'binary'

		fig, ax = plt.subplots(figsize=(16, 9))
		ax.matshow(data)
		ax.axis(False)

		st.pyplot(fig)


	st.title("The Majority Problem / Density Classification")

	st.write("""

		Many physical systems can be thought of as being made up of individual components with similar properties interacting amongst themselves 
		and its environment, based on some simple rules. Without much extrapolation, it is easy to see how cellular automata will serve as 
		a great way to simulate and possibly even understand the underlying rules that define such physical systems.
		""")

	im_path = os.path.join(os.path.dirname(__file__), 'images/examples.png')
	img = Image.open(im_path)
	st.image(img, caption="some systems that are modelled using cellular automata")

	st.write("""

		Below, we present to you a problem faced by distributed systems with agents that interact locally or in a limited manner. Given that each cell 
		in an automaton can have one of finitely many states, is there an automaton that can converge to the the state that is in majority in the IV?
		The problem seems trivial at first: why not use a counter? It's an array after all; Until you realize that CA here can be used to represent physical 
		systems, which often, are only locally connected, and have no direct way of communicating their state to distant cells. Nor is the computation trivial as 
		such systems do not have external counters to help them decide which element is in majority.


		""")

	st.markdown("---")

	st.write("""
		## Problem Statement and the GKL Classifier
		
		Is there an automaton [rule] that can accurately perform majority voting (or density classification) by converging to a 
		homogeneous state where the state array consists only of the majority element, in all cases? 

		One of the oldest approaches to solving this is a non-elementary $1$-D automaton, called the GKL classifier. 
		The GKL rule presented in $1987$ by Gacs, Kurdyumov and Levin, achieved an accuracy of $97.8 \%$ using a $2$-state model and $r=3$ neighbourhood. This classifier converges to the correct state
		in almost all cases, except around a density of $0.5$. Let's take a look at what the rule is and why it doesn't work at and around $0.5$.
		""") 

	im_path = os.path.join(os.path.dirname(__file__), 'images/gkl_desc.png')
	img = Image.open(im_path)
	st.image(img, caption="gkl rule")

	st.write("""
		Above, the cell demarcated in red corresponds to the current cell in a given state array. The rule shown on the left is applied to every cell
		in the state array with the neighbourhood as indicated by the arrows. Notice that the second cell to the left and right of the current position 
		are not part of the neighbourhood. 

		The problem with this rule is that it must converge, therefore the state array constitution changes at every step. In other words, at every time step, the density of the symbols changes in favor of the
		majority symbol. This results in a problem when the IV has equal amounts of each symbol, or ratios very close to each other. At density $0.5$ for a $2$ symbol CA, this classifier will favor either symbol with 
		uniform probability at time step $1$, and once a majority starts existing as a result of this, the classifier moves in the direction that converges to this new majority symbol. The problem remains the same when 
		the densities are not significantly different from each other. 

		""")

	st.write("""

		Later, Land and Belew, in their $1995$ paper showed that there exists no perfect $2$-state cellular automaton for the density classification problem. However, it has been shown that a slight modification to
		the neighbourhood gives better performance as compared to the vanilla GKL rule. For example, instead of taking the first and third neighbours, taking the first and fifth, third and sixth, second and seventh and so on
		show different performaces, and J.R.G Mendonca's $2019$ paper shows that the best classification is achieved when the neighbourhood has indices related as $j$ and $3j$. No one knows why this might be the case, but our
		own explorations only confirmed this. You can specify the neighbourhood for a given fixed IV and see the differences for yourself.
		""")
	st.markdown("""---""")

	IV_fixed = np.array([1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0])
	st.write(f"The fixed IV is: {IV_fixed} and has a length of {len(IV_fixed)}, where 1 is the majority element with a density $0.5088127064374639$, which is very close to $0.5$.")
	i = st.number_input("Enter position of first neighbour on the left/right (j): ", 1)
	j = st.number_input("Enter position of second neighbour on the left/right (k): ", 3)
	if st.button('Run!'):
		GKL_modif = GKL_CA(len(IV_fixed), IV_fixed, 0.5088127064374639)
		data, mjrt, ctr = GKL_modif.run_automaton(j=int(i), k=int(j))
		plot_sim(data)
		if ctr < 599:
			st.write(f"The predicted majority element is ${int(mjrt)}$ and the classifier converges in ${ctr}$ steps.\n The true majority element is ${1}$")
		else:
			st.write("The classifier did not converge.")





	st.write("""

		Above, we ran the automaton for 600 generations in every case to give it enough time to converge. When you play around with the vanilla GKL classifier below, you'll notice that classification is sound when the density is not this close to $0.5$.

		Where do we go from here? **drumroll** Let's tweak the problem statement!

		## Modified Problem Statement
		
		Capcarrere et al use a modified approach to the density classification problem to find one such perfect cellular automaton classifier. 
		The output configuration in the original problem has to be a homogeneous state array consisting only of the majority element. Instead of finding
		a more efficient rule to achieve this, they decided to change the way the final classification is represented. It is observed 
		that the $2$-state, $r=1$ rule $184$ CA, upon presentation of an arbitrary initial configuration, relaxes the grid to the limit cycle within 
		$N/2$ (upper limit) time steps where $N$ is the number of cells. The density classification can be observed as follows: If the density of 
		$1$s $> 0.5$ $(< 0.5)$, then the final configuration consists of one or more blocks of at least two consecutive $1$s ($0$s), interspersed by an 
		alternation of $0$s and $1$s. For an initial density of $0.5$, the final configuration is simply an alternation of $0$s and $1$s.

		""")

	st.markdown("""---""")

	st.write("""

		## See for yourself!

		You can explore how the GKL Classifier and Rule 184 work to conclude whether the majority element in the initial configuration was
		$1$ or $0$. Use the slider to set the density of 1s in your initialisation vector. We will generate a random IV based on this density
		and run it through both the classifiers.

	 	""")

	density = st.slider("Enter the density of 1s in your IV:", 0.0, 1.0, step=0.0001)


	ruleset_str = "10111000"
	ruleset = [char for char in ruleset_str[: : -1]]


	length = st.number_input("Enter the length of your IV (between 300-500):", 300)
	if type(length) != int or length > 500 or length < 300: 
		st.write("""
			Invalid entry, enter an integer within range.
			""")


	majority = 1 if density > 0.5 else 0 if density < 0.5 else None # find majority element
	freq = (int)(density*length)
	arr = [1]*freq
	arr2 = [0]*(length-freq)
	arr += arr2
	IV = np.array(random.sample(arr, length))
		
	st.write("IV: ", np.array2string(IV))

	if st.button("Run both!"):
		st.write("Output of Rule 184:")
		CA_184 = E_CA(length, IV, ruleset, int(0.7*length))
		data_184, _, _ = CA_184.run_automaton()
		plot_sim(data_184)
		st.write(f"The majority element is {int(majority)} and the classifier predicted {int(majority)}.") #for now.


		st.write("Output of the GKL Classifier:")	
		CA_GKL = GKL_CA(length, IV, density)
		data_GKL, density_, ctr = CA_GKL.run_automaton(j=1, k = 3)
		plot_sim(data_GKL)
		st.write(f"The predicted majority element is {int(density_)} and the classifier converges in {ctr} steps.\n The true majority element is {int(majority)}")
	  

	st.write("""
		The Rule 184 elementary CA has a $100\%$ classification accuracy as a result of the following properties:
		""")
	im_path = os.path.join(os.path.dirname(__file__), 'images/density_class2.PNG')
	img = Image.open(im_path)
	st.image(img, caption="Rule 184 ")

	st.write("""
		However, this cannot be used as a model for physical systems, because it still requires an external entity to read the final state array configuration be it using
		regular expressions or counters. 
		""")
