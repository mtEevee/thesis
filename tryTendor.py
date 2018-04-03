#from Pillow import Image
#Pillow.Image.open('file')

from keras.models import Sequential
from keras.layers import Dense
from keras.utils.vis_utils import plot_model
import numpy as np
import pandas as pd
import os
import imread

import tensorboard
import tensorflow as tf

data_dir = "/Users/roman/Downloads/train_DETg9GD"
train = pd.read_csv(os.path.join(data_dir, 'train.csv'))

temp = []
for img_name in train.ID:
    img_path = os.path.join(data_dir, 'Train', img_name)
    img = imread(img_path)
    img = imresize(img, (32, 32))
    temp.append(img.astype('float32'))


train_x = np.stack(temp)

# define vars
input_num_units = 32 * 32 * 3 # image is 3D (RGB) that is why multiply by 3
hidden_num_units = 500
output_num_units = 3

epochs = 50
batch_size = 128

model = Sequential([InputLayer(input_shape=(input_num_units,)),

    Dense(units=hidden_num_units, activation='relu'),

    Dense(units=output_num_units, activation='softmax'), ])

model.fit(train_x, train_y, batch_size=batch_size,epochs=epochs,verbose=1, validation_split=0.2,
          callbacks=[keras.callbacks.TensorBoard(log_dir="logs/final/{}".format(time()), histogram_freq=1,
                                                 write_graph=True, write_images=True)])
