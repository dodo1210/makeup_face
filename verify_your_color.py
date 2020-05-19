import sys
import cv2
import time
from PIL import Image, ImageColor
from sklearn.cluster import KMeans
from statistics import mean, mode, median
import numpy as np
import pandas as pd

data = pd.read_csv("base.csv")

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

# Insert image
name = 'davi'
image = cv2.imread('base_raw/'+name+'.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#Identify face
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.3,
    minNeighbors=3,
    minSize=(30, 30)
)

#Get number faces in picture
print("Found {0} Faces!".format(len(faces)))

count = 0
color = []
for (x, y, w, h) in faces:
    #cut face
    count+=1
    hexa = []
    integer = []

    roi_color = image[y+10:y-10 + h-10, x+10:x-10+ w-10]

    print("[INFO] Object found. Saving locally.")
    #save face
    cv2.imwrite('base_faces/'+name+str(count)+'.jpg', roi_color)
    img = Image.open('base_faces/'+name+str(count)+'.jpg')

    #get color
    for pixel in img.getdata():
        moment_hexa = []
        moment_hexa.append(int(rgb_to_hex((pixel[0], pixel[1], pixel[2])),16))
        moment_hexa.append(0)
        hexa.append(moment_hexa)
    all = []
    #convert color and identify if color is clear or dark
    for h in hexa:
        all.append(h[0])
    rgb = (ImageColor.getcolor('#'+hex(int(str(np.percentile(all,20)).split('.')[0])).split('0x')[1], "RGB"))
    light_color = ((rgb[0]*299+rgb[1]*587+rgb[2]*114)/1000)

    #compare color of picture with color of base
    get = 0
    count = 0
    mininum = 256
    for d in data['Color']:
        light_rgb = ImageColor.getcolor('#'+str(d), "RGB")
        light_data = ((light_rgb[0]*299+light_rgb[1]*587+light_rgb[2]*114)/1000)
        diference = light_color - light_data
        if diference<0:
            diference=diference*-1          
        if diference < mininum:
            get = count
            mininum = diference
        count+=1
    print("Sua base eh:"+data['Base'][get])

    