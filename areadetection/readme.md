# abnormal object detection
### https://github.com/ISCAS007/keras-yolo3

1. download and convert weights
2. demo video and target area, target object detection
```
python yolo_video.py --input=/home/yzbx/Videos/sherbrooke_video.avi
```

### https://github.com/ISCAS007/yolov3
```
conda activate cuda10.0
python main.py --video_name ~/Videos/sherbrooke_video.avi --bbox 200 200 600 400 --label car
python main.py --video_name ~/Videos/sherbrooke_video.avi --bbox 100 400 500 500 --label person
```


# other object detection
- /home/yzbx/git/gnu/YOLO_tensorflow/scripts/demo-ioucheck.py
- /home/yzbx/git/gnu/keras-yolo3/test/demo-ioucheck.py
