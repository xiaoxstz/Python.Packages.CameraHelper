from .CamPylonWrapper import CamPylonWrapper
from .CamCommonWrapper import CamCommonWrapper
from .CameraType import CameraType
from .CamPylonFreerun import CamPylonFreerun

class CameraChooser:
    def Choose(cameraType:CameraType):
        bSucceed = True
        camera = None
        if cameraType == CameraType.CommonWrapper:
            camera = CamCommonWrapper()
            bSucceed = True
        elif cameraType == CameraType.PylonWrapper:
            camera = CamPylonWrapper()
            bSucceed = True
        elif cameraType == CameraType.PylonFreerun:
            camera = CamPylonFreerun()
            bSucceed = True
        else: 
            bSucceed = False
        return (bSucceed,camera)