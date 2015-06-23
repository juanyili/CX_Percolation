import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

L = 101 #length of matrix
W = 50 #width
p = 1.0 #void probability

mat = np.random.choice([0, 1], size=(L,W), p=[1-p,p])
success = 0. #keep track of successful trials
countarray=[]
xarray=[]
yarray=[]
posarray=[]
for i in range(1000):
	# choose a random cell in the center that has value 1
	val = 0
	while val == 0:
		x,y = L/2, np.random.randint(0,W)
		val = mat[x,y]
	flag = 0 # while it does not reach the bottom or the top
	count = 0
	while flag == 0 and 0<x<L-1 and count<501: #take maximum 500 steps
		count += 1
		nextdir = np.random.randint(0,4)
		if nextdir == 0: #up
			x += (-1)
		if nextdir == 1: #down
			x += 1
		if nextdir == 2: #left
			y += -1
		if nextdir == 3: #right
			y += 1
		y = y%W #left and right is perodic
		if x == 0 or x == L-1:
			flag = 1 #terminates the run
			if mat[x,y] == 1:
				success+=1
	countarray.append(count)
	xarray.append(x)
	yarray.append(y)
	posarray.append([x,y])
print success

plt.hist(xarray,bins=50, normed=True)
plt.xlim((min(xarray), max(xarray)))
#produce a gaussian fit
mean = np.mean(xarray)
variance = np.var(xarray)
sigma = np.sqrt(variance)
x = np.linspace(min(xarray), max(xarray),100)
plt.plot(x,mlab.normpdf(x,mean,sigma))

plt.show()


