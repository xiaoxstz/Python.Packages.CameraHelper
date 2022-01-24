# cython: language_level=3
from pypylon import pylon # pip install pypylon
import threading
from .PylonImageConvert import PylonImageConvert

class CamPylonWrapper:
    def __init__(self) -> None:
        self.__Connected = False

        try:
            # connecting to the first available camera
            self.__camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
            self.__bExit = False

            self.__camera.Open()

            # Grabing continuously (video) with minimal delay
            self.__camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

            # get image size
            # self.width = self.__camera.Width.GetValue()    # not right value
            # self.height = self.__camera.Height.GetValue()
            ret,img = self.get_frame()
            if ret:
                self.height = img.shape[0]
                self.width = img.shape[1]
            self.__Connected = True
        except Exception as ex:
            print(ex)
            self.__Connected = False
    
    def start_grab_thread(self, grabbed_callback):
        self.grab_thread = threading.Thread(target=self.__grab_loop,
        args=("grab_thread",grabbed_callback)
        )
        self.grab_thread.start()
    
    def __grab_loop(self, thread_name:str,grabbed_callback):
        while self.__camera.IsGrabbing() and not self.__bExit:
            self.__grab(grabbed_callback)
    
    def __grab(self, grabbed_callback,timeout:int=5000):
        grabResult = self.__camera.RetrieveResult(timeout, pylon.TimeoutHandling_ThrowException)
        if grabResult.GrabSucceeded():
            grabbed_callback(grabResult)
            grabResult.Release()
        else:
            grabResult.Release()
            return None
    
    def get_frame(self,timeout:int=5000):
        if self.IsConnected():
            grabResult = self.__camera.RetrieveResult(timeout, pylon.TimeoutHandling_ThrowException)
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
        else:
            return (False, None)

    def Close(self):
        self.__bExit = True
        # Releasing the resource (not needed)
        # self.__camera.StopGrabbing()
    
    def __del__(self):
        self.Close()
    
    def IsConnected(self):
        return self.__Connected

def grabbed_callback(frame):
    print("--grabbed_callback")

if __name__ == '__main__':
    cam = CamPylonWrapper()
    if cam.IsConnected():
        cam.start_grab_thread(grabbed_callback)
    else:
        print("failed to open the camera")
