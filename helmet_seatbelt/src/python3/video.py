# -*- coding: utf-8 -*-
import sys

sys.path.append('/home/yzbx/git/gnu/darkflow')
from darkflow.net.build import TFNet
import cv2


if len(sys.argv) < 3:
    print('usage : python3 src/video.py in.mp4 out.mp4')
options = {"model": "/media/sdb/ISCAS_Dataset/helmet_seatbelt/config/tiny-yolo-helmet_seatbelt.cfg", "load": "/media/sdb/ISCAS_Dataset/helmet_seatbelt/tiny-yolo-helmet_seatbelt.weights", "threshold": 0.1}

tfnet = TFNet(options)

cap=cv2.VideoCapture(sys.argv[1])
if not cap.isOpened():
    print('cannot open video ',sys.argv[1])
    
frameNum=1

detectNum=0
color={}
color['person']=(255,0,0)
color['seatbelt']=(0,255,0)
color['helmet']=(0,0,255)



while True:
    ret,imgcv=cap.read()
    if not ret:
        print('video ends')
        break
    
    print('process frame ',frameNum)
    result=tfnet.return_predict(imgcv)
    h,w,c=imgcv.shape
    
    if frameNum==1 :
        video = cv2.VideoWriter('video.avi',-1,1,(w,h))
        
    for bbox in result:
        left=bbox['topleft']['x']
        top=bbox['topleft']['y']
        bottom=bbox['bottomright']['y']
        right=bbox['bottomright']['x']
        cv2.rectangle(imgcv,(left,top),(right,bottom),color[bbox['label']],3)
        
        text=bbox['label']+":"+bbox['confidence'].__str__()
        cv2.putText(imgcv,text,(left,max(top-12,0)),0,1e-3*h,color[bbox['label']])   
    
    frameNum=frameNum+1
    video.write(imgcv)
    
    detectNum=detectNum+len(result)
    print('detect %d objects on frame %d (total objects: %d)'%(len(result),frameNum,detectNum))
    print(result)
    
video.release()
    
