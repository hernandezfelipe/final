import cv2
import os
import numpy as np
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers import Activation, Dense, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
from keras.datasets import mnist
from keras.optimizers import Adam
from keras.layers.normalization import BatchNormalization
from keras.utils import np_utils
from random import sample
from keras.models import model_from_json
import psutil
import easygui
from tweet import post_picture
from time import sleep, time
from datetime import datetime
from audio import bark
from url import get_url

div = 4
HEIGHT = 480 // div
WIDTH = 640  // div

path = '/home/felipe/final'

json_file = open(path+'/model_mic.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(path+'/model_mic.h5')
print("Loaded model from disk")

# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

def predict(res):

    res = cv2.resize(res, (HEIGHT,WIDTH))        
    X_train = np.array(res)       
    X_train = X_train.reshape(1, HEIGHT, WIDTH, 3)
    X_train = X_train.astype('float32')
    X_train/=255

    score = loaded_model.predict(X_train)[0][0]

    return score

