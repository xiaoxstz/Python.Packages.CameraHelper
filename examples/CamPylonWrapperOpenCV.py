from CameraHelper import CamPylonWrapper
import cv2
import numpy as np

if __name__ == "__main__":
    win_name = "camera"
    cam = CamPylonWrapper()
    if cam.IsConnected():
        image = np.zeros([cam.height, cam.width, 3], dtype=np.uint8)
        while True:
            ret, image = cam.get_frame()
            if ret:
                cv2.imshow(win_name, image)
                cv2.resizeWindow(win_name, 960, 960)
            key = cv2.waitKey(1)
            if key == 27:
                break
        cv2.destroyAllWindows()
    else:
        print("failed to connect the camera")
