"""
This program has been tested with:
* the camera "HIKVISION E14a" with the module "CommonWrapper"
* Basler camera with the module "PylonFreerun"
* Basler camera with the module "PylonWrapper"
"""
from CameraHelper import CameraChooser # version tested: 0.0.7~0.0.9
from CameraHelper import CameraType
import tkinter
import cv2
import numpy as np
from pypylon import pylon

#region image grabbed callback
def grabbed_callback(frame):
    global image
    image = frame

def pylon_grabbed_callback(grabResult):
    """this function should not put the code that costs too much time"""

    global frame_counter
    # print("OnImageGrabbed start")
    global image
    if grabResult.GrabSucceeded():
        # image = PylonImageConvert.convert(grabResult).GetArray() # convert, not necessary if the image format is set well
        image = grabResult.GetArray()
        frame_counter += 1
    else:
        pass
    # canvas.itemconfig(canvas_img, image=image) # could not put here
    # print("OnImageGrabbed end")

class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):
        pylon_grabbed_callback(grabResult)

#endregion

def get_tk_photo(image:np.ndarray):
    img_resize = cv2.resize(image, dsize=(canvas_width, canvas_height), interpolation=interplation) 
    if tranformation is None:
        tk_photo_Data = ppm_header + img_resize.tobytes()
    else:
        tk_photo_Data = ppm_header + cv2.cvtColor(img_resize, tranformation).tobytes()
    tk_photo =  tkinter.PhotoImage(width=canvas_width, height=canvas_height, data=tk_photo_Data, format='PPM')
    return tk_photo

def update():
    global image
    if image is not None:
        img_temp = image.copy()
        global canvas_img,tk_photo
        tk_photo = get_tk_photo(img_temp)
        # canvas_img = canvas.create_image(0, 0, image = tk_photo, anchor = tkinter.NW)
        canvas.itemconfig(canvas_img,image=tk_photo)
    tkWindow.after(10,update)


if __name__ == '__main__':
    frame_counter = 0
    camType = CameraType.PylonFreerun
    ret, cam = CameraChooser.Choose(camType)
    size_ratio = 0.5
    if cam.IsConnected():
        canvas_width = int(cam.width * size_ratio)
        canvas_height = int(cam.height * size_ratio)
    else:
        canvas_width = 960
        canvas_height = 960
    tkWindow = tkinter.Tk()
    canvas = tkinter.Canvas(tkWindow,width = canvas_width, height = canvas_height,bg='gray')
    canvas.pack()

    image = np.zeros([canvas_height,canvas_width,3],dtype=np.uint8)

    ppm_header = f'P6 {canvas_width} {canvas_height} 255 '.encode()

    if size_ratio > 1:
        interplation = cv2.INTER_CUBIC   # best for zoom in
    else:
        interplation = cv2.INTER_AREA    # best for zoom out

    tranformation = None
    if camType == CameraType.PylonFreerun or camType == CameraType.PylonWrapper:
        tranformation = cv2.COLOR_BGR2RGB # swap red and green channel
    else:
        tranformation = None 

    tk_photo = get_tk_photo(image)
    canvas_img = canvas.create_image(0, 0, image = tk_photo, anchor = tkinter.NW)

    if cam.IsConnected():
        if camType == CameraType.PylonFreerun:
            cam.start_grab_thread(SampleImageEventHandler)
        elif camType == CameraType.PylonWrapper:
            cam.start_grab_thread(pylon_grabbed_callback)
        else:
            cam.start_grab_thread(grabbed_callback)
        update()
    tkWindow.mainloop()

    cam.Close()