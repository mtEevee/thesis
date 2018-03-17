import numpy as np
import h5py
f = h5py.File('somefile.mat','r')
data = f.get('data/variable1')
data = np.array(data)
