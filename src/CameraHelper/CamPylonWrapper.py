from pypylon import pylon # pip install pypylon
import threading
from .PylonImageConvert import PylonImageConvert

class CamPylonWrapper:
    def __init__(self) -> None:
        # connecting to the first available camera
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.__bExit = False

        self.camera.Open()
        
        # Grabing continuously (video) with minimal delay
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        # get image size
        # self.width = self.camera.Width.GetValue()    # not right value
        # self.height = self.camera.Height.GetValue()
        ret,img = self.get_frame()
        if ret:
            self.height = img.shape[0]
            self.width = img.shape[1]

    
    def start_grab_thread(self, grabbed_callback):
        self.grab_thread = threading.Thread(target=self.__grab_loop,
        args=("grab_thread",grabbed_callback)
        )
        self.grab_thread.start()
    
    def __grab_loop(self, thread_name:str,grabbed_callback):
        while self.camera.IsGrabbing() and not self.__bExit:
            self.__grab(grabbed_callback)
    
    def __grab(self, grabbed_callback,timeout:int=5000):
        grabResult = self.camera.RetrieveResult(timeout, pylon.TimeoutHandling_ThrowException)
        if grabResult.GrabSucceeded():
            grabbed_callback(grabResult)
            grabResult.Release()
        else:
            grabResult.Release()
            return None
    
    def get_frame(self,timeout:int=5000):
        grabResult = self.camera.RetrieveResult(timeout, pylon.TimeoutHandling_ThrowException)
        try:
            if grabResult.GrabSucceeded():
                img = PylonImageConvert.convert(grabResult)
                image = img.GetArray()  # shape: (height,width)
                grabResult.Release()
                return (True,image)
            else:
                grabResult.Release()
                return (False,None)
        except Exception as e:
            print(e)
            return (False, None)
    
    def Close(self):
        self.__bExit = True
        # Releasing the resource (not needed)
        # self.camera.StopGrabbing()
    
    def __del__(self):
        self.Close()