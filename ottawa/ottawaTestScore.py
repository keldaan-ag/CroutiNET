import os
import numpy as np
from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model
from keras.preprocessing import image
import csv
import math

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper

IMG_SIZE  = 224
INPUT_DIM = (IMG_SIZE, IMG_SIZE, 3)

baseDir = r"D:\Arnaud\data_croutinet\ottawa\data"
roadsDir = os.path.join(baseDir, "roads")
bestModel = os.path.join(baseDir, 'scoreNetworkNoSigmoid.h5')
scoreSave = os.path.join(baseDir,"scores2.csv")

imagesNames = [f for f in os.listdir(roadsDir)]

pictures = []

print("loading model")
model = load_model(bestModel)

i=0
a=0
b=0
print("loading pictures")
for name in imagesNames:
    a = np.floor(i*100/len(imagesNames))
    if a != b :
        print(str(int(a)) + "%")
        b = a
    pictures.append(image.img_to_array(image.load_img(os.path.join(roadsDir, name), target_size=(IMG_SIZE, IMG_SIZE))))
    i+=1

print("pictures as array")
pictures = np.array(pictures)

print("preprocess pictures")
pictures = preprocess_input(x=np.expand_dims(pictures.astype(float), axis=0))[0]

print("pictures values as float32")
pictures = pictures.astype('float32')

prediction = model.predict(pictures)

with open(scoreSave, 'w') as csvfileWriter:
    writer = csv.writer(csvfileWriter)
    for k in range(len(imagesNames)):
        csvfileWriter.write("{},{}\n".format(imagesNames[k], str(truncate(prediction[k,0],4))))
