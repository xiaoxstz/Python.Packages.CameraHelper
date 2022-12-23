# cython: language_level=3
from .CamPylonWrapper import CamPylonWrapper
from .CamCommonWrapper import CamCommonWrapper
from .CameraType import CameraType
from .CamPylonFreerun import CamPylonFreerun

from pypylon import pylon  # pip install pypylon


class CameraChooser:
    def Choose(cameraType: CameraType, camera_info: dict):
        bSucceed = False
        camera = None
        try:
            if cameraType == CameraType.CommonWrapper:
                camera = CamCommonWrapper(camera_info)
                bSucceed = True
            elif cameraType == CameraType.PylonWrapper or cameraType == CameraType.PylonFreerun:
                pylon_device_info = None

                # Get the transport layer factory.
                tlFactory = pylon.TlFactory.GetInstance()
                # Get all attached devices and exit application if no device is found.
                device_info_list = tlFactory.EnumerateDevices()
                for info in device_info_list:
                    serial_no = info.GetSerialNumber()
                    if camera_info["Serial Number"] == serial_no:
                        pylon_device_info = info

                if pylon_device_info is not None:
                    obj = pylon.InstantCamera(tlFactory.CreateDevice(pylon_device_info))
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

        return (bSucceed, camera)
