import numpy as np
import h5py
import hdf5
f = h5py.File('E:\Wavelet_analysis\electrodeNames.mat','r')
data = f.get('data/electrodeNames')
data = np.array(data)