from turtle import update
from CameraHelper import PylonImageConvert
from CameraHelper import CamPylonFreerun
from pypylon import pylon
import numpy as np
import tkinter
import PIL.Image, PIL.ImageTk

class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):
        """this function should not put the code that costs too much time"""
        # print("OnImageGrabbed start")
        global image
        img = PylonImageConvert.convert(grabResult)
        image = img.GetArray()
        # canvas.itemconfig(canvas_img, image=image) # could not put here
        # print("OnImageGrabbed end")
        pass

    def test(self):
        pass

def update():
    global image
    if image is not None:
        img_temp = image.copy()
        image = None
        global __imgShown # this line is a must
        __PIL_Img = PIL.Image.fromarray(img_temp).resize(
                (canvas.winfo_width(), canvas.winfo_height()),
                PIL.Image.ANTIALIAS)
        __imgShown = PIL.ImageTk.PhotoImage(image = __PIL_Img)
        canvas.itemconfig(canvas_img, image=__imgShown) # could not put here  
        image = None
    else:
        pass
    tkWindow.after(10,update)

if __name__ == '__main__':
    cam = CamPylonFreerun(SampleImageEventHandler)
    size_ratio = 0.2
    canvas_width = int(cam.width * size_ratio) 
    canvas_height = int(cam.height * size_ratio)
    
    tkWindow = tkinter.Tk()
    canvas = tkinter.Canvas(tkWindow, width = canvas_width, height = canvas_height,bg='gray')
    canvas.pack(fill=tkinter.BOTH,expand=tkinter.YES)

    image = np.zeros([cam.height,cam.width,3],dtype=np.uint8)    
    __PIL_Img = PIL.Image.fromarray(image).resize(
            (canvas.winfo_width(), canvas.winfo_height()),
            PIL.Image.ANTIALIAS)
    __imgShown = PIL.ImageTk.PhotoImage(image = __PIL_Img)
    canvas_img = canvas.create_image(0, 0, image = __imgShown, anchor = tkinter.NW)

    update()
    tkWindow.mainloop()



