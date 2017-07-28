# from face_recognition import face_locations
# conflict with cuda
import cv2
import tensorflow as tf
from keras.models import load_model
import numpy as np
from statistics import mode
from utils import preprocess_input
from utils import get_labels
import os,sys
import imageio
import image_plot
import matplotlib.pyplot as plt

# config
gnu_code_path = '/home/yzbx/git/gnu/face_classification'

class FaceDetection:
    def __init__(self,srccode="opencv"):
        if srccode not in ["opencv","dlib"]:
            self.srccode = "opencv"
        self.srccode=srccode
        detection_model_path = os.path.join(gnu_code_path,
                                            'trained_models/detection_models/haarcascade_frontalface_default.xml')
        self.opencv_face_detection = cv2.CascadeClassifier(detection_model_path)

    def process(self,image):
        if self.srccode=="opencv":
            if len(image.shape)==2:
                gray=image
            else:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.opencv_face_detection.detectMultiScale(gray, 1.3, 5)
        elif self.srccode=="dlib":
            # to avoid package conflict
            from face_recognition import face_locations
            face_locations = face_locations(image)
            faces=[]
            for (t,r,b,l) in face_locations:
                faces.append((l,t,r-l,b-t))
        #todo elif self.srccode=='facenet':
        else:
            print('undefine srccode %s'%self.srccode)
            faces=[]
        return faces



