import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import scipy.stats as ss

# L: length of matrix
# W: width
# p: void probability

class RWMatrix:
	def __init__(self,L,W,p):
		self.L=L
		self.W=W
		self.p=p

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
			while flag == 0 and 0<x<L-1 and count<301: #take maximum 200 steps
				count += 1
				nextdir = np.random.choice([0,1,2,3])
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

		self.xarray=xarray
		self.yarray=yarray

	def plotXarrayHist(self,filename):
		plt.hist(self.xarray,bins=50, normed=True)
		plt.xlim((0, self.L))
		#plt.savefig(filename)


	def plotGFit(self): #produce a gaussian fit
		mean = np.mean(self.xarray)
		variance = np.var(self.xarray)
		sigma = np.sqrt(variance)
		x = np.linspace(min(self.xarray), max(self.xarray),100)
		plt.plot(x,mlab.normpdf(x,mean,sigma))
		plt.show()

	def plotGTheo():
		pass		
		#theoretical curve????
		# a = np.linspace(ss.norm.ppf(0.01),ss.norm.ppf(0.99), 100)
		# b = a + 75
		# plt.plot(b, mlab.normpdf(b,75,1),'r-')


for p in np.arange(0.5,1.1,0.1):
	a = RWMatrix(151,50,0.8)
	print np.var(a.xarray)

