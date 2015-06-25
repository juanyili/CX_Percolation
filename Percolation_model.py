import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import scipy.stats as ss

class RWMatrix:

	def __init__(self,L,W,p,q):
		self.L=L # length of matrix
		self.W=W # width
		self.p=p # void/available probability
		self.q=q # bias probability of heading downwards (0<=q<=0.25)
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
			while flag == 0 and 0<x<L-1 and count<L*2: #take maximum as twice many steps as the length
				count += 1
				dx,dy = 0,0
				nextdir = np.random.choice([0,1,2,3],p=[0.5-q,q,0.25,0.25])
				if nextdir == 0: #up
					dx = (-1)
				if nextdir == 1: #down
					dx = 1
				if nextdir == 2: #left
					dy = -1
				if nextdir == 3: #right
					dy = 1
				if mat[x+dx,(y+dy)%W] == 1: # if the next position is available
					x = x+dx # then update
					y = (y+dy)%W #left and right sides are connect; perodic
				if x == 0 or x == L-1: #when it hits the surface or the bottom
					flag = 1 #terminates the run
					if mat[x,y] == 1:
						success+=1
			countarray.append(count)
			xarray.append(x)
			yarray.append(y)
			posarray.append([x,y])

		self.xarray=xarray
		self.yarray=yarray

	def plotXarrayHist(self):
		plt.hist(self.xarray,bins=50, normed=True)
		plt.xlim((0, self.L))
		#plt.savefig(filename)


	def plotUGFit(self): #produce an UN-normed gaussian fit
		mean = np.mean(self.xarray)
		variance = np.var(self.xarray)
		sigma = np.sqrt(variance)
		x = np.linspace(min(self.xarray), max(self.xarray),100)
		gfit=mlab.normpdf(x,mean,sigma)*(len(self.xarray)*(max(self.xarray)-min(self.xarray))/50)
		plt.plot(x,gfit,label='p=%s'%self.p)
		plt.legend()


	def plotGFit(self): #produce a Normed gaussian fit
		mean = np.mean(self.xarray)
		variance = np.var(self.xarray)
		sigma = np.sqrt(variance)
		x = np.linspace(min(self.xarray), max(self.xarray),100)
		plt.plot(x,mlab.normpdf(x,mean,sigma),label='p=%s'%self.p)
		plt.legend()

	def plotGTheo(self): # produce a theoretical prediction of the gaussian curve	
		tmean = (2*self.q-0.5)*self.L*2 + self.L/2
		tvar = 4*self.q*(0.5-self.q)*self.L*2
		tsig = np.sqrt(tvar)
		x = np.linspace(0, self.L,100)
		plt.plot(x,mlab.normpdf(x,tmean,tsig),label='p=%s'%self.p, ls=':')


for p in np.arange(0, 1.1, 0.2):
	a = RWMatrix(201,50,p,0.25)
	a.plotXarrayHist()
	a.plotGFit()
	a.plotGTheo()
plt.show()