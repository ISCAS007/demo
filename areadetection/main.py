# -*- coding: utf-8 -*-

from algorithm import yolov3_slideWindows
from easydict import EasyDict as edict
import argparse
import os
import cv2
import sys
yolov3_path=os.path.expanduser('~/git/gnu/code/yolov3')
if yolov3_path not in sys.path:
    sys.path.insert(0,yolov3_path)
from utils.utils import plot_one_box

def isObjectInArea(rule,bbox):
    """
        rule=bbox={'bbox':list(xyxy),'conf':conf,'label':dog}
    """
    if rule['label']!=bbox['label']:
        return False,'label'

    if rule['conf']>bbox['conf']:
        return False,'conf'

    rect1=rule['bbox']
    rect2=bbox['bbox']

    w=min(rect1[2],rect2[2])-max(rect1[0],rect2[0])
    h=min(rect1[3],rect2[3])-max(rect1[1],rect2[1])

    if w<=0 or h <=0:
        return False,'iou'
    else:
        return True,'warning'

class Area_Detector():
    def __init__(self,config):
        self.config=config

        opt=edict()
        opt.root_path=config.root_path
        opt.cfg=os.path.join(config.root_path,config.cfg)
        opt.data_cfg=os.path.join(config.root_path,config.data_cfg)
        opt.weights=os.path.join(config.root_path,config.weights)
        opt.img_size=config.img_size
        self.detector=yolov3_slideWindows(opt)

    def process_frame(self,frame):
        image,bboxes=self.detector.process_slide(frame)
        return image,bboxes

    def process_video(self,video_name):
        cap=cv2.VideoCapture(video_name)
        if not cap.isOpened():
            assert False,'cannot open video {}'.format(video_name)

        COLOR_AREA=(0,0,255)
        COLOR_ALARM=(0,0,255)
        COLOR_NORMAL=(0,255,0)

        # config for writer video
        save_video_name='{}_{}'.format(self.config.label,os.path.basename(video_name))
        codec = cv2.VideoWriter_fourcc(*"mp4v")
        fps=30
        writer=None

        rule={'bbox':self.config.bbox,
              'conf':self.config.conf,
              'label':self.config.label}
        while True:
            ret,frame=cap.read()
            if ret:
                image,bboxes=self.detector.process_slide(frame)
                for bbox in bboxes:
                    flag,reason=isObjectInArea(rule,bbox)
                    if flag:
                        color=COLOR_ALARM
                    else:
                        color=COLOR_NORMAL

                    plot_one_box(bbox['bbox'], frame, label=bbox['label']+' %s %0.2f'%(reason,bbox['conf']), color=color)

                frame=cv2.rectangle(img=frame, pt1=tuple(rule['bbox'][0:2]), pt2=tuple(rule['bbox'][2:4]), color=COLOR_AREA, thickness=2)
                cv2.imshow(self.config.label,frame)
                key=cv2.waitKey(30)
                if key==ord('q'):
                    break

                if writer is None:
                    height,width,_=frame.shape
                    writer=cv2.VideoWriter(save_video_name,
                            codec, fps,
                            (width, height))

                writer.write(frame)
            else:
                break

        if writer is not None:
            writer.release()

        cap.release()

class Config(edict):
    def __init__(self):
        super().__init__()
        self.cfg=''
        self.data_cfg=''
        self.weights=''
        self.root_path=''
        self.img_size=416
        self.label='car'
        self.conf=0.2
        self.bbox=[20,20,100,100]
        self.video_name='test.mp4'

        self.get_parser()

    def get_parser(self):
        parser = argparse.ArgumentParser()

        parser.add_argument('--root_path',type=str,default=os.path.expanduser('~/git/gnu/code/yolov3'),help='config root path for cfg, data_cfg and weights')
        parser.add_argument('--cfg', type=str, default='cfg/yolov3.cfg', help='cfg file path')
        parser.add_argument('--data_cfg', type=str, default='data/coco.data', help='coco.data file path')
        parser.add_argument('--weights', type=str, default='weights/yolov3.weights', help='path to weights file')
        parser.add_argument('--label',default='car',choices=['car','person'],help='the class to detect')
        parser.add_argument('--conf',type=float,default=0.2,help='conf threshold for object')
        parser.add_argument('--bbox',type=int,nargs=4,default=[20,20,100,100],help='x1,y1,x2,y2 for bbox')
        parser.add_argument('--video_name',required=True,help='input video name')

        args = parser.parse_args()
        sort_keys=sorted(list(self.keys()))
        #TODO remove function key words
        for key in sort_keys:
            if hasattr(args,key):
                print('{} = {} (default: {})'.format(key,args.__dict__[key],self[key]))
                self[key]=args.__dict__[key]
            else:
                if callable(self[key]):
                    pass
                else:
                    print('{} : (default:{})'.format(key,self[key]))

        for key in args.__dict__.keys():
            if key not in self.keys():
                print('{} : unused keys {}'.format(key,args.__dict__[key]))


if __name__ == '__main__':
    config=Config()
    detector=Area_Detector(config)
    detector.process_video(config.video_name)