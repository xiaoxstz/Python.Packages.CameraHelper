from CameraHelper import PylonImageConvert
from CameraHelper import CamPylonFreerun
from pypylon import pylon


class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):
        """this function should not put the code that costs too much time"""
        if grabResult.GrabSucceeded():
            image = PylonImageConvert.convert(grabResult).GetArray()
            grabResult.Release()
            global frame_counter
            frame_counter += 1
            print(f"OnImageGrabbed, frame:{frame_counter}")
        else:
            pass
    
    def test(self):
        pass

if __name__ == '__main__':
    frame_counter = 0
    cam = CamPylonFreerun()
    if cam.IsConnected():
        cam.start_grab_thread(SampleImageEventHandler)
        import time
        bExit = False
        while not bExit:
            time.sleep(1)
        cam.Close()
    else:
        print("failed to open the camera")