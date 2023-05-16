import cv2
import numpy as np
from djitellopy import Tello
import datetime

tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

 
def getColor(image):
    average_color_row = np.average(image, axis=0)
    average_color = np.average(average_color_row, axis=0)
    return average_color
def getGreenDifferential(rgb):
    return (abs(rgb[0]/rgb[1]) + abs(rgb[2]/rgb[1]))/2


image = frame_read.frame

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# Define lower and upper range of green color in HSV
lower_green = np.array([40, 100, 70])
upper_green = np.array([75, 255, 255])
# Create a mask of pixels that fall within the range of the green color
green_mask = cv2.inRange(hsv, lower_green, upper_green)
# The mask is applied on the original image
green_image = cv2.bitwise_and(image, image, mask=green_mask)
   
# Save the resulting image
cv2.imwrite("Filtration{}.png".format(datetime.datetime.now()), green_image)


        
average_color = getColor(frame_read.frame)
greenDifferential = getGreenDifferential(average_color)
print("Green differntial: " + str(greenDifferential))







