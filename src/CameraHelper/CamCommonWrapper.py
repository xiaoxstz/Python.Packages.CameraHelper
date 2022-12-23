# cython: language_level=3
import cv2
import threading


class CamCommonWrapper:
    def __init__(self, camera_info: dict):
        self.__Connected = False
        if camera_info["TL Type"] != "Directshow":
            self.__Connected = False
            return

        # Open the video source
        self.__camera = cv2.VideoCapture(camera_info["index"], cv2.CAP_DSHOW)
        if self.__camera.isOpened():
            # Get video source width and height
            self.width = int(self.__camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.__camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

            self.__Connected = True

    def start_grab_thread(self, grabbed_callback):
        self.grab_thread = threading.Thread(
            target=self.__grab_loop, args=("grab_thread", grabbed_callback)
        )
        self.grab_thread.start()

    def __grab_loop(self, thread_name: str, grabbed_callback):
        while self.__camera.isOpened():
            self.__grab(grabbed_callback)

    def __grab(self, grabbed_callback, timeout: int = 5000):
        ret, frame = self.get_frame()
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

    def IsConnected(self):
        return self.__Connected


def grabbed_callback(frame):
    print("--grabbed_callback")


if __name__ == "__main__":
    camera_info = dict()
    camera_info["TL Type"] = "Directshow"
    camera_info["index"] = 0
    cam = CamCommonWrapper(camera_info)
    if cam.IsConnected():
        cam.start_grab_thread(grabbed_callback)
    else:
        print("failed to open the camera")
