from CameraHelper import PylonImageConvert
from CameraHelper import CamPylonFreerun
from pypylon import pylon
import cv2
import numpy as np

class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):
        """this function should not put the code that costs too much time"""
        # print("OnImageGrabbed start")
        global image
        if grabResult.GrabSucceeded():
            img = PylonImageConvert.convert(grabResult)
            image = img.GetArray()
        else:
            pass
        # print("OnImageGrabbed end")
    
    def test(self):
        pass

if __name__ == '__main__':
    win_name = "camera"
    cam = CamPylonFreerun()
    if cam.IsConnected():
        cam.start_grab_thread(SampleImageEventHandler)
        image = np.zeros([cam.height,cam.width,3],dtype=np.uint8)
        while True:
            cv2.imshow(win_name, image)
            cv2.resizeWindow(win_name,960,960)
            key = cv2.waitKey(1)
            if key == 27:
                break
        cv2.destroyAllWindows()
    else:
        print("failed to connect the camera")



