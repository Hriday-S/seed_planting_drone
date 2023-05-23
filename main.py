import cv2
import numpy as np
from djitellopy import Tello
import datetime
import tkinter as tk
from tkinter import font
import threading
from PIL import Image, ImageTk

# Initialize Tello drone
tello = Tello()
tello.connect()
tello.streamon()




window = tk.Tk()

button_font = font.Font(size = 16)

scale = 100
forward = tk.Button(window, text = "FOWARD", width = 10, height = 5, font = button_font, command = lambda:tello.move_forward(scale))
forward.grid(row = 0, column = 2)

backward = tk.Button(window, text = "BACKWARD", width = 10, height = 5, font = button_font, command = lambda:tello.move_back(scale))
backward.grid(row = 2, column = 2)

left = tk.Button(window, text = "LEFT", width = 10, height = 5, font = button_font, command = lambda:tello.move_left(scale))
left.grid(row = 1, column = 1)

takeOff = tk.Button(window, text = "Take Off", width = 10, height = 5, font = button_font, command = tello.takeoff)
takeOff.grid(row = 1, column = 5)

land = tk.Button(window, text = "Land", width = 10, height = 5, font = button_font, command = tello.land)
land.grid(row = 2, column = 5)

right = tk.Button(window, text = "RIGHT", width = 10, height = 5, font = button_font, command = lambda:tello.move_right(scale))
right.grid(row = 1, column = 4)

up = tk.Button(window, text = "UP", width = 10, height = 5, font = button_font, command = lambda:tello.move_up(scale))
up.grid(row =0, column = 5)

down = tk.Button(window, text = "DOWN", width = 10, height = 5, font = button_font, command = lambda:tello.move_down(scale))
down.grid(row =3, column = 5)

battery = tk.Label(window, text = "Battery: {}%".format(tello.get_battery()))
battery.grid(row = 4, column = 5)

canvas = tk.Canvas(window, width = 960/2, height = 720/2)
canvas.grid(row = 5, column = 0)

scaleSlider = tk.Scale(window, from_=0, to=100)
scaleSlider.grid(row = 1, column = 6)

def update_video():
    while True:
        frame = cv2.resize(tello.get_frame_read().frame, (580, 360))
        framehsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        hue_channel = framehsv[:,:, 0]
        saturation_channel = framehsv[:,:, 1]
        value_channel = framehsv[:,:, 2]
        #35, 75
        hue_min = 35
        hue_max = 75

        value_min = 20
        value_max = 60


        mask = ((hue_channel < hue_max) & (hue_channel > hue_min)) | ((value_channel < value_max) & (value_channel > value_min))
        
        filtered_image = np.zeros_like(frame)
        filtered_image[mask] = frame[mask]
        
        image = Image.fromarray(filtered_image)
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0,0, anchor = tk.NW, image = photo)
        canvas.image = photo
        
video_thread = threading.Thread(target=update_video)
video_thread.daemon = True


video_thread.start()


window.mainloop()

telllo.streamoff()
tello.end()
