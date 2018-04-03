from keras.models import Sequential
from keras.layers import Dense
from keras.utils.vis_utils import plot_model
import tensorflow as tf
import tensorboard
import keras
import numpy
numpy.random.seed(7) #initialized the random number generator to ensure our results are reproducible

graph = tf.Graph()
with graph.as_default():
  variable = tf.Variable(42, name='foo')
  initialize = tf.global_variables_initializer()
  assign = variable.assign(13)
with tf.Session(graph=graph) as sess:
  sess.run(initialize)
  sess.run(assign)
logDir = 'D:/Lisa/forPython/logs'
file_writer = tf.summary.FileWriter(logDir, sess.graph)


# load pima indians dataset
dataset = numpy.loadtxt("D:/Lisa/THESIS/pima-indians-diabetes.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0:8] #X - input data, all rows and first 7 columns
Y = dataset[:,8] # Y - output data, all rows and last column, only 0 or 1 values

# create model
model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

#Compile and fit the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#model.fit(X, Y, epochs=150, batch_size=10)
model.fit(X, Y, batch_size=10,epochs=150,verbose=1, callbacks=[keras.callbacks.TensorBoard(log_dir=logDir, write_graph=True, write_images=True)])

# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

print(model.summary())

#plot model
#plot_model(model, to_file='D:/Lisa/THESIS/tryKeras.png', show_shapes=True, show_layer_names=True)











