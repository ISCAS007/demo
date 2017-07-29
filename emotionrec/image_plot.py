# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import random

class Image_Plot:
    def __init__(self):
        self.emotions_dict={0:'angry',1:'disgust',2:'fear',3:'happy',
                    4:'sad',5:'surprise',6:'neutral'}

        self.imagefig=None
        self.plotfig=None

    def test(self):
        # Simple data to display in various forms
        x1 = np.linspace(0.0, 5.0)
        x2 = np.linspace(0.0, 2.0)

        y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
        y2 = np.cos(2 * np.pi * x2)

        plt.subplot(1, 2, 1)
        plt.plot(x1, y1, 'ko-')
        plt.title('video')
        # plt.ylabel('Damped oscillation')
        plt.xticks([])
        plt.yticks([])

        plt.subplot(1, 2, 2)
        plt.plot(x2, y2, 'r.-')
        plt.xlabel('time (s)')
        plt.ylabel('Undamped')

        plt.show()

    def emotion_plot(self,image,emotions,showPlot=True):
        emotions_int=[]
        for emotion in emotions:
            for i in self.emotions_dict.keys():
                if emotion==self.emotions_dict[i]:
                    emotions_int.append(i)
                    break
            else:
                print('unknow emotion: ',emotion)

        if self.imagefig is None:
            plt.subplot(1,2,1)
            plt.title('emotion is %s'%emotions[-1])
            plt.xticks([])
            plt.yticks([])
            self.imagefig=plt.imshow(image)
        else:
            plt.subplot(1, 2, 1)
            plt.title('emotion is %s' % emotions[-1])
            self.imagefig.set_data(image)

        if self.plotfig is None:
            plt.subplot(1,2,2)
            plt.xlabel('frame number')
            plt.ylabel('emotion')
            yticks=list(self.emotions_dict.values())
            plt.yticks(np.arange(len(yticks)),yticks)
            plt.ylim(ymin=0, ymax=len(self.emotions_dict))
            self.plotfig,=plt.plot(range(len(emotions_int)),emotions_int)
        else:
            plt.subplot(1, 2, 2)
            self.plotfig.set_data(range(len(emotions_int)),emotions_int)
            plt.xlim(xmax=len(emotions_int))
            plt.ylim(ymin=0, ymax=len(self.emotions_dict))
            plt.draw()

        if showPlot:
            plt.show()
        else:
            plt.pause(0.5)

if __name__ == '__main__':
    plt.ion()
    #plt.figure(num=1,figsize=(600,400))
    testplot=Image_Plot()
    image=mpimg.imread('/home/yzbx/Pictures/yolo.png')
    emotions=['angry','angry','disgust','sad']
    testplot.emotion_plot(image,emotions,False)

    images=[]
    images.append(image)
    image=mpimg.imread('/home/yzbx/Pictures/step1.png')
    images.append(image)
    image = mpimg.imread('/home/yzbx/Pictures/step2.png')
    images.append(image)
    image = mpimg.imread('/home/yzbx/Pictures/step3.png')
    images.append(image)
    image = mpimg.imread('/home/yzbx/Pictures/step4.png')
    images.append(image)
    for i in range(100):
        emotion=testplot.emotions_dict[random.randint(0,6)]
        emotions.append(emotion)
        print('emotions len',len(emotions))
        image=images[random.randint(0,len(images)-1)]
        testplot.emotion_plot(image,emotions,False)