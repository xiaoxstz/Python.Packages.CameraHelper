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
    global __imgShown # this line is a must
    __PIL_Img = PIL.Image.fromarray(image)
    __imgShown = PIL.ImageTk.PhotoImage(image = __PIL_Img)
    canvas.itemconfig(canvas_img, image=__imgShown) # could not put here
    tkWindow.after(10,update)

if __name__ == '__main__':
    cam = CamPylonFreerun(SampleImageEventHandler)
    size_ratio = 0.3
    canvas_width = int(cam.width * size_ratio) 
    canvas_height = int(cam.height * size_ratio)
    # canvas_width = 600
    # canvas_height = 600
    
    tkWindow = tkinter.Tk()
    canvas = tkinter.Canvas(tkWindow, width = canvas_width, height = canvas_height,bg='gray')
    canvas.pack(fill=tkinter.BOTH,expand=tkinter.YES)

    image = np.zeros([cam.height,cam.width,3],dtype=np.uint8)    
    __PIL_Img = PIL.Image.fromarray(image)
    __imgShown = PIL.ImageTk.PhotoImage(image = __PIL_Img)
    canvas_img = canvas.create_image(0, 0, image = __imgShown, anchor = tkinter.NW)

    update()
    tkWindow.mainloop()



