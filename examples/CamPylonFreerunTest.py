from CameraHelper import PylonImageConvert
from CameraHelper import CamPylonFreerun
from pypylon import pylon

class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):
        image = PylonImageConvert.convert(grabResult)
        print("OnImageGrabbed")

if __name__ == '__main__':
    cam = CamPylonFreerun(SampleImageEventHandler)
    import time
    time.sleep(1)
    cam.Close()