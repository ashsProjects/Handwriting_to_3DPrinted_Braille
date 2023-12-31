import numpy as np
import os
import cv2
import Process_Image
import Send_Gcode_to_Pi
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
    # labels = string.ascii_uppercase
    labels = 'ssssssssss'+string.ascii_uppercase+string.ascii_lowercase #s for filler
    index = np.argmax(prediction)
    letter = labels[index]
    
    try:
        letter = letter.lower()
    except:
        pass
    
    return letter

if __name__ == '__main__':
    print('Starting Main.py')
    Process_Image.seperate_letters()
    print('Finished seperating letters')
    
    #read in all letters from the IndividualLettes folder
    letters = []
    folder = sorted(os.listdir('IndividualLetters'), key=len)
    
    #load letter_classifier.h5 model to classify the letters
    model = load_model('letters_only_cnn.h5')
    
    for file in folder:
        image = reshape_image(file)
        y_pred = model.predict(image)
        letters.append(map_to_letter(y_pred))
    print(f'Letters classified: {letters}')
    print('Finished classifying all images to letters')
    
    #Pass in the word to print
    Print_STL.run(letters)
    print('Finshed creating STL file')
    
    #Use the combined stl file to convert it into gcode and print it
    Send_Gcode_to_Pi.main()
    
    #Clear folders: IndividualLetters, InputImage for next word
    for f_name in os.listdir(path='InputImage'):
        os.remove("InputImage/" + f_name)
    for f_name in os.listdir(path='IndividualLetters'):
        os.remove("IndividualLetters/" + f_name)
        
    print("Completed with no errors. Exiting")
    
