from darkflow.net.build import TFNet
import cv2
import sys,os

crab_options = {
"config": "/home/yzbx/git/gnu/darkflow/yzbx/crab/",
"model": "/home/yzbx/git/gnu/darkflow/yzbx/crab/crab-tiny-yolo.cfg", 
"load": -1, 
"backup": "/home/yzbx/git/gnu/darkflow/yzbx/crab/tiny-yolo/",
"threshold": 0.1}

crab_carapace_options = {
"model": "/home/yzbx/git/gnu/darkflow/yzbx/crab/crab-carapace-tiny-yolo.cfg", 
"load": -1, 
"backup": "/home/yzbx/git/gnu/darkflow/yzbx/crab/crab-carapace/tiny-yolo/"}

snail_options = {
"model": "/home/yzbx/git/gnu/darkflow/yzbx/crab/snail-tiny-yolo.cfg", "load": -1, 
"backup": "/home/yzbx/git/gnu/darkflow/yzbx/crab/snail/tiny-yolo/", "threshold": 0.1}

_3c_options = {
"model": "/home/yzbx/git/gnu/darkflow/yzbx/crab/3c-tiny-yolo.cfg", "load": -1, 
"backup": "/home/yzbx/git/gnu/darkflow/yzbx/crab/3c/tiny-yolo/", "threshold": 0.1}

print("usage: python3 crab.py [appName] [imgName]")
print("appName: crab, crab_carapace, snail, 3c")

appName='3c'
imgName=''

if len(sys.argv) > 1:
    appName=sys.argv[1]

if appName=='crab':
    os.system('echo crab > labels.txt')
    options=crab_options
    imgName='crab.jpg'
elif appName.find('carapace')!=-1:
    os.system('echo "river crab carapace" > labels.txt')
    options=crab_carapace_options
    imgName='crab_carapace.jpg'
elif appName=='snail':
    os.system('echo snail > labels.txt')
    options=snail_options
    imgName='snail.jpg'
elif appName=='3c':
    os.system('echo crab > labels.txt')
    os.system('echo "river crab carapace" >> labels.txt')
    os.system('echo snail >> labels.txt')
    options=_3c_options
    imgName='snail.jpg'
else:
    print('unknown appName')
    sys.exit(-1)
    
if len(sys.argv) > 2:
    imgName=sys.argv[2]
    
tfnet = TFNet(options)

imgcv = cv2.imread(imgName)
imgcv=cv2.resize(imgcv,(640,480))
if imgcv is None:
    print('cannot open file %s'%imgName)
    
result = tfnet.return_predict(imgcv)
h,w,c=imgcv.shape
print('shape is ',imgcv.shape)
for bbox in result:
    print('bbox is ',bbox)
    left=bbox['topleft']['x']
    top=bbox['topleft']['y']
    bottom=bbox['bottomright']['y']
    right=bbox['bottomright']['x']
    cv2.rectangle(imgcv,(left,top),(right,bottom),(255,0,0),3)
    
    text=bbox['label']+":"+bbox['confidence'].__str__()
    cv2.putText(imgcv,text,(left,max(top-12,0)),0,1e-3*h,(0,255,0))
    
print('options is ',options)
print('result is ', result)
cv2.namedWindow(imgName,cv2.WINDOW_NORMAL)
cv2.imshow(imgName,imgcv)
cv2.waitKey(0)

