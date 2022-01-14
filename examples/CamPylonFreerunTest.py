from CameraHelper import PylonImageConvert
from CameraHelper import CamPylonFreerun
from pypylon import pylon

class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):
        """this function should not put the code that costs too much time"""
        image = PylonImageConvert.convert(grabResult)
        print("OnImageGrabbed")
    
    def test(self):
        pass

if __name__ == '__main__':
    cam = CamPylonFreerun(SampleImageEventHandler)
    import time
    time.sleep(1)
    cam.Close()