import face_recognition as face
import cv2,os
import matplotlib.pyplot as plt
import imageio

plt.ion()

reader = imageio.get_reader('data/Obama.mp4')
image_nums = reader.get_length()
for i, img in enumerate(reader):
	if i%30==0:
		locs=face.face_locations(img)

		for loc in locs:
			pt1=(loc[3],loc[0])
			pt2=(loc[1],loc[2])
			cv2.rectangle(img,pt1,pt2,(0,0,255),thickness=3)
		plt.imshow(img)
		plt.pause(0.01)
	

