from CameraHelper import CamCommonWrapper

cam = CamCommonWrapper()
ret, img = cam.get_frame()
if ret:
    shape = img.shape
    print(shape)