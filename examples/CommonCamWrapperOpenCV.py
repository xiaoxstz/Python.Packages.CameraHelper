from CameraHelper import CamCommonWrapper
import cv2
import numpy as np

if __name__ == '__main__':
    win_name = "camera"
    cam = CamCommonWrapper()
    image= np.zeros([cam.height,cam.height,3],dtype=np.uint8)    
    while True:
        ret, image = cam.get_frame()
        if ret:
            cv2.imshow(win_name, image)
            cv2.resizeWindow(win_name,960,960)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cv2.destroyAllWindows()