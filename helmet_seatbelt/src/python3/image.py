# -*- coding: utf-8 -*-
import sys

sys.path.append('/home/yzbx/git/gnu/darkflow')
from darkflow.net.build import TFNet
import cv2


if sys.argc < 2:
    print('usage : python3 src/video.py xxx.mp4')
options = {"model": "/media/sdb/ISCAS_Dataset/helmet_seatbelt/config/tiny-yolo-helmet_seatbelt.cfg", "load": "/media/sdb/ISCAS_Dataset/helmet_seatbelt/tiny-yolo-helmet_seatbelt.weights", "threshold": 0.1}

tfnet = TFNet(options)

frame=cv2.imread(sys.argv[1])

result=tfnet.return_predict(imgcv)
print(result)
    
