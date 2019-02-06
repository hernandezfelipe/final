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

           

HEIGHT = 480/4
WIDTH = 640/4
N_SPLICES = 4
px = HEIGHT
py = WIDTH

wait = 0
WAIT_TURNS = 60
sequence = 0
THRESHOLD = 1

BRIGHTNESS_THRESHOLD = 50
BRIGHTNESS_THRESHOLD2 = 205
BLACK_PIXELS_PERCENTAGE = 0.50
WHITE_PIXELS_PERCENTAGE = 0.50

PIC_TIMELAPSE = 600

SCORE_THRESHOLD = 1 # > 
time_init = time()
time_end = 0

subtract = cv2.imread(path+"/subtract.png")
blacks = np.where(subtract == [0,0,0])

while True:

    now = datetime.now()         
    time_taken = time()   
    s, img = cam.read()   
    
    pic_img = img.copy()
    
    img[blacks] = [255]
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    input_pic = []

    for j in range(N_SPLICES):
        for k in range(N_SPLICES):

            temp_img = img[j*px:j*px+px, k*py:k*py+py, :]        
            input_pic.append(temp_img)

    X_train = np.array(input_pic)       
    X_train = X_train.reshape(X_train.shape[0], HEIGHT, WIDTH, 3)
    X_train = X_train.astype('float32')
    X_train/=255

    score = loaded_model.predict(X_train)
    score2 = len(np.where(score > 0.9)[0])
    
#    cv2.imshow("Cam", img)
 #   cv2.waitKey(1)

    quantidade_pixels_pretos = np.where(gray < BRIGHTNESS_THRESHOLD)[0].shape[0]
    quantidade_pixels_brancos = np.where(gray > BRIGHTNESS_THRESHOLD2)[0].shape[0]
    pretos = quantidade_pixels_pretos / float(gray.shape[0] * gray.shape[1])
    brancos= quantidade_pixels_brancos/ float(gray.shape[0] * gray.shape[1])

    print(score)
    print("Wait: ", wait, "Seq: ", sequence, "Score: ", score2, "Prt: ", pretos, "Brc: ", brancos)
    
        
    if pretos < BLACK_PIXELS_PERCENTAGE	and now.hour < 21 and now.hour > 6:
    
        if (time_end - time_init) > PIC_TIMELAPSE:
            
            pic_id = str(now.month) + str(now.day) + str(now.hour) +  str(now.minute) + str(now.second)
            cv2.imwrite(path+"/data/data_sacada/sacada" + pic_id + ".png", pic_img)
            
            time_init = time()
    
        if score2 > SCORE_THRESHOLD and wait == 0 and sequence < THRESHOLD:
        
            sequence += 1
                
        elif score2 > SCORE_THRESHOLD and wait == 0 and sequence == THRESHOLD:
            
            pic_id = str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second)

            cv2.imwrite(path+"/auto_tweet.png",pic_img)
            cv2.imwrite(path+"/data/data_tiao/tiao"+str(pic_id)+".png", pic_img)

            wait = WAIT_TURNS
            sequence = 0
            
            try:
            
                print("Postando foto")
                post_picture(path+"/auto_tweet.png")
            
            except:
            
                print("Corrigir")
        
        
        elif score2 > SCORE_THRESHOLD:
        
            pic_id = str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second)
            cv2.imwrite(path+"/data/data_tiao/tiao"+str(pic_id)+".png", pic_img)
            
            sequence = 0
        
            if wait > 0:
            
                wait -= 1
                
        else:
        
            sequence = 0
        
            if wait > 0:
            
                wait -= 1               
                
    else:
    
        print("Muito escuro", pretos)
        sequence = 0
        wait = 0
        
    
    time_end = time()  
    print(time() - time_taken, "Sec de processamento")  
    f = open("report.txt", 'w')
    f.write(str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"-"+str(now.hour)+":"+str(now.minute)+":"+str(now.second))
    f.close()
