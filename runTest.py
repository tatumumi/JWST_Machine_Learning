#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 12:08:07 2022

@author: joshuaumiamaka
"""

#the code below was taken from https://spacetelescope.github.io/
#hellouniverse/notebooks/hello-universe/Classifying_JWST-HST_galax
#y_mergers_with_CNNs/Classifying_JWST-HST_galaxy_mergers_with_CNN
#s.html

# arrays
import numpy as np

# fits
from astropy.io import fits
from astropy.utils.data import download_file
from astropy.visualization import simple_norm

# plotting
from matplotlib import pyplot as plt
import pickle

# keras
from keras.models import Model
from keras.layers import Input, Flatten, Dense, Activation, Dropout, BatchNormalization
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.regularizers import l2
from keras.callbacks import EarlyStopping

# sklearn (for machine learning)
from sklearn.model_selection import train_test_split
from sklearn import metrics

# from IPython import get_ipython
# get_ipython().run_line_magic('matplotlib', 'notebook')

version = 'pristine'

pickle_file = 'all_images.pickle'
hdu = pickle.load(open(pickle_file,'rb'))

#CPU times: user 2.86 s, sys: 4.32 s, total: 7.18 s
#Wall time: 20.6 s


#dividing into training and validation sets
X = hdu[0]
y = hdu[1]

random_state = 42

X = np.asarray(X).astype('float32')
y = np.asarray(y).astype('float32')

print(X.shape)
X = X[:,0:4] #added 4 instead of 3 (4 filters)
print(X.shape)
print(y.shape)

# First split off 30% of the data for validation+testing
X_train, X_split, y_train, y_split = train_test_split(X, y, test_size=0.3, random_state=random_state, shuffle=True)

# Then divide this subset into training and testing sets
X_valid, X_test, y_valid, y_test = train_test_split(X_split, y_split, test_size=0.666, random_state=random_state, shuffle=True)

imsize = np.shape(X_train)[2]
print("printing imsize: ", imsize)
print("X train shape: ", X_train.shape)

#X_train = X_train.reshape(len(X_train), imsize, imsize, 3)
#X_valid = X_valid.reshape(len(X_valid), imsize, imsize, 3)
#X_test = X_test.reshape(len(X_test), imsize, imsize, 3)

X_train = np.transpose(X_train,[0,2,3,1])
X_valid = np.transpose(X_valid,[0,2,3,1])
X_test = np.transpose(X_test,[0,2,3,1])

print("X train shape: ", X_train.shape)

#building an CNN in keras 
data_shape = np.shape(X)
input_shape = (imsize, imsize, 3) 

x_in = Input(shape=input_shape)
c0 = Convolution2D(8, (5, 5), activation='relu', strides=(1, 1), padding='same')(x_in)
b0 = BatchNormalization()(c0)
d0 = MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid')(b0)
e0 = Dropout(0.5)(d0)

c1 = Convolution2D(16, (3, 3), activation='relu', strides=(1, 1), padding='same')(e0)
b1 = BatchNormalization()(c1)
d1 = MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid')(b1)
e1 = Dropout(0.5)(d1)

c2 = Convolution2D(32, (3, 3), activation='relu', strides=(1, 1), padding='same')(e1)
b2 = BatchNormalization()(c2)
d2 = MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid')(b2)
e2 = Dropout(0.5)(d2)

f = Flatten()(e2)
z0 = Dense(64, activation='softmax', kernel_regularizer=l2(0.0001))(f)
z1 = Dense(32, activation='softmax', kernel_regularizer=l2(0.0001))(z0)
y_out = Dense(1, activation='sigmoid')(z1)

cnn = Model(inputs=x_in, outputs=y_out)


optimizer = 'adam'
fit_metrics = ['accuracy']
loss = 'binary_crossentropy'
cnn.compile(loss=loss, optimizer=optimizer, metrics=fit_metrics)
cnn.summary()


nb_epoch = 20
batch_size = 128
shuffle = True

# Train
history = cnn.fit(X_train, y_train, 
                  batch_size=batch_size, 
                  epochs=nb_epoch, 
                  validation_data=(X_valid, y_valid),
                  shuffle=shuffle,
                  verbose=False)

loss = history.history['loss']
val_loss = history.history['val_loss']
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

epochs = list(range(len(loss)))

figsize = (6, 4)
fig, axis1 = plt.subplots(figsize=figsize)
plot1_lacc = axis1.plot(epochs, acc, 'navy', label='accuracy')
plot1_val_lacc = axis1.plot(epochs, val_acc, 'deepskyblue', label="validation accuracy")

plot1_loss = axis1.plot(epochs, loss, 'red', label='loss')
plot1_val_loss = axis1.plot(epochs, val_loss, 'lightsalmon', label="validation loss")


plots = plot1_loss + plot1_val_loss
labs = [plot.get_label() for plot in plots]
axis1.set_xlabel('Epoch')
axis1.set_ylabel('Loss/Accuracy')
plt.title("Loss/Accuracy History (Pristine Images)")
plt.tight_layout()
axis1.legend(loc='lower right')

plt.savefig("history.pdf")
plt.close()


valid_predictX_valid = cnn.predict(X_valid)
train_predictX_train = cnn.predict(X_train)


pickle.dump((loss, val_loss, acc, val_acc, X_train, y_train, X_valid, y_valid, valid_predictX_valid, train_predictX_train),open("pre_images.pickle", 'wb'))
