# cython: language_level=3
from .CamPylonWrapper import CamPylonWrapper
from .CamCommonWrapper import CamCommonWrapper
from .CameraType import CameraType
from .CamPylonFreerun import CamPylonFreerun
from .CameraDetector import CameraDetector

class CameraChooser:
    def Choose(cameraType:CameraType):
        bSucceed = False
        camera = None
        camera_detector = CameraDetector()
        try:
            if cameraType == CameraType.CommonWrapper:
                camera = CamCommonWrapper()
                bSucceed = True
            elif cameraType == CameraType.PylonWrapper or cameraType == CameraType.PylonFreerun:
                basler_dict_list = camera_detector.find_basler_cams()
                if len(basler_dict_list) == 0:
                    pass
                elif len(basler_dict_list) == 1:
                    if cameraType == CameraType.PylonWrapper:
                        camera = CamPylonWrapper(basler_dict_list[0])
                        bSucceed = True
                    elif cameraType == CameraType.PylonFreerun:
                        camera = CamPylonFreerun(basler_dict_list[0])
                        if camera.IsConnected():
                            bSucceed = True
                        else:
                            bSucceed = False
                else:
                    pass
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