from pygrabber.dshow_graph import FilterGraph

from pypylon import pylon # pip install pypylon
from pypylon import genicam
class CameraDetector:
    def __init__(self) -> None:
        self.__cam_dict_list = []
    
    def find_cameras(self):
        self.__find_basler_cams()
        self.__find_directshow_cams()
    
    def get_cams(self):
        return self.__cam_dict_list

    def __find_directshow_cams(self):
        graph = FilterGraph()
        devices = graph.get_input_devices()
        for i in range(len(devices)):
            cam_dict = dict()
            cam_dict['index'] = i
            cam_dict['TL Type'] = "Directshow"
            cam_dict['Model Name'] = devices[i]
            self.__cam_dict_list.append(cam_dict)

    def __find_basler_cams(self):
        try:
            # Get the transport layer factory.
            tlFactory = pylon.TlFactory.GetInstance()

            # Get all attached devices and exit application if no device is found.
            devices = tlFactory.EnumerateDevices()
            if len(devices) == 0:
                raise pylon.RuntimeException("No camera present.")

            for cam in devices:
                cam_dict = dict()
                cam_dict["User Name"] = cam.GetUserDefinedName()
                cam_dict["Serial Number"] = cam.GetSerialNumber()
                cam_dict["Verdor"] = cam.GetVendorName()
                cam_dict["Model Name"] = cam.GetModelName()

                tl_type = cam.GetTLType()
                if tl_type == "U3V":
                    cam_dict["TL Type"] = "USB3"
                else:
                    cam_dict["TL Type"] = tl_type

                self.__cam_dict_list.append(cam_dict)   
        except genicam.GenericException as e:
            # Error handling.
            print("An exception occurred.", e.args[0])

if __name__ == '__main__':
    cam_detector = CameraDetector()
    cam_detector.find_cameras()
    cam_dict_list = cam_detector.get_cams()
    for cam_dict in cam_dict_list:
        print("camera:")
        for key,value in cam_dict.items():
            print(f"{key}:{value}")