import numpy as np
import os
import cv2
import subprocess
import ProcessImage
import string
import Print_STL
import tensorflow as tf
from keras.models import load_model
    
def reshape_image(image_path):
    img = cv2.imread('IndividualLetters/'+image_path, cv2.IMREAD_GRAYSCALE)
    img_resized = cv2.resize(img, (28, 28))
    img_array = np.expand_dims(img_resized, axis=-1)
    img_array = img_array / 255.0
    img_array = np.reshape(img_array, (1,28,28,1))
    return img_array

def map_to_letter(prediction):
    labels = string.digits+string.ascii_lowercase+string.ascii_uppercase
    index = np.argmax(prediction)
    letter = labels[index]
    return letter

if __name__ == '__main__':
    ProcessImage.seperate_letters()
    
    #read in all letters from the IndividualLettes folder
    letters = []
    folder = os.listdir('IndividualLetters')
    
    #load letter_classifier.h5 model to classify the letters
    model = load_model('letter_classifier.h5')
    
    for file in folder:
        image = reshape_image(file)
        y_pred = model.predict(image)
        letters.append(map_to_letter(y_pred))
    
    #Pass in the word to print
    Print_STL.run(letters)
    
    #Clear folders: IndividualLetters, InputImage, ProcessedImage for next word
    for f_name in os.listdir(path='InputImage'):
        os.remove("InputImage/" + f_name)
    for f_name in os.listdir(path='IndividualLetters'):
        os.remove("IndividualLetters/" + f_name)
    for f_name in os.listdir(path='CombinedSTL'):
        os.remove("CombinedSTL/" + f_name)
        
    print("Completed with no errors!")
    
