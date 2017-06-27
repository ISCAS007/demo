# -*- coding: utf-8 -*-
#import sys
#sys.path.append('/home/yzbx/git/gnu/darkflow')

from darkflow.net.build import TFNet
import cv2
import numpy as np
import os,sys,json
import datetime
from mywebsocket import senddata

basedir="/home/yisa/git"
cfgfilepath=os.path.join(basedir,"yzbxLib/tmp/config/tiny-yolo-helmet_seatbelt.cfg")
weightsfilepath=os.path.join(basedir,"darknet/backup/tiny-yolo-helmet_seatbelt_final.weights")
#videofilepath='rtsp://47.92.4.47:554/x1704003?type=onvif'
#videofilepath='rtsp://47.92.4.47:554/PYS0001?type=onvif'
videofilepath='rtsp://t.qdrise.com.cn:554/x1703009?type=onvif'

cap=cv2.VideoCapture(videofilepath)
if not cap.isOpened():
    ret,cap=cv2.VideoCapture('/home/yisa/Videos/record2.mp4')
    
    if not cap.isOpened():
        print('cannot capture video')
        sys.exit()

options = {
"model": cfgfilepath,
"load": weightsfilepath, 
"threshold": 0.1,}

tfnet = TFNet(options)

def process(img):
    imgcv=img.copy()
    #imgcv = cv2.imread("/home/yisa/git/yzbxLib/tmp/1.jpg")
    result = tfnet.return_predict(imgcv)

    h,w,c=imgcv.shape
    color={}
    color['person']=(255,0,0)
    color['seatbelt']=(0,255,0)
    color['helmet']=(0,0,255)

    bboxes={}
    bboxes['person']=[]
    bboxes['seatbelt']=[]
    bboxes['helmet']=[]
    for bbox in result:
        print(bbox)
        left=bbox['topleft']['x']
        top=bbox['topleft']['y']
        bottom=bbox['bottomright']['y']
        right=bbox['bottomright']['x']
        cv2.rectangle(imgcv,(left,top),(right,bottom),color[bbox['label']],3)
        
        text=bbox['label']+":"+bbox['confidence'].__str__()
        cv2.putText(imgcv,text,(left,max(top-12,0)),0,1e-3*h,color[bbox['label']])
        
        # convert to  non-maximum suppression format
        bboxes[bbox['label']].append((left,top,right,bottom))
    
    # 0 未知类型, 1. 未带安全帽， 2. 吸烟， 3. 打电话
    warning_type=0
    if len(bboxes['person']) > len(bboxes['helmet']) : 
        warning_type=1

    USE_SQL=False
    return_dict={}
    if USE_SQL:
        return_dict['UID']='unknown'
        return_dict['DEVICE_ID']='unknown'
        return_dict['WARN_TYPE']=warning_type=1
        return_dict['WARN_TIME']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return_dict['DETAIL_INFO']=result='no detatil'
    else :
        return_dict['device']='unknown'
        return_dict['time']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return_dict['type']=warning_type
        #return_dict['detail']=json.dumps(result)
        return_dict['detail']='no detail'
        #return_dict['image']=img_len

    cv2.imshow('show',imgcv)
    cv2.waitKey(10)
    return return_dict

frameNum=1
while True:
    ret,imgcv=cap.read()
    if not ret:
        break
    
    print('process start, framenum=%d'%frameNum)
    return_dict=process(imgcv)
    senddata(return_dict,imgcv)
    
    print('process end, framenum=%d'%frameNum)
    frameNum=frameNum+1

