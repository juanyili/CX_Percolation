from pylab import *
from scipy.ndimage import measurements
import matplotlib.pyplot as plt
import numpy as np

sucarray=[]
prob=[]
L=10
for p in np.arange(0.4,0.98,0.001):
	prob.append(p)
	a = False
	while a == False:
		mat=np.random.choice([0, 1], size=(L,L), p=[1-p,p])
		if np.sum(mat[0])>0:
			a = True

	#showing in two colors
	#pcolor(mat, cmap="binary")
	#show()

	success = 0 # keep track of number of successful paths
	for i in range(500):
		# choose a random cell in the top roll that is 1
		pos = 0
		while pos == 0:
			x,y = 0, np.random.randint(0,L)
			pos = mat[x,y]

		flag = 0 # while it does not reach the bottom
		# create an array of number of cells each run has gone through
		while flag == 0 and x<L-1:
			# choose a random number out of 3 to decide the position of the next step
			nextdir = np.random.randint(0,3)
			if nextdir == 0: #left
				y+=(-1)
			if nextdir == 1: #center
				x+=1
			if nextdir == 2: #right
				y+=1
			y = y%L
			# whenever runs into a cell of 0, then terminates the run
			if mat[x,y]==0:
				flag = 1
				#print x,y
			# if the path reaches to the bottom, the success increases 1
			if x == L-1:
				success += 1
	sucarray.append(success/500)

plot(prob,sucarray)

show()