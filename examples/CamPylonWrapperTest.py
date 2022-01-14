from CameraHelper import CamPylonWrapper

cam = CamPylonWrapper()
ret, img = cam.get_frame()
if ret:
    shape = img.shape
    print(shape)