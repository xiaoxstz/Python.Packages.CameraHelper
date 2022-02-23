# cython: language_level=3
"""this class can reach the max frame rate"""
from pypylon import pylon # pip install pypylon
from pypylon import genicam

class CamPylonFreerun:
    def __init__(self,camera_obj) -> None:
        self.__Connected = False
        try:
            self.__camera = camera_obj
            self.__camera.Open()
            self.width = self.__camera.Width.GetValue() 
            self.height = self.__camera.Height.GetValue()
            self.__Connected = True
            
        except genicam.GenericException as e:
            # Error handling.
            print("An exception occurred.", e.args[0])
            self.__Connected = False

    
    def start_grab_thread(self,imageEvent:pylon.ImageEventHandler):
        # For demonstration purposes only, register another image event handler.
        self.__camera.RegisterImageEventHandler(imageEvent(), pylon.RegistrationMode_Append, pylon.Cleanup_Delete)

        # Start the grabbing using the grab loop thread, by setting the grabLoopType parameter
        # to GrabLoop_ProvidedByInstantCamera. The grab results are delivered to the image event handlers.
        # The GrabStrategy_OneByOne default grab strategy is used.
        self.__camera.StartGrabbing(pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera)
        pass

    def Close(self):
        if self.IsConnected():
            if self.__camera.IsGrabbing():
                # Releasing the resource    
                self.__camera.StopGrabbing()
                self.__Connected = False

    def __del__(self):
        """called when use `del` command"""
        print("camera: __del__")
        self.Close()
    
    def IsConnected(self):
        return self.__Connected

