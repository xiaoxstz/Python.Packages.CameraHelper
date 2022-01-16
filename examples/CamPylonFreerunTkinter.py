from cgitb import text
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
        global frame_counter
        # print("OnImageGrabbed start")
        global image
        img = PylonImageConvert.convert(grabResult)
        image = img.GetArray()
        frame_counter +=1
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

        global canvas_frame_counter
        canvas_frame_counter +=1
        canvas.itemconfig(canvas_frame_counter_text,text=f"{canvas_frame_counter}")
        image = None
    else:
        pass
    tkWindow.after(10,update)

def __add_circle(event):
    global canvas_spot
    canvas_spot = canvas.create_oval(400,400,410,410,fill="blue")

def __select(event):
    # self.canvas.find_closest()
    # self.canvas.find_withtag()
    # self.canvas.find_overlapping() 
    # reference:Python Tkinter Canvas中的tag的使用, https://blog.csdn.net/weixin_41984221/article/details/110918899
    canvas.itemconfig(canvas_spot,fill="red")

def __unselect(event):
    canvas.itemconfig(canvas_spot,fill="blue")

def __move(event):
    canvas.coords(canvas_spot,100,100,110,110)

if __name__ == '__main__':
    frame_counter = 0
    cam = CamPylonFreerun(SampleImageEventHandler)
    size_ratio = 0.2
    canvas_width = int(cam.width * size_ratio) 
    canvas_height = int(cam.height * size_ratio)
    
    tkWindow = tkinter.Tk()
    tkWindow.geometry('+100+50')
    canvas = tkinter.Canvas(tkWindow, width = canvas_width, height = canvas_height,bg='gray')
    canvas.pack(fill=tkinter.BOTH,expand=tkinter.YES)
    
    image = np.zeros([cam.height,cam.width,3],dtype=np.uint8)    
    __PIL_Img = PIL.Image.fromarray(image).resize(
            (canvas.winfo_width(), canvas.winfo_height()),
            PIL.Image.ANTIALIAS)
    __imgShown = PIL.ImageTk.PhotoImage(image = __PIL_Img)
    canvas_img = canvas.create_image(0, 0, image = __imgShown, anchor = tkinter.NW)
    canvas_spot = None

    canvas.bind_all("<Control-Key-0>", __add_circle,add=True)
    canvas.bind_all("<Control-Key-1>", __select,add=True)
    canvas.bind_all("<Control-Key-2>", __unselect,add=True)
    canvas.bind_all("<Control-Key-3>", __move,add=True)

    canvas.create_text(10,10,text="canvas frame counter:",fill="red")
    canvas_frame_counter = 0
    canvas_frame_counter_text = canvas.create_text(20,20,text="0",fill="red")
    update()
    tkWindow.mainloop()



