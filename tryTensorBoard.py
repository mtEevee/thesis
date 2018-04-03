import os
import keras
import numpy as np
import pandas as pd
from PIL import Image
import Pillow


from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Convolution2D, Flatten, MaxPooling2D, Reshape, InputLayer


data_dir = "D:/Lisa/forPython/"
train = pd.read_csv(os.path.join(data_dir, 'train.csv'))
temp = []
for img_name in train.ID:
    img_path = os.path.join(data_dir, 'Train', img_name)
    img = PIL.Image.open(img_path)
    img = imresize(img, (32, 32))
    temp.append(img.astype('float32'))

train_x = np.stack(temp)

# define vars
input_num_units = 32 * 32 * 3 # image is 3D (RGB) that is why multiply by 3
hidden_num_units = 500
output_num_units = 3

epochs = 50
batch_size = 128

model = Sequential([
    InputLayer(input_shape=(input_num_units,)),

    Dense(units=hidden_num_units, activation='relu'),

    Dense(units=output_num_units, activation='softmax'),
])