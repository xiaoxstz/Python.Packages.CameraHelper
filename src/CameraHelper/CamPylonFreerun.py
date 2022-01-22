# cython: language_level=3
"""this class can reach the max frame rate"""
from pypylon import pylon # pip install pypylon
from pypylon import genicam

class CamPylonFreerun:
    def __init__(self) -> None:
        try:
            # Create an instant camera object for the camera device found first.
            self.__camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
            self.__camera.Open()
            self.width = self.__camera.Width.GetValue() 
            self.height = self.__camera.Height.GetValue()
            
        except genicam.GenericException as e:
            # Error handling.
            print("An exception occurred.", e.GetDescription())
    
    def start_grab_thread(self,imageEvent:pylon.ImageEventHandler):
        # For demonstration purposes only, register another image event handler.
        self.__camera.RegisterImageEventHandler(imageEvent(), pylon.RegistrationMode_Append, pylon.Cleanup_Delete)

        # Start the grabbing using the grab loop thread, by setting the grabLoopType parameter
        # to GrabLoop_ProvidedByInstantCamera. The grab results are delivered to the image event handlers.
        # The GrabStrategy_OneByOne default grab strategy is used.
        self.__camera.StartGrabbing(pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera)
        pass

    def Close(self):
        if self.__camera.IsGrabbing():
            # Releasing the resource    
            self.__camera.StopGrabbing()

    def __del__(self):
        """called when use `del` command"""
        print("__del__")
        self.Close()


class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):
        """this function should not put the code that costs too much time"""
        print("OnImageGrabbed")

if __name__ == '__main__':
    cam = CamPylonFreerun()
    cam.start_grab_thread(SampleImageEventHandler)
    print(f"image size: ({cam.height},{cam.width})")
    import time
    time.sleep(1)
    cam.Close()
