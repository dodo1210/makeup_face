import sys
import cv2
import time
from PIL import Image, ImageColor
from sklearn.cluster import KMeans
from statistics import mean, mode, median
import numpy as np

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

# Read the image
name = 'lamcome'
image = cv2.imread('base_raw/'+name+'.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.3,
    minNeighbors=3,
    minSize=(30, 30)
)

print("Found {0} Faces!".format(len(faces)))

count = 0
for (x, y, w, h) in faces:
    count+=1
    hexa = []
    integer = []

    roi_color = image[y+10:y-10 + h-10, x+10:x-10+ w-10]

    print("[INFO] Object found. Saving locally.")
    cv2.imwrite('base_faces/'+name+str(count)+'.jpg', roi_color)
    img = Image.open('base_faces/'+name+str(count)+'.jpg')

    for pixel in img.getdata():
        moment_hexa = []
        moment_hexa.append(int(rgb_to_hex((pixel[0], pixel[1], pixel[2])),16))
        moment_hexa.append(0)
        hexa.append(moment_hexa)
    all = []
    for h in hexa:
        all.append(h[0])
    #print(hex(int(str(median(all)).split('.')[0])).split('0x')[1])
    rgb = (ImageColor.getcolor('#'+hex(int(str(np.percentile(all,20)).split('.')[0])).split('0x')[1], "RGB"))
    print((rgb[0]*299+rgb[1]*587+rgb[2]*114)/1000)
    if ((rgb[0]*299+rgb[1]*587+rgb[2]*114)/1000)>64 and ((rgb[0]*299+rgb[1]*587+rgb[2]*114)/1000)<=96:
        print("1")
        print(hex(int(str(np.percentile(all,30)).split('.')[0])).split('0x')[1])
    elif ((rgb[0]*299+rgb[1]*587+rgb[2]*114)/1000)>96 and ((rgb[0]*299+rgb[1]*587+rgb[2]*114)/1000)<=128:
        print("2")
        print(hex(int(str(np.percentile(all,45)).split('.')[0])).split('0x')[1])
    elif ((rgb[0]*299+rgb[1]*587+rgb[2]*114)/1000)>128 and ((rgb[0]*299+rgb[1]*587+rgb[2]*114)/1000)<=160:
        print("3")
        print(hex(int(str(np.percentile(all,55)).split('.')[0])).split('0x')[1])
    elif ((rgb[0]*299+rgb[1]*587+rgb[2]*114)/1000)>160 and ((rgb[0]*299+rgb[1]*587+rgb[2]*114)/1000)<=192:
        print("4")
        print(hex(int(str(np.percentile(all,75)).split('.')[0])).split('0x')[1])
    elif ((rgb[0]*299+rgb[1]*587+rgb[2]*114)/1000)>32 and ((rgb[0]*299+rgb[1]*587+rgb[2]*114)/1000)<=64:
        print("5")
        print(hex(int(str(np.percentile(all,75)).split('.')[0])).split('0x')[1])
