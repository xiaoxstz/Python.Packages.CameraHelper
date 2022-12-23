"""
This program has been tested on:
* the camera "HIKVISION E14a"
"""
from CameraHelper import CamCommonWrapper
import tkinter
import cv2
import numpy as np


def grabbed_callback(frame):
    global image
    image = frame


def update_image():
    global image
    if image is not None:
        img_temp = image.copy()
        global canvas_img, tk_photo
        image = None
        img_resize = cv2.resize(
            img_temp, dsize=(canvas_width, canvas_height), interpolation=interplation
        )
        if tranformation is None:
            tk_photo_Data = ppm_header + img_resize.tobytes()
        else:
            tk_photo_Data = (
                ppm_header + cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB).tobytes()
            )
        tk_photo = tkinter.PhotoImage(
            width=canvas_width, height=canvas_height, data=tk_photo_Data, format="PPM"
        )
        canvas.itemconfig(canvas_img, image=tk_photo)
    tkWindow.after(10, update)


if __name__ == "__main__":
    cam = CamCommonWrapper()
    if cam.IsConnected():
        size_ratio = 0.5
        canvas_width = int(cam.width * size_ratio)
        canvas_height = int(cam.height * size_ratio)
    else:
        canvas_width = 960
        canvas_height = 960
    tkWindow = tkinter.Tk()
    canvas = tkinter.Canvas(
        tkWindow, width=canvas_width, height=canvas_height, bg="gray"
    )
    canvas.pack()

    image = np.zeros([canvas_height, canvas_width, 3], dtype=np.uint8)

    tranformation = None
    # tranformation = cv2.COLOR_BGR2RGB

    # interplation = cv2.INTER_CUBIC # scale up use this line
    interplation = cv2.INTER_AREA  # scale down use this line
    img_resize = cv2.resize(
        image, dsize=(canvas_width, canvas_height), interpolation=interplation
    )
    ppm_header = f"P6 {canvas_width} {canvas_height} 255 ".encode()
    if tranformation is None:
        tk_photo_Data = ppm_header + img_resize.tobytes()
    else:
        tk_photo_Data = (
            ppm_header + cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB).tobytes()
        )
    tk_photo = tkinter.PhotoImage(
        width=canvas_width, height=canvas_height, data=tk_photo_Data, format="PPM"
    )
    canvas_img = canvas.create_image(0, 0, image=tk_photo, anchor=tkinter.NW)

    if cam.IsConnected():
        cam.start_grab_thread(grabbed_callback)
        update_image()

    tkWindow.mainloop()

    cam.Close()