class FaceClassification:
    def __init__(self,srccode="opencv"):
        self.fd=FaceDetection(srccode)
        # parameters
        emotion_model_path = os.path.join(gnu_code_path,'trained_models/emotion_models/simple_CNN.530-0.65.hdf5')
        gender_model_path = os.path.join(gnu_code_path,'trained_models/gender_models/simple_CNN.81-0.96.hdf5')

        # loading models

        self.emotion_classifier = load_model(emotion_model_path)
        self.gender_classifier = load_model(gender_model_path)

    def process_image(self,image_path,waitTime=0,showImage=True):
        #print('before loop')
        emotion_labels = get_labels('fer2013')
        gender_labels = get_labels('imdb')
        font = cv2.FONT_HERSHEY_SIMPLEX

        x_offset_emotion = 20
        y_offset_emotion = 40
        x_offset = 30
        y_offset = 60

        if type(image_path) is str:
            frame = cv2.imread(image_path)
        else:
            frame=image_path

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.fd.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        emotions=[]
        #print('start loop')
        for (x,y,w,h) in faces:
            face = frame[(y - y_offset):(y + h + y_offset),
                        (x - x_offset):(x + w + x_offset)]

            gray_face = gray[(y - y_offset_emotion):(y + h + y_offset_emotion),
                            (x - x_offset_emotion):(x + w + x_offset_emotion)]
                            
            if 0 in face.shape or 0 in gray_face.shape:
                continue
            try:
                #print('start try')
                face = cv2.resize(face, (48, 48))
                gray_face = cv2.resize(gray_face, (48, 48))
                #print('end try')
            except:
                #print('face shape is',face.shape)
                #print('gray_face shape is',gray_face.shape)
                continue
            face = np.expand_dims(face, 0)
            face = preprocess_input(face)
            gender_label_arg = np.argmax(self.gender_classifier.predict(face))
            gender = gender_labels[gender_label_arg]

            gray_face = preprocess_input(gray_face)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_label_arg = np.argmax(self.emotion_classifier.predict(gray_face))
            emotion = emotion_labels[emotion_label_arg]

            if gender == gender_labels[0]:
                gender_color = (0, 0, 255)
            else:
                gender_color = (255, 0, 0)

            cv2.rectangle(frame, (x, y), (x + w, y + h), gender_color, 2)
            cv2.putText(frame, emotion, (x, y - 30), font,
                            0.5, gender_color, 2, cv2.LINE_AA)
            cv2.putText(frame, gender, (x , y - 30 + 15), font,
                            0.5, gender_color, 2, cv2.LINE_AA)
            #print('x,y,w,h,emotion,gender',x,y,w,h,emotion,gender)
            print(emotion,gender)
            emotions.append(emotion)
                     
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # cv2.imwrite('predicted_test_image.png', frame)

        if showImage:
            cv2.imshow('predicted test image',frame)
            cv2.waitKey(waitTime)
        
        return frame,emotions

    def process_video(self,video_path):
        cap=cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print('cannot open video %s'%video_path)
            sys.exit(-1)
        
        # Define the codec and create VideoWriter object
        # DIVX, XVID, MJPG, X264, WMV1, WMV2
        # uppercase or lowercase ???
        fourcc = cv2.VideoWriter_fourcc(*'xvid')
        frameNum=0
        while True:
            ret,frame=cap.read()
            if not ret:
                if frameNum == 0:
                    print('cannot read video %s (but open okay!!!)'%video_path)
                    sys.exit(-1)
                else:
                    print('video %s process finished'%video_path)
                    break
            #print('start process image')
            out_frame,_=self.process_image(frame,waitTime=30)
            
            #print('out_frame.size is',out_frame.shape)
            if frameNum==0:
                #dirname=os.path.dirname(video_path)
                #basename=os.path.basename(video_path)
                #out_video_path=os.path.join(dirname,self.fd.srccode+"_"+basename)  
                filename,suffix=os.path.splitext(video_path)
                out_video_path=filename+"_"+self.fd.srccode+".avi"
                # out = cv2.VideoWriter(out_video_path,fourcc, 20.0, out_frame.shape[0:2])
                out=imageio.get_writer(out_video_path,fps=30)
                
            #print('start write frame')
            
            # out.write(out_frame)
            write_frame=cv2.cvtColor(out_frame,cv2.COLOR_BGR2RGB)
            out.append_data(write_frame)
            frameNum+=1
            
            if frameNum > 100:
                #break
                pass
                
        #if frameNum % 100 == 0:
            #print('frameNum is %d'%frameNum)
            print(frameNum)
        # Release everything if job is finished
        print('start release')
        cap.release()
        print('release video capture')
        #out.release()
        out.close()
        print('close video write')
        cv2.destroyAllWindows()
        print('destroy all windows')

    def emotion_visulization(self,video_path):
        plt.ion()
        myplt=image_plot.Image_Plot()
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print('cannot open video %s' % video_path)
            sys.exit(-1)

        frameNum = 0

        all_emotions=[]
        while True:
            ret, frame = cap.read()
            if not ret:
                if frameNum == 0:
                    print('cannot read video %s (but open okay!!!)' % video_path)
                    sys.exit(-1)
                else:
                    print('video %s process finished' % video_path)
                    break

            out_frame, emotions = self.process_image(frame,showImage=False)
            all_emotions.append(emotions)
            if frameNum == 0:
                filename, suffix = os.path.splitext(video_path)
                out_video_path = filename + "_" + self.fd.srccode + ".avi"
                out = imageio.get_writer(out_video_path, fps=30)

            write_frame = cv2.cvtColor(out_frame, cv2.COLOR_BGR2RGB)
            myplt.emotion_plot(write_frame,all_emotions)

            out.append_data(write_frame)
            frameNum += 1

            if frameNum > 100:
                # break
                pass

            print(frameNum)
        # Release everything if job is finished
        print('start release')
        cap.release()
        print('release video capture')
        out.close()
        print('close video write')
        cv2.destroyAllWindows()
        print('destroy all windows')

if __name__ == '__main__':
    image_path = os.path.join(gnu_code_path, 'images/test_image.jpg')

    image_suffix=('jpg','JPG','png','PNG','jpeg','JPEG','bmp','BMP')
    video_suffix=('mp4','MP4','avi','AVI','mov','MOV')
    if len(sys.argv) > 2:
        srccode=sys.argv[2]
    else:
        srccode="opencv"
    fc=FaceClassification(srccode=srccode)
    if len(sys.argv) > 1:
        input=sys.argv[1]
        if input.endswith(image_suffix):
            fc.process_image(input)
        else:
            #fc.process_video(input)
            fc.emotion_visulization(input)
    else:
        fc.process_image(image_path=image_path)
