import cv2 
import os 
import numpy as np 
from random import shuffle
from tqdm import tqdm
import matplotlib.pyplot as plt 
import tflearn 
from tflearn.layers.conv import conv_2d, max_pool_2d 
from tflearn.layers.core import input_data, dropout, fully_connected 
from tflearn.layers.estimator import regression 
import tensorflow as tf
from numpy import expand_dims
from PIL import Image


IMG_SIZE=50
LR = 1e-3

tf.reset_default_graph() 
convnet = input_data(shape =[None, IMG_SIZE, IMG_SIZE, 1], name ='input') 

convnet = conv_2d(convnet, 32, 5, activation ='relu') 
convnet = max_pool_2d(convnet, 5) 

convnet = conv_2d(convnet, 64, 5, activation ='relu') 
convnet = max_pool_2d(convnet, 5) 

convnet = conv_2d(convnet, 128, 5, activation ='relu') 
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 64, 5, activation ='relu') 
convnet = max_pool_2d(convnet, 5) 

convnet = conv_2d(convnet, 32, 5, activation ='relu') 
convnet = max_pool_2d(convnet, 5) 

convnet = fully_connected(convnet, 1024, activation ='relu') 
convnet = dropout(convnet, 0.8) 

convnet = fully_connected(convnet, 5, activation ='softmax') 
convnet = regression(convnet, optimizer ='adam', learning_rate = LR, loss ='categorical_crossentropy', name ='targets') 

model = tflearn.DNN(convnet) 


model.load("Garbage_Segregator-0.001-6conv-basic.model")
video = cv2.VideoCapture(0)

while True:
    _, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(gray, (IMG_SIZE, IMG_SIZE)) 
               
    img = np.expand_dims(img, axis=0)
        
    img=img.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    nlist=['metal', 'paper', 'cardboard', 'glass', 'plastic']
    cv2.imshow('VideoFeed',frame)
    prediction = (model.predict(img))
    res=nlist[prediction[0].tolist().index(max(prediction[0]))]
    print(prediction)
    if prediction[0][0]>0.80:
        print("Metal");
    elif prediction[0][1]>0.80:
        print("Paper");
    elif prediction[0][2]>0.80:
        print("Cardboard");
    elif prediction[0][3]>0.80:
        print("Glass");
    elif prediction[0][4]>0.80:
        print("Plastic");
    else:
        print(res);
    cv2.imshow("Capturing", frame)
    key=cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
