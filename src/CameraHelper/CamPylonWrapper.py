from pypylon import pylon # pip install pypylon
import threading

class CamPylonWrapper:
    def __init__(self) -> None:
        # connecting to the first available camera
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

        self.camera.Open()
        
        # Grabing continuously (video) with minimal delay
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        self.__converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        self.__converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.__converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

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
        while self.camera.IsGrabbing():
            self.__grab(grabbed_callback)
    
    def __grab(self, grabed_callback,timeout:int=5000):
        grabResult = self.camera.RetrieveResult(timeout, pylon.TimeoutHandling_ThrowException)
        if grabResult.GrabSucceeded():
            grabed_callback(grabResult)
            grabResult.Release()
        else:
            grabResult.Release()
            return None
    
    def get_frame(self,timeout:int=5000):
        grabResult = self.camera.RetrieveResult(timeout, pylon.TimeoutHandling_ThrowException)
        try:
            if grabResult.GrabSucceeded():
                img = self.convert(grabResult)
                image = img.GetArray()  # shape: (height,width)
                grabResult.Release()
                return (True,image)
            else:
                grabResult.Release()
                return (False,None)
        except Exception as e:
            print(e)
            return (False, None)


    def convert(self,grabResult):
        image = self.__converter.Convert(grabResult)
        return image

    
    def __Close(self):
        # Releasing the resource    
        self.camera.StopGrabbing()
    
    def __del__(self):
        self.__Close()