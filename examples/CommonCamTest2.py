from CameraHelper import CamCommonWrapper

def grabbed_callback(frame):
    print("--grabbed_callback")

if __name__ == '__main__':
    cam = CamCommonWrapper()
    if cam.IsConnected():
        cam.start_grab_thread(grabbed_callback)
    else:
        print("failed to connect the camera")
