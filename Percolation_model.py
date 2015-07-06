import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.ndimage import measurements
from pylab import *

class RWMatrix:

	def __init__(self,L,W,p):
		self.L=L # length of matrix; coordinates to x
		self.W=W # width; coordinates to y
		self.p=p # void/ava probability
		self.mat = np.random.choice([0, 1], size=(L,W), p=[1-p,p])

	def walk(self,m,q,N):
		#m walkers released
		#q bias probability of heading downwards (0<=q<=0.25)
		#N max steps a walker takes; when p>pc, it should be about 2*L
		#success = 0. #keep track of successful trials
		countarray=[]
		xarray=[]
		yarray=[]
		posarray=[]
		for i in range(m):
			# choose a random cell in the center that has value 1
			val = 0
			while val == 0:
				x,y = self.L/2, np.random.randint(0,self.W)
				val = self.mat[x,y]
			flag = 0 # while it does not reach the bottom or the top
			count = 0
			while flag == 0 and 0<x<self.L-1 and count<N: #take maximum as twice many steps as the length
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
				if self.mat[x+dx,(y+dy)%self.W] == 1: # if the next position is ava
					x = x+dx # then update
					y = (y+dy)%self.W #left and right sides are connect; perodic
				if x == 0 or x == self.L-1: #when it hits the surface or the bottom
					flag = 1 #terminates the run
					#if mat[x,y] == 1:
						#success+=1
			countarray.append(count)
			xarray.append(x)
			yarray.append(y)
			posarray.append([x,y])

		self.xarray=xarray
		self.yarray=yarray


#different plots
	def plotXarrayHist(self):
		plt.hist(self.xarray,bins=50, normed=True, label='p=%s'%self.p)
		plt.xlim((0, self.L))
		plt.legend()
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
		print 'At p = %s, mean is %s, variance is %s' %(self.p, mean, variance)

	def plotGTheo(self): # produce a theoretical prediction of the gaussian curve	
		tmean = (2*self.q*2-1)*self.L + self.L/2
		tvar = 4*self.q*2*(1-self.q*2)*self.L
		tsig = np.sqrt(tvar)
		x = np.linspace(0, self.L,100)
		plt.plot(x,mlab.normpdf(x,tmean,tsig),label='p=%s'%self.p, ls=':')
		plt.legend()

	def show(self):
		plt.show()

	def savefig(self,filename):
		plt.savefig(filename)


	# Label the matrix into clusters
	def labelCluster(self):
		def find(target):
			return target
		def union(label,left,above): #unite two clusters together
			small = min(left,above)
			big = max(left,above)
			temp = label.flatten()
			i = [small if i ==big else i for i in temp]
			label = np.reshape(i,[self.L,self.W])
			return label
		ll = 0
		label=np.zeros([self.L,self.W])
		for x in range(self.L):
			for y in range(self.W):
				if self.mat[x,y] == 1:
					left = label[x-1,y]
					above = label[x,y-1]
					if x == 0 and y == 0: #first cell upper right
						ll+=1
						label[x,y] = ll
					elif x == 0 and y != 0: #first column
						if self.mat[x,y-1]==0: #above empty
							ll+=1
							label[x,y] = ll #above not empty
						else: #above not empty
							label[x,y]=find(above)
					elif y == 0 and x!=0: #first row
						if self.mat[x-1,y] ==0: #left empty
							ll+=1
							label[x,y] = ll
						else: #left not empty
							label[x,y]=find(left)
					elif x!=0 and y!= 0:
						if self.mat[x-1,y] == 0 and self.mat[x,y-1] == 0:
							ll+=1
							label[x,y]=ll
						elif self.mat[x-1,y] != 0 and self.mat[x,y-1] == 0: #left not empty, above is
							label[x,y] = find(left)
						elif self.mat[x-1,y] == 0 and self.mat[x,y-1] != 0: #left empty, above is not
							label[x,y] = find(above)
						else: # when both neighbors are already labelled
							label = union(label,left,above) #change all left index to above index
							label[x,y] = min(left,above)
		def periodic(label):
			for x in range(self.L):
				left = label[x,0]
				right = label[x,self.W-1]
				if left!=0 and right!=0 and left!=right:
					small = min(label[x,0],label[x,self.W-1])
					big = max(label[x,0],label[x,self.W-1])
					temp = label.flatten()
					i = [small if i == big else i for i in temp]
					label = np.reshape(i,[self.L,self.W])
			return label
		def correctIndex(label):
			unique = np.unique(label[np.nonzero(label)]) #generate an array of only unique nonzero values
			temp=label.flatten()
			i = [np.nonzero(unique==i)[0][0]+1 if i !=0 else i for i in temp]
			label = np.reshape(i,[self.L,self.W])
			return label

		label = periodic(label)
		label = correctIndex(label)
		return label

	# Return an array of the cluster size distribution
	# EXAMPLE: print max(a.clusterDistribution(l)) #largest cluster size
	# EXAMPLE: plt.hist(a.clusterDistribution(l)) # histrogram of distribution
	def clusterDistribution(self,label):
		sizearray=[]
		for i in np.arange(1,label.max()+1):
			sizearray.append(np.count_nonzero(label==i))
		return sizearray

	# Return True if there is a spanning cluster
	def spanningCluster(self,label):
		span = set(label[0,:]) & set(label[self.W-1,:])
		span.remove(0.0)
		return len(span) != 0

# use scipy package; should be written into a method
# subplot(1,3,1)
# a=RWMatrix(50,30,0.55)
# imshow(a.mat, origin='lower', interpolation='nearest', cmap='binary')
# colorbar()
# title("Matrix")

# lw, num = measurements.label(a.mat)

# subplot(1,3,2)
# area = measurements.sum(a.mat, lw, index=arange(lw.max() + 1))
# areaImg = area[lw]
# im3 = imshow(areaImg, origin='lower', interpolation='nearest')
# colorbar()
# title("Clusters by area")

# # Bounding box
# sliced = measurements.find_objects(areaImg == areaImg.max())
# if(len(sliced) > 0):
#     sliceX = sliced[0][1]
#     sliceY = sliced[0][0]
#     plotxlim=im3.axes.get_xlim()
#     plotylim=im3.axes.get_ylim()
#     plot([sliceX.start, sliceX.start, sliceX.stop, sliceX.stop, sliceX.start], \
#                       [sliceY.start, sliceY.stop, sliceY.stop, sliceY.start, sliceY.start], \
#                       color="red")
#     xlim(plotxlim)
#     ylim(plotylim)

# subplot(1,3,3)
# hist(area, bins=15)
# title("histogram of cluster size distribution")

# show()