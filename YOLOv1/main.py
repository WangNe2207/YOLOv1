import tensorflow as tf
import os
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

VALID = 200
TRAIN = 2000
TEST =  100

classesNum = {'dog': 0, 'cat': 1}
def convertFunction(folder, name, file):
    path = folder + '/' + name
    path = os.path.normpath(path)
    tree = ET.parse(path)
    root = tree.getroot()

    file.write(path.replace('xml', 'png'))
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        className = obj.find('name').text
        if className not in classesNum.keys() or int(difficult) == 1:
            continue

        #get bounding box
        box = ( int(obj.find('bndbox').find('xmin').text),
                int(obj.find('bndbox').find('ymin').text),
                int(obj.find('bndbox').find('xmax').text),
                int(obj.find('bndbox').find('ymax').text))

        id = list(classesNum.keys()).index(className)

        #write to file
        file.write(' ' + ','.join([str(a) for a in box]) + ',' + str(id))
    file.write('\n')

with open(os.path.join('%s.txt' % ('annotations')) , 'w') as f:
    for file in os.listdir('annotations'):
        if file.endswith('.xml'):
            convertFunction(folder = 'annotations', name=str(file), file=f)


train_datasets = []
with open(os.path.normpath('annotations.txt'), 'r') as f:
    train_datasets = f.readlines()

train_image = train_datasets[0:TRAIN]
valid_image = train_datasets[TRAIN:TRAIN + VALID]
test_image = train_datasets[TRAIN + VALID:TRAIN + VALID + TEST]

def annotationConverting(dataset):
    X, Y = [], []
    for item in dataset:
        item = item.replace("\n", "").split(" ")
        X.append(item[0])
        arr = []
        for i in range(1, len(item)):
            arr.append(item[i])
        Y.append(arr)
    return X,Y

X_train, Y_train = annotationConverting(train_image)
X_valid, Y_valid = annotationConverting(valid_image)
X_test, Y_test = annotationConverting(test_image)

print('folder: ',X_train[0])
print('folder: ',Y_train[0])
