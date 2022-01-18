from CameraHelper import PylonImageConvert
from CameraHelper import CamPylonFreerun
from pypylon import pylon

class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):
        """this function should not put the code that costs too much time"""
        image = PylonImageConvert.convert(grabResult)
        global frame_counter
        frame_counter += 1
        print(f"OnImageGrabbed, frame:{frame_counter}")
    
    def test(self):
        pass

if __name__ == '__main__':
    frame_counter = 0
    cam = CamPylonFreerun()
    cam.start_grab_thread(SampleImageEventHandler)
    import time
    bExit = False
    while not bExit:
        time.sleep(1)
    cam.Close()