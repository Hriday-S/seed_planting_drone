import cv2
import numpy as np
from djitellopy import Tello

tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()
row = 1
col = 6
currentImage = 0

def getColor(image):
    average_color_row = np.average(image, axis=0)
    average_color = np.average(average_color_row, axis=0)
    return average_color
def getGreenDifferential(rgb):
    return (abs(rgb[0]/rgb[1]) + abs(rgb[2]/rgb[1]))/2
def readRow(numCol):
    global currentImage
    for i in range(col):
        cv2.imwrite("t_read_img_differential{}.png".format(currentImage), frame_read.frame)
      
        average_color = getColor(frame_read.frame)
        greenDifferential = getGreenDifferential(average_color)
        print("Green differntial: " + str(greenDifferential))
        print(str(currentImage)+": " + str(average_color))
        tello.move_left(70)
        currentImage += 1
    tello.move_right(150)
tello.takeoff()
for i in range(row-1):
    readRow(col)
    tello.move_up(50)
readRow(col)
tello.land()

for i in range(row*col):
    print(i)


image_paths=['t_read_img_differential0.png','t_read_img_differential1.png','t_read_img_differential2.png','t_read_img_differential3.png','t_read_img_differential4.png','t_read_img_differential5.png']
# initialized a list of images
imgs = []

for i in range(len(image_paths)):
	imgs.append(cv2.imread(image_paths[i]))
	imgs[i]=cv2.resize(imgs[i],(0,0),fx=0.4,fy=0.4)
	# this is optional if your input images isn't too large
	# you don't need to scale down the image
	# in my case the input images are of dimensions 3000x1200
	# and due to this the resultant image won't fit the screen
	# scaling down the images
# showing the original pictures
cv2.imshow('0',imgs[0])
cv2.imshow('1',imgs[1])
cv2.imshow('2',imgs[2])
cv2.imshow('3',imgs[3])
cv2.imshow('4',imgs[4])
cv2.imshow('5',imgs[5])

stitchy=cv2.Stitcher.create()
(dummy,output)=stitchy.stitch(imgs)

if dummy != cv2.STITCHER_OK:
# checking if the stitching procedure is successful
# .stitch() function returns a true value if stitching is
# done successfully
	print("stitching ain't successful")
else:
	print('Your Panorama is ready!!!')

# final output
cv2.imshow('final result',output)

cv2.waitKey(0)

