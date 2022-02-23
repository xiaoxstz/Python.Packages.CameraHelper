from pygrabber.dshow_graph import FilterGraph

from pypylon import pylon # pip install pypylon
from pypylon import genicam
class CameraDetector:   
    def find_all_cameras():
        cam_dict_list = []
        cam_obj_list = []

        basler_dict_list,balser_obj_list = CameraDetector.find_basler_cams()
        directshow_dict_list,directshow_obj_list = CameraDetector.find_directshow_cams()

        cam_dict_list = basler_dict_list + directshow_dict_list
        cam_obj_list = balser_obj_list + directshow_obj_list
        return cam_dict_list, cam_obj_list

    def find_directshow_cams():
        cam_dict_list = []
        cam_obj_list = []
        graph = FilterGraph()
        devices = graph.get_input_devices()
        for i in range(len(devices)):
            cam_dict = dict()
            cam_dict['index'] = i
            cam_dict['TL Type'] = "Directshow"
            cam_dict['Model Name'] = devices[i]
            cam_dict_list.append(cam_dict)
        return cam_dict_list,cam_obj_list

    def find_basler_cams():
        cam_dict_list = []
        cam_obj_list = []
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

                cam_dict_list.append(cam_dict)
                cam_obj_list.append(cam)
            
        except genicam.GenericException as e:
            # Error handling.
            print("An exception occurred.", e.args[0])
        return cam_dict_list , cam_obj_list

if __name__ == '__main__':
    cam_dict_list,cam_obj_list = CameraDetector.find_all_cameras()
    for cam_dict in cam_dict_list:
        print("camera:")
        for key,value in cam_dict.items():
            print(f"{key}:{value}")