# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

class Image_Plot:
    def __init__(self):
        self.emotions_dict={0:'angry',1:'disgust',2:'fear',3:'happy',
                    4:'sad',5:'surprise',6:'neutral'}

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

        plt.subplot(1,2,1)
        plt.imshow(image)
        plt.title('image')
        plt.xticks([])
        plt.yticks([])

        plt.subplot(1,2,2)
        plt.xlabel('frame number')
        plt.ylabel('emotion')
        yticks=list(self.emotions_dict.values())
        plt.yticks(np.arange(len(yticks)),yticks)
        plt.plot(emotions_int)

        if showPlot:
            plt.show()

if __name__ == '__main__':
    testplot=Image_Plot()
    image=mpimg.imread('/home/yzbx/Pictures/yolo.png')
    emotions=['angry','angry','disgust','sad']
    testplot.emotion_plot(image,emotions)