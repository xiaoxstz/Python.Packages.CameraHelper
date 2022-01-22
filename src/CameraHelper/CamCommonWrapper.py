# cython: language_level=3
import cv2
import threading
class CamCommonWrapper:
    def __init__(self, video_source=0):
        # Open the video source
        self.__camera = cv2.VideoCapture(video_source,cv2.CAP_DSHOW)
        if not self.__camera.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = int(self.__camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.__camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def start_grab_thread(self, grabbed_callback):
        self.grab_thread = threading.Thread(target=self.__grab_loop,
        args=("grab_thread",grabbed_callback)
        )
        self.grab_thread.start()
    
    def __grab_loop(self, thread_name:str,grabbed_callback):
        while self.__camera.isOpened():
            self.__grab(grabbed_callback)
    
    def __grab(self, grabbed_callback,timeout:int=5000):
        ret,frame = self.get_frame()
        if ret:
            grabbed_callback(frame)

    def get_frame(self):
        ret = False
        if self.__camera.isOpened():
            ret, frame = self.__camera.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
    
    def Close(self):
        if self.__camera.isOpened():
            self.__camera.release()

    # Release the video source when the object is destroyed
    def __del__(self):
        self.Close()

def grabbed_callback(frame):
    print("--grabbed_callback")

if __name__ == '__main__':
    cam = CamCommonWrapper()
    cam.start_grab_thread(grabbed_callback)