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
"threshold": 0.1,
"backup": "/home/yzbx/git/gnu/darkflow/yzbx/crab/crab-carapace/tiny-yolo/"}

snail_options = {
"model": "/home/yzbx/git/gnu/darkflow/yzbx/crab/snail-tiny-yolo.cfg", "load": -1, 
"backup": "/home/yzbx/git/gnu/darkflow/yzbx/crab/snail/tiny-yolo/", "threshold": 0.1}

_3c_options = {
"model": "/home/yzbx/git/gnu/darkflow/yzbx/crab/3c-tiny-yolo.cfg", "load": -1, 
"backup": "/home/yzbx/git/gnu/darkflow/yzbx/crab/3c/tiny-yolo/", "threshold": 0.1}

print("usage: python3 crab.py [appName] [input dir] [output dir]")
print("appName: crab, crab_carapace, snail, 3c")

appName='3c'
input_dir='/media/sdb/ISCAS_Dataset/crab/river-crab-test'
output_dir=os.path.join(input_dir,'output')

if len(sys.argv) > 1:
    appName=sys.argv[1]

if appName=='crab':
    os.system('echo crab > labels.txt')
    options=crab_options
elif appName.find('carapace')!=-1:
    os.system('echo "river crab carapace" > labels.txt')
    options=crab_carapace_options
elif appName=='snail':
    os.system('echo snail > labels.txt')
    options=snail_options
elif appName=='3c':
    os.system('echo crab > labels.txt')
    os.system('echo "river crab carapace" >> labels.txt')
    os.system('echo snail >> labels.txt')
    options=_3c_options
else:
    print('unknown appName')
    sys.exit(-1)
    
if len(sys.argv) > 2:
    input_dir=sys.argv[2]
    
if len(sys.argv) > 3:
    output_dir=sys.argv[3]
    
tfnet = TFNet(options)
print('options is ',options)

img_suffix=('jpg','JPG','JPEG','jpeg','bmp','BMP','png','PNG')
for f in os.listdir(input_dir):
    print('file is',f)
    imgName=os.path.join(input_dir,f)
    if os.path.isfile(imgName) and imgName.endswith(img_suffix):
        imgcv = cv2.imread(imgName)
        imgcv=cv2.resize(imgcv,(640,480))
        if imgcv is None:
            print('cannot open file %s'%imgName)
            continue
            
        result = tfnet.return_predict(imgcv)
        h,w,c=imgcv.shape
        #print('shape is ',imgcv.shape)
        for bbox in result:
            #print('bbox is ',bbox)
            left=bbox['topleft']['x']
            top=bbox['topleft']['y']
            bottom=bbox['bottomright']['y']
            right=bbox['bottomright']['x']
            cv2.rectangle(imgcv,(left,top),(right,bottom),(255,0,0),3)
            
            text=bbox['label']+":"+bbox['confidence'].__str__()
            cv2.putText(imgcv,text,(left,max(top-12,0)),0,1e-3*h,(0,255,0))
            
        
        cv2.namedWindow(imgName,cv2.WINDOW_NORMAL)
        cv2.imshow(imgName,imgcv)
        
        outname=os.path.join(output_dir,imgName)
        cv2.imwrite(outname,imgcv)
        
        cv2.waitKey(0)

