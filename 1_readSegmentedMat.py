import numpy as np
import scipy.io as sio

inputPath = 'E:/Segmented/Stimulus_locked/Subtraction/Day_1/S3/'

#for e_files in pathlib.Path(inputPath).glob('.mat'):
file = sio.loadmat(inputPath + 'e_AF3.mat')
data = file['El']
nSegments = data.shape[1]
for i in range(0,nSegments):
    segments = data[:,i]

#print(data.head)
#data = f.get('data/variable1')
#data = np.array(data)