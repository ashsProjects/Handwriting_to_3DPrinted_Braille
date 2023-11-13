import pandas as pd
import numpy as np
import os
import cv2
import subprocess
import ProcessImage
#import model

def run_java(word):
    java_file = 'replace.java'#replace with Java file
    command = ['java', java_file, str(word)]#Javac must be in PATH
    result = subprocess.run(command, capture_output=True, text=True)
    print(f'Java process: {result.stdout if result.stdout != "" else result.stderr}')

if __name__ == '__main__':
    ProcessImage.seperate_letters()
    
    #read in all letters from the IndividualLettes folder
    letters = ['a','b','c']
    folder = os.listdir('IndividualLetters')
    
    for file in folder:
        image = cv2.imread('IndividualLetters/'+file)
        #y_pred = model.predict(image)
        #letters.append(y_pred)
    
    word_to_print = ''.join(letters)
    
    #fork, exec, and wait for process
    run_java(word_to_print)
    
    #Clear folders: IndividualLetters, InputImage, ProcessedImage for next word
    for f_name in os.listdir(path='InputImage'):
        os.remove("InputImage/" + f_name)
    for f_name in os.listdir(path='IndividualLetters'):
        os.remove("IndividualLetters/" + f_name)
        
    print("Completed with no errors!")
    
