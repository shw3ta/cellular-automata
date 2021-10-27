import random

f = open('initialization_vectors_289.txt', 'w')

for _ in range(1000):
	
	i = random.uniform(0.45, 0.55)  # generate a random density close to 0.5
	majority = 1 if i>0.5 else 0  # find majority element

	n = 289  # number of cells
	freq = (int)(i*n)
	arr = [1]*freq
	arr2 = [0]*(n-freq)
	arr += arr2

	vectors = []

	for _ in range(1000):
	  random.shuffle(arr)
	  f.write(str(arr) + ', ' + str(i) + ', '+ str(majority) + '\n')

print('Done')