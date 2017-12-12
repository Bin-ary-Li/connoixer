import numpy as np
import os, os.path
from flask import jsonify, json
import resize


def readImageFrom(imageaddress):
    imagedir = resize.image_resize(imageaddress,114)
    X = np.array(imagedir, dtype = 'float32')
    return X


def imageProcessing(imageaddress):
    inputImage = readImageFrom(imageaddress)
    
    #type casting, and scaling
    inputImage = np.float32(inputImage)
    inputImage = inputImage/255.0

    #centering
    inputImage_mean = np.mean(inputImage)
    inputImage = np.subtract(inputImage, inputImage_mean)
    #normalization
    inputImage = inputImage/np.std(inputImage)
    return inputImage


def createJSON(imageaddress):
    np_image = imageProcessing(imageaddress)
    np_image = np.resize(np_image, [114,114,3])
    processed_image = np_image.tolist()
    image_dic = {}
    image_dic['input'] = processed_image
    imageList = []
    imageList.append(image_dic)
    instanceWrapper = {}
    instanceWrapper['instances'] = imageList
    return instanceWrapper
