import Percolation_model as pm
import matplotlib.pyplot as plt
import numpy as np
plt.ion()
plt.show()

for p in np.arange(0.4,1,0.02):
	a = pm.RWMatrix(501,50,p,0.25)
	v = np.var(a.xarray)
	print v
	plt.scatter(p, v)
	plt.draw()
