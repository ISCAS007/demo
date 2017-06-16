from darkflow.net.build import TFNet
import cv2

# options = {"model": "cfg/yolo.cfg", "load": "bin/yolo.weights", "threshold": 0.1}
options = {"pbLoad": "yzbx/helmet_seatbelt_20170609/", "load": "bin/yolo.weights", "threshold": 0.1}

tfnet = TFNet(options)

imgcv = cv2.imread("./dataset/dog.jpg")
result = tfnet.return_predict(imgcv)
print(result)
