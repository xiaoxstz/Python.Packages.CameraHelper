"""
This program has been tested on:
* the camera "HIKVISION E14a"
"""
from CameraHelper import CamCommonWrapper
import cv2
import numpy as np

if __name__ == '__main__':
    win_name = "camera"
    cam = CamCommonWrapper()
    image= np.zeros([cam.height,cam.height,3],dtype=np.uint8) 
    tranformation = cv2.COLOR_BGR2RGB   
    while True:
        ret, image = cam.get_frame()
        if ret:
            imgshown = cv2.cvtColor(image, tranformation)
            cv2.imshow(win_name, imgshown)
            cv2.resizeWindow(win_name,960,960)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cv2.destroyAllWindows()