"""
This program has been tested on:
* the camera "HIKVISION E14a" with the module "CommonWrapper"
* Basler camera with the module "PylonFreerun"
"""
from CameraHelper import CameraChooser # version >= 0.0.7
from CameraHelper import CameraType
from TKCanvasPainter import SpotPainter
import tkinter
import cv2
import numpy as np
from pypylon import pylon

def grabbed_callback(frame):
    global image
    image = frame

def update():
    global image
    if image is not None:
        img_temp = image.copy()
        global canvas_img,tk_photo
        image = None
        img_resize = cv2.resize(img_temp, dsize=(canvas_width, canvas_height), interpolation=interplation) 
        if tranformation is None:
            tk_photo_Data = ppm_header + img_resize.tobytes()
        else:
            tk_photo_Data = ppm_header + cv2.cvtColor(img_resize, tranformation).tobytes()
        tk_photo =  tkinter.PhotoImage(width=canvas_width, height=canvas_height, data=tk_photo_Data, format='PPM')
        # canvas_img = canvas.create_image(0, 0, image = tk_photo, anchor = tkinter.NW)
        canvas.itemconfig(canvas_img,image=tk_photo)
    tkWindow.after(10,update)

class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):
        """this function should not put the code that costs too much time"""
        
        global frame_counter
        # print("OnImageGrabbed start")
        global image
        if grabResult.GrabSucceeded():
            # image = PylonImageConvert.convert(grabResult).GetArray() # convert, not necessary if the image format is set well
            image = grabResult.GetArray()
            frame_counter +=1
        else:
            pass
        # canvas.itemconfig(canvas_img, image=image) # could not put here
        # print("OnImageGrabbed end")
        pass


if __name__ == '__main__':
    frame_counter = 0
    camType = CameraType.PylonFreerun
    ret, cam = CameraChooser.Choose(camType)
    size_ratio = 0.5
    canvas_width = int(cam.width * size_ratio)
    canvas_height = int(cam.height * size_ratio)
    tkWindow = tkinter.Tk()
    canvas = tkinter.Canvas(tkWindow,width = canvas_width, height = canvas_height,bg='gray')
    canvas.pack()

    spot_painter = SpotPainter(10,"red","blue")
    spot_painter.bind2Canvas(canvas)

    image = np.zeros([cam.height,cam.width,3],dtype=np.uint8)   

    # interplation = cv2.INTER_CUBIC # scale up use this line
    interplation = cv2.INTER_AREA    # scale down use this line
    img_resize = cv2.resize(image, dsize=(canvas_width, canvas_height), interpolation=interplation) 
    ppm_header = f'P6 {canvas_width} {canvas_height} 255 '.encode()

    tranformation = None
    if camType == CameraType.PylonFreerun or camType == CameraType.PylonWrapper:
        tranformation = cv2.COLOR_BGR2RGB # swap red and green channel
    else:
        tranformation = None 

    if tranformation is None:
        tk_photo_Data = ppm_header + img_resize.tobytes()
    else:
        tk_photo_Data = ppm_header + cv2.cvtColor(img_resize, tranformation).tobytes()
    tk_photo =  tkinter.PhotoImage(width=canvas_width, height=canvas_height, data=tk_photo_Data, format='PPM')
    canvas_img = canvas.create_image(0, 0, image = tk_photo, anchor = tkinter.NW)

    if camType == camType.PylonFreerun:
        cam.start_grab_thread(SampleImageEventHandler)
    else:
        cam.start_grab_thread(grabbed_callback)
    update()
    tkWindow.mainloop()

    cam.Close()