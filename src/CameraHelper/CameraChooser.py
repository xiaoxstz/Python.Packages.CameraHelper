# cython: language_level=3
from .CamPylonWrapper import CamPylonWrapper
from .CamCommonWrapper import CamCommonWrapper
from .CameraType import CameraType
from .CamPylonFreerun import CamPylonFreerun

from pypylon import pylon # pip install pypylon
from pypylon import genicam

class CameraChooser:
    def Choose(cameraType:CameraType,camera_info:dict,camera_obj=None):
        bSucceed = False
        camera = None
        try:
            if cameraType == CameraType.CommonWrapper:
                camera = CamCommonWrapper(camera_info)
                bSucceed = True
            elif cameraType == CameraType.PylonWrapper or cameraType == CameraType.PylonFreerun:
                if camera_obj  is None:
                    # Get the transport layer factory.
                    tlFactory = pylon.TlFactory.GetInstance()
                    # Get all attached devices and exit application if no device is found.
                    devices = tlFactory.EnumerateDevices()
                    for device in devices:
                        serial_no = device.GetSerialNumber()
                        if camera_info["Serial Number"] == serial_no:
                            camera_obj = device

                obj = pylon.InstantCamera( pylon.TlFactory.GetInstance().CreateDevice(camera_obj) )            
                if cameraType == CameraType.PylonWrapper:
                    camera = CamPylonWrapper(obj)
                else:
                    camera = CamPylonFreerun(obj)
            else: 
                pass
            
            if camera is not None and camera.IsConnected():
                bSucceed = True
            else:
                bSucceed = False
        except RuntimeError as ex:
            print(ex)
            bSucceed = False
        except Exception as ex:
            print(ex)
            bSucceed = False
        
        return (bSucceed,camera)