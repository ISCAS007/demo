# -*- coding: utf-8 -*-
#import sys
#sys.path.append('/home/yzbx/git/gnu/darkflow')

from darkflow.net.build import TFNet
import cv2
import numpy as np
import os,sys,json
import datetime
from mywebsocket import senddata
import time

basedir="/home/yisa/git"
cfgfilepath=os.path.join(basedir,"yzbxLib/tmp/config/tiny-yolo-helmet_seatbelt.cfg")
weightsfilepath=os.path.join(basedir,"darknet/backup/tiny-yolo-helmet_seatbelt_final.weights")

#videofilepath='rtsp://47.92.4.47:554/x1704003?type=onvif'
#videofilepath='rtsp://47.92.4.47:554/PYS0001?type=onvif'
videofilepath='rtsp://t.qdrise.com.cn:554/x1703009?type=onvif'
if len(sys.argv) > 1:
    string=sys.argv[1]
    if(string.find('rtsp') != -1):
        print('use rtsp: ',sys.argv[1])
        videofilepath=sys.argv[1]
        print('rtsp address is :',videofilepath)
    elif string.find('10.206')!= -1:
        print('use ip: ',sys.argv[1])
        videofilepath='rtsp://agy:!agy12345@%s:554/'%string
        print('rtsp address is :',videofilepath)
    else:
        print('use device: ',sys.argv[1])
        videofilepath='rtsp://t.qdrise.com.cn:554/%s?type=onvif'%string
        print('rtsp address is :',videofilepath)
        

#options = {
#"model": cfgfilepath,
#"load": weightsfilepath, 
#"threshold": 0.2,}

options = {"model": "weights/tiny-yolo-helmet_seatbelt-english.cfg", "load": -1, "threshold": 0.2, "backup": "weights/darkflow/english/"}

tfnet = TFNet(options)

print('load tfnet okay!!!'+'*'*60)

def getDeviceId(url):
    if url.find('onvif')!=-1:
        start=url.rfind('/')+1
        end=url.rfind('?')

        if end <= start:
            return 'unknown'
        return url[start:end]
    elif len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return 'unknow'

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
    if len(bboxes['helmet']) > 0:
        SendFlag=True
    else :
        SendFlag=False

    USE_SQL=False
    return_dict={}
    if USE_SQL:
        return_dict['UID']='unknown'
        return_dict['DEVICE_ID']=getDeviceId(videofilepath)
        return_dict['WARN_TYPE']=warning_type
        return_dict['WARN_TIME']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return_dict['DETAIL_INFO']=result='no detatil'
    else :
        return_dict['device']=getDeviceId(videofilepath)
        return_dict['time']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return_dict['type']=warning_type
        #return_dict['detail']=json.dumps(result)
        return_dict['detail']='no detail'
        #return_dict['image']=img_len

    cv2.imshow('show',imgcv)
    cv2.waitKey(10)
    return return_dict,imgcv,SendFlag

print('start read rtsp'+'*'*60)
frameNum=1

cap=cv2.VideoCapture(videofilepath)
if not cap.isOpened():
    print('cannot capture video: %s'%videofilepath)
    sys.exit()

while True:
    ret,imgcv=cap.read()
    print('end read rtsp'+'*'*60)
    if not ret:
        if frameNum==1 :
            print('cannot open video')
        else:
            print('video read finished')
        break
    
    print('process start, framenum=%d'%frameNum)
    return_dict,imgcv,SendFlag=process(imgcv)
    
    if SendFlag:
        senddata(return_dict,imgcv)
    
    print('process end, framenum=%d'%frameNum)
    frameNum=frameNum+1

    time.sleep(5)
    
cap.release()

