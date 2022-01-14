"""this class can reach the max frame rate"""
from pypylon import pylon # pip install pypylon
from pypylon import genicam

class CamPylonFreerun:
    def __init__(self,imageEvent:pylon.ImageEventHandler) -> None:
        try:
            # Create an instant camera object for the camera device found first.
            self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

            # For demonstration purposes only, register another image event handler.
            self.camera.RegisterImageEventHandler(imageEvent(), pylon.RegistrationMode_Append, pylon.Cleanup_Delete)

            # Start the grabbing using the grab loop thread, by setting the grabLoopType parameter
            # to GrabLoop_ProvidedByInstantCamera. The grab results are delivered to the image event handlers.
            # The GrabStrategy_OneByOne default grab strategy is used.
            self.camera.StartGrabbing(pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera)
            
        except genicam.GenericException as e:
            # Error handling.
            print("An exception occurred.", e.GetDescription())

    def Close(self):
        if self.camera.IsGrabbing():
            # Releasing the resource    
            self.camera.StopGrabbing()

    def __del__(self):
        """called when use `del` command"""
        print("__del__")
        self.Close()


class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):
        print("OnImageGrabbed")

if __name__ == '__main__':
    cam = CamPylonFreerun(SampleImageEventHandler)
    import time
    time.sleep(1)
    cam.Close()
