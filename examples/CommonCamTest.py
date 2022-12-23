from CameraHelper import CamCommonWrapper

camera_info=dict()
camera_info['TL Type'] = "Directshow"
camera_info["index"] = 0

cam = CamCommonWrapper(camera_info)
if cam.IsConnected():
    ret, img = cam.get_frame()
    if ret:
        shape = img.shape
        print(shape)
else:
    print("failed to connect the camera")
