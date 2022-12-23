from cgitb import text
from turtle import update
from CameraHelper import PylonImageConvert
from CameraHelper import CamPylonFreerun
from pypylon import pylon
import numpy as np
import tkinter
import cv2


class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):
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
        pass

    def test(self):
        pass


def update_image():
    global image
    if image is not None:
        img_temp = image.copy()
        image = None
        global tk_photo  # this line is a must

        # ---- transfer numpy array to tkinter photo data
        # tk_photo_Data = f'P5 {canvas_width} {canvas_height} 255 '.encode() + image.astype(np.uint8).tobytes()

        # ---- resize
        img_resize = cv2.resize(
            img_temp, dsize=(canvas_width, canvas_height), interpolation=interplation
        )
        # --- transfer numpy array to tkinter photo data
        tk_photo_Data = (
            ppm_header + cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB).tobytes()
        )

        # --- update image
        tk_photo = tkinter.PhotoImage(
            width=canvas_width, height=canvas_height, data=tk_photo_Data, format="PPM"
        )
        canvas.itemconfig(canvas_img, image=tk_photo)  # could not put here

        global canvas_frame_counter
        canvas_frame_counter += 1
        canvas.itemconfig(canvas_frame_counter_text, text=f"{canvas_frame_counter}")
    else:
        pass
    tkWindow.after(5, update)


def __add_circle(event):
    global canvas_spot
    canvas_spot = canvas.create_oval(400, 400, 410, 410, fill="blue")


def __LButton_DbClick__callback(event):
    global canvas_spot
    canvas_spot = canvas.create_oval(
        event.x, event.y, event.x + 10, event.y + 10, fill="blue"
    )


def __select(event):
    # self.canvas.find_closest()
    # self.canvas.find_withtag()
    # self.canvas.find_overlapping()
    # reference:Python Tkinter Canvas中的tag的使用, https://blog.csdn.net/weixin_41984221/article/details/110918899
    canvas.itemconfig(canvas_spot, fill="red")


def __unselect(event):
    canvas.itemconfig(canvas_spot, fill="blue")


def __move(event):
    canvas.coords(canvas_spot, 100, 100, 110, 110)


if __name__ == "__main__":
    frame_counter = 0
    cam = CamPylonFreerun()
    if cam.IsConnected():
        cam.start_grab_thread(SampleImageEventHandler)
        size_ratio = 0.2
        canvas_width = int(cam.width * size_ratio)
        canvas_height = int(cam.height * size_ratio)
    else:
        canvas_width = 960
        canvas_height = 960

    tkWindow = tkinter.Tk()
    tkWindow.geometry("+100+50")
    canvas = tkinter.Canvas(
        tkWindow, width=canvas_width, height=canvas_height, bg="gray"
    )
    canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)

    image = np.zeros([canvas_height, canvas_width, 3], dtype=np.uint8)

    # interplation = cv2.INTER_CUBIC # scale up use this line
    interplation = cv2.INTER_AREA  # scale down use this line
    img_resize = cv2.resize(
        image, dsize=(canvas_width, canvas_height), interpolation=interplation
    )
    ppm_header = f"P6 {canvas_width} {canvas_height} 255 ".encode()
    tk_photo_Data = ppm_header + cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB).tobytes()
    tk_photo = tkinter.PhotoImage(
        width=canvas_width, height=canvas_height, data=tk_photo_Data, format="PPM"
    )
    canvas_img = canvas.create_image(0, 0, image=tk_photo, anchor=tkinter.NW)
    canvas_spot = None

    canvas.bind_all("<Control-Key-0>", __add_circle, add=True)
    canvas.bind_all("<Control-Key-1>", __select, add=True)
    canvas.bind_all("<Control-Key-2>", __unselect, add=True)
    canvas.bind_all("<Control-Key-3>", __move, add=True)
    canvas.bind("<Double-Button-1>", __LButton_DbClick__callback, add=True)

    canvas.create_text(10, 10, text="canvas frame counter:", fill="red")
    canvas_frame_counter = 0
    canvas_frame_counter_text = canvas.create_text(20, 20, text="0", fill="red")
    if cam.IsConnected():
        update_image()
    tkWindow.mainloop()

    if cam.IsConnected():
        cam.Close()
