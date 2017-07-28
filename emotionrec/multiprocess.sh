#!/bin/bash
source requirement.sh

python3 fc.py /media/sdb/ISCAS_Dataset/emotion001.mp4 opencv
python3 fc.py /media/sdb/ISCAS_Dataset/emotion002.mp4 opencv
python3 fc.py /media/sdb/ISCAS_Dataset/emotion003.mp4 opencv
python3 fc.py /media/sdb/ISCAS_Dataset/emotion004.mp4 opencv
python3 fc.py /media/sdb/ISCAS_Dataset/emotion005.mp4 opencv

python3 fc.py /media/sdb/ISCAS_Dataset/emotion001.mp4 dlib
python3 fc.py /media/sdb/ISCAS_Dataset/emotion002.mp4 dlib
python3 fc.py /media/sdb/ISCAS_Dataset/emotion003.mp4 dlib
python3 fc.py /media/sdb/ISCAS_Dataset/emotion004.mp4 dlib
python3 fc.py /media/sdb/ISCAS_Dataset/emotion005.mp4 dlib

python3 fc.py /media/sdb/ISCAS_Dataset/moviesets001.mp4 opencv
python3 fc.py /media/sdb/ISCAS_Dataset/moviesets002.mp4 opencv
python3 fc.py /media/sdb/ISCAS_Dataset/moviesets003.mp4 opencv

python3 fc.py /media/sdb/ISCAS_Dataset/moviesets001.mp4 dlib
python3 fc.py /media/sdb/ISCAS_Dataset/moviesets002.mp4 dlib
python3 fc.py /media/sdb/ISCAS_Dataset/moviesets003.mp4 dlib
