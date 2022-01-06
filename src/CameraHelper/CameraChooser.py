from .CamPylonWrapper import CamPylonWrapper
from .CamCommonWrapper import CamCommonWrapper
from .CameraType import CameraType

class CameraChooser:
    def Choose(cameraType:CameraType):
        bSucceed = True
        camera = None
        if cameraType == CameraType.CamCommon:
            camera = CamCommonWrapper()
        elif cameraType == CameraType.CamBasler:
            camera = CamPylonWrapper()
        else: 
            bSucceed = False
        return (bSucceed,camera)