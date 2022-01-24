from CameraHelper import CamPylonWrapper

cam = CamPylonWrapper()
if cam.IsConnected():
    ret, img = cam.get_frame()
    if ret:
        shape = img.shape
        print(shape)
else:
    print("failed to connect the camera")
