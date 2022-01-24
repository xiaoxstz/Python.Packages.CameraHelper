# cython: language_level=3
from .CamPylonWrapper import CamPylonWrapper
from .CamCommonWrapper import CamCommonWrapper
from .CameraType import CameraType
from .CamPylonFreerun import CamPylonFreerun

class CameraChooser:
    def Choose(cameraType:CameraType):
        bSucceed = False
        camera = None
        try:
            if cameraType == CameraType.CommonWrapper:
                camera = CamCommonWrapper()
                bSucceed = True
            elif cameraType == CameraType.PylonWrapper:
                camera = CamPylonWrapper()
                bSucceed = True
            elif cameraType == CameraType.PylonFreerun:
                camera = CamPylonFreerun()
                if camera.IsConnected():
                    bSucceed = True
                else:
                    bSucceed = False
            else: 
                bSucceed = False
        except RuntimeError as ex:
            print(ex)
            bSucceed = False
        except Exception as ex:
            print(ex)
            bSucceed = False
        return (bSucceed,camera)