#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 14:53:07 2017

@author: bingfei
"""

import cv2
import numpy as np
import csv

color=[(0,255,0),(255,0,0),(0,0,255)]

img_path='/Users/bingfei/project/Trajectory/Exca Traj/map.jpg' #input map
img=cv2.imread(img_path)
w=img.shape[1]
h=img.shape[0]

st=[16,45,58]
fps=5

#Calculate image2map matrix
image=np.float32([[384,368],[842,354],[354,542],[920,508]]) #input 4 points on the image
realp=np.float32([[1425,797],[1704,719],[1509,880],[1710,823]]) #input corresponding 4 points on the map
p=cv2.getPerspectiveTransform(np.array([image]), np.array([realp]))

#lat, lon to 2D
def gps2map(longitude,latitude):
    x = w * (longitude + 180) / (2 * 180)
    y = h * (latitude + 180) / (2 * 180)
    return [x,y]

def map2gps(p):
    longitude=p[0]*(2*180)/w-180
    latitude=p[1]*(2*180)/h-180
    return [longitude, latitude]

def Time(starttime, fps):
    second=(starttime[2]+(i)/fps)%60
    minute=(starttime[1]+(starttime[2]+(i)/fps)/60)%60
    hour=(starttime[0]+(starttime[1]+(starttime[2]+(i)/fps)/60)/60)%24
    time= str(hour)+':'+str(minute)+':'+str(second)
    return time

'''#Calculate map2GPS matrix
gps=np.float32([gps2map(22.481212,114.152343),gps2map(22.481234,114.152125),gps2map(22.481324,114.15213)]) #input gps points
reala=np.float32([[200,190],[262,186],[254,218]])
a=cv2.getAffineTransform(np.array([reala]), np.array([gps]))'''

boundingbox=[]
for k in range(2):
    csvFile = open("/Users/bingfei/project/Trajectory/Exca Traj/annotations"+str(k)+".csv", "r") #input tracking results (coordinates of the object)
    reader = csv.reader(csvFile)
    bbx=[]
    for item in reader:
        for item in reader:
            item=map(int, item)
            bbx.append(item)
    boundingbox.append(bbx)
    
    '''with open('/Users/bingfei/project/Trajectory/Hong Kong/gps'+str(k)+'.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(['centroid_x','centroid_y','Latitude','Longitude','time'])'''

for i in range(1):
    img=cv2.imread(img_path)
    for j in range(2):
        
        coordinate=boundingbox[j][i]
        object_image_pt_x=coordinate[0]+0.5*coordinate[2]
        object_image_pt_y=coordinate[1]+0.5*coordinate[3]    
        centroid=[object_image_pt_x,object_image_pt_y]

        centroid.append(1)

        real_coordinate=np.dot(p,centroid)
        object_real_pt_x=np.int(real_coordinate[0]/real_coordinate[2])
        object_real_pt_y=np.int(real_coordinate[1]/real_coordinate[2])
        
        cv2.circle(img,(object_real_pt_x-150,object_real_pt_y-75),7, color[j],-1)
    
        #gps_coordinate=map2gps(np.dot(a,[object_real_pt_x,object_real_pt_y,1]))
        time= Time(st,fps)
    
        '''with open('/Users/bingfei/project/Trajectory/Hong Kong/gps'+str(j)+'.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                writer.writerow([centroid[0],centroid[1], gps_coordinate[0],gps_coordinate[1],time])'''
    cv2.imwrite('/Users/bingfei/project/Trajectory/Exca Traj/Trajectory/'+str(i)+'.jpg',img)
    print(i)
    
for i in range(1,1491):
    img=cv2.imread('/Users/bingfei/project/Trajectory/Exca Traj/Trajectory/'+str(i-1)+'.jpg')
    for j in range(2):
        
        coordinate=boundingbox[j][i]
        object_image_pt_x=coordinate[0]+0.5*coordinate[2]
        object_image_pt_y=coordinate[1]+0.5*coordinate[3]    
        centroid=[object_image_pt_x,object_image_pt_y]

        centroid.append(1)

        real_coordinate=np.dot(p,centroid)
        object_real_pt_x=np.int(real_coordinate[0]/real_coordinate[2])
        object_real_pt_y=np.int(real_coordinate[1]/real_coordinate[2])
        
        cv2.circle(img,(object_real_pt_x-150,object_real_pt_y-75),7, color[j],-1)
    
        #gps_coordinate=map2gps(np.dot(a,[object_real_pt_x,object_real_pt_y,1]))
        time= Time(st,fps)
    
        '''with open('/Users/bingfei/project/Trajectory/Hong Kong/gps'+str(j)+'.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                writer.writerow([centroid[0],centroid[1], gps_coordinate[0],gps_coordinate[1],time])'''
    cv2.imwrite('/Users/bingfei/project/Trajectory/Exca Traj/Trajectory/'+str(i)+'.jpg',img)
    print(i)
 
    
'''for i in range(8998):
    
    for l in range(3):
        csvFile = open("/Users/bingfei/project/Trajectory/Hong Kong/annotations"+str(l)+".csv", "r")
        reader = csv.reader(csvFile)
        bbx=[]
        for item in reader:            
            item=map(int, item)
            bbx.append(item)
            
        coordinate=bbx[i]
        object_image_pt_x=coordinate[0]+0.5*coordinate[2]
        object_image_pt_y=coordinate[1]+0.5*coordinate[3] 
        centroid=[object_image_pt_x,object_image_pt_y]

        centroid.append(1)

        real_coordinate=np.dot(p,centroid)
        object_real_pt_x=np.int(real_coordinate[0]/real_coordinate[2])
        object_real_pt_y=np.int(real_coordinate[1]/real_coordinate[2])
        
        cv2.circle(img, (object_real_pt_x,object_real_pt_y),5, color[l],-1)
        
        gps_coordinate=map2gps(np.dot(a,[object_real_pt_x,object_real_pt_y,1]))
        
        second=(st[2]+(i)/fps)%60
        minute=(st[1]+(st[2]+(i)/fps)/60)%60
        hour=(st[0]+(st[1]+(st[2]+(i)/fps)/60)/60)%24
        time= Time(st,fps)
        
        with open('/Users/bingfei/project/Trajectory/Exca Traj/gps'+str(l)+'.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                writer.writerow([centroid[0],centroid[1], gps_coordinate[0],gps_coordinate[1],time])
                
    cv2.imwrite('/Users/bingfei/project/Trajectory/Hong Kong/results/'+str(i)+'.jpg',img)'''