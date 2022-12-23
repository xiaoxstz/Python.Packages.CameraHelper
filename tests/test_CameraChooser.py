import unittest
from CameraHelper import CameraDetector
from CameraHelper import CameraChooser
from CameraHelper import CameraType

from pypylon import pylon


class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):
        """this function should not put the code that costs too much time"""
        print("grabbed one")
    
    def test(self):
        pass

class Test(unittest.TestCase):
    def test_PylonFreerun(self):
        camera_info_list= CameraDetector.find_basler_cams()
        if len(camera_info_list) > 0:
            camera_info = camera_info_list[0]
            
            bSucceed, camera = CameraChooser.Choose(CameraType.PylonFreerun,camera_info)
            if camera.IsConnected():
                camera.start_grab_thread(SampleImageEventHandler)
                import time
                bExit = False
                while not bExit:
                    time.sleep(1)
                camera.Close()
            else:
                print("failed to open the camera")
        else:
            print("found no basler camera")
    
    def test_PylonWrapper(self):
        camera_info_list= CameraDetector.find_basler_cams()
        if len(camera_info_list) > 0:
            camera_info = camera_info_list[0]
            
            bSucceed, camera = CameraChooser.Choose(CameraType.PylonWrapper,camera_info)
            if camera.IsConnected():
                camera.start_grab_thread(SampleImageEventHandler)
                import time
                bExit = False
                while not bExit:
                    time.sleep(1)
                camera.Close()
            else:
                print("failed to open the camera")
        else:
            print("found no basler camera")
    
    def test_CommonWrapper(self):
        camera_info = dict()
        bSucceed, camera = CameraChooser.Choose(CameraType.CommonWrapper,camera_info)
        if bSucceed and camera.IsConnected():
            camera.start_grab_thread(SampleImageEventHandler)
            import time
            bExit = False
            while not bExit:
                time.sleep(1)
            camera.Close()
        else:
            print("failed to open the camera")

