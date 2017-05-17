import face_recognition as face
import cv2,os
from skimage import io

for subdir,dirs,files in os.walk('data/test'):
	for file in files:
		img=face.load_image_file(subdir+'/'+file)

		# [top, right, bottom, left]
		locs=face.face_locations(img)

		for loc in locs:
			pt1=(loc[3],loc[0])
			pt2=(loc[1],loc[2])
			cv2.rectangle(img,pt1,pt2,(0,0,255),thickness=3)

		io.imshow(img)
		io.show()
	
