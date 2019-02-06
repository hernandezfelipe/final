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

p = psutil.Process(os.getpid())
p.nice(19)  # set>>> p.nice()10

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

path = '/home/felipe/tiao2'

json_file = open(path+'/modelbr.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(path+'/modelbr.h5')
print("Loaded model from disk")
 
# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

   
cam = cv2.VideoCapture(0)    

div = 4
HEIGHT = 480 / div
WIDTH = 640  / div

wait = 0
WAIT_TURNS = 60
sequence = 0
THRESHOLD = 1

BRIGHTNESS_THRESHOLD = 50
BRIGHTNESS_THRESHOLD2 = 200
BLACK_PIXELS_PERCENTAGE = 0.50
WHITE_PIXELS_PERCENTAGE = 0.50

SCORE_THRESHOLD = 0.5 # > 
time_init = time()
time_end = 0

while True:

    now = datetime.now()         
    time_taken = time()   
    s, img = cam.read()   
        
    X_train = np.array(img)       
    X_train = X_train.reshape(X_train.shape[0], HEIGHT, WIDTH, 3)
    X_train = X_train.astype('float32')
    X_train/=255

    score = loaded_model.predict(X_train)
    
    cv2.imshow("Cam", img)
    cv2.waitKey(1)

    print(score)
    print("Wait: ", wait, "Seq: ", sequence, "Score: ", score)
    
    sound = bark()
        
    if now.hour < 20 and now.hour > 6:
      
        if score > SCORE_THRESHOLD and wait == 0 and sequence < THRESHOLD:
        
            sequence += 1
                
        elif score > SCORE_THRESHOLD and wait == 0 and sequence == THRESHOLD and sound > 0.9:
            
            pic_id = str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second)

            cv2.imwrite(path+"/auto_tweet.png",pic_img)

            wait = WAIT_TURNS
            sequence = 0
            
            try:
            
                print("Postando foto")
                #post_picture(path+"/auto_tweet.png")
            
            except:
            
                print("Corrigir")
                       
        else:
        
            sequence = 0
        
            if wait > 0:
            
                wait -= 1               

    
    time_end = time()  
    print(time() - time_taken, "Sec de processamento")  
    f = open("report.txt", 'w')
    f.write(str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"-"+str(now.hour)+":"+str(now.minute)+":"+str(now.second))
    f.close()
