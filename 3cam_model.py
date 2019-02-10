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
from model import predict
 
p = psutil.Process(os.getpid())
p.nice(19)  # set>>> p.nice()10

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
   
cam = cv2.VideoCapture(0)    


path = '/home/felipe/final'

wait = 0
WAIT_TURNS = 60
sequence = 0
THRESHOLD = 0

BRIGHTNESS_THRESHOLD = 50
BRIGHTNESS_THRESHOLD2 = 200
BLACK_PIXELS_PERCENTAGE = 0.50
WHITE_PIXELS_PERCENTAGE = 0.50

SCORE_THRESHOLD = 0.95 # > 
SOUND_THRESHOLD = 0.95
time_init = time()
time_end = 0

pic_enabled = True

old_sound = 0

command_delay = 0

command = "Init"

while True:

    score = 0
            
    now = datetime.now()         
    time_taken = time() 
    
    current_sound = bark()
    
    dif = current_sound - old_sound
    
    if dif >= 0:
    
        sound = dif
        
    else:
    
        sound = 0    
     
    print("Sound:", '{:04f}'.format(sound))
    
    
    s, img = cam.read()
    
    cv2.imshow("Cam", cv2.resize(img, (320, 240)))
    cv2.waitKey(1)             
    
    time_id = '{:02d}'.format(now.day)+"-"+'{:02d}'.format(now.month)+"-"+str(now.year)+"-"+'{:02d}'.format(now.hour)+":"+'{:02d}'.format(now.minute)+":"+'{:02d}'.format(now.second)
    
    if sound > SOUND_THRESHOLD:
      
        score = predict(img)    
    
        print("W:", wait, "S:", sequence, "Score:", '{:04f}'.format(score), "Sound:", '{:04f}'.format(sound), "Time:", time_id)
     
                  
        if now.hour < 20 and now.hour > 6:
          
            if score > SCORE_THRESHOLD and wait == 0 and sequence < THRESHOLD:
            
                sequence += 1
                    
            elif score > SCORE_THRESHOLD and wait == 0 and sequence == THRESHOLD:
                
                f = open("report.txt", 'a')
    
                f.write(str(time_id) + " " + '{:04f}'.format(score) + " " + '{:04f}'.format(sound) + "\n")
    
                f.close()
                cv2.imwrite(path+"/auto_tweet.png",img)

                wait = WAIT_TURNS
                sequence = 0
                
                try:
                
                    print("Postando foto")
                    
                    if pic_enabled:
                    
                        post_picture(path+"/auto_tweet.png")
                
                except:
                
                    print("Corrigir")
                           
            else:
            
                sequence = 0
            
                if wait > 0:
                
                    wait -= 1               

    command_delay = (command_delay + 1) % 10
    
    if command_delay == 0:
                
        try:
            command = get_url()          
            if command == "reboot" or command == "Reboot":
                os.system("reboot")        
            elif command == "shutdown" or command == "Shutdown":
                os.system("shutdown now")
            elif command == "enable" or command == "Enable":
                pic_enabled = True            
            elif command == "disable" or command == "Disable":
                pic_enabled = False            
        except:    
            pass
     
    time_end = time()  
        
    print('{:04f}'.format(time_end - time_taken), "Segundos ", "Comando:", command, "-", command_delay, "Time:", time_id) 
    
    f = open("last_run.txt","w")
    f.write(time_id+"\n")
    f.close()
    
    old_sound = sound
