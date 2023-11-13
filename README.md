# Handwriting_to_3DPrinted_Braille
This is a project that takes in a handwritten word, parses it using a neural network to letters, and prints the
braille-equivalent 3D-printed word. This is done using a Raspberry Pi that coordinates the device used to upload the
image onto the Pi and a 3D printer.

# Directory/File Descriptions:
  /ProcessImage.py: The python file that will find the contours of letters in word and seperate them into individual files. It is set to produce images of size 28x28 right now; can change<br><br>
  /Main.py: The main file that coordinates everything. It processes the image, seperates letters, calls the model to classify them, and forks a process to the Java file<br><br>
  /replace.java: Need to be changed<br><br>
  /ArchivedImages: Where images are put after being processed. Useful for report<br><br>
  /ImagesForTesting: Where images to be testes are located; can be deleted<br><br>
  /IndividualLetters: This is where letters will be written to by the program after finding contours and seperating letters; will be emptied after each image is processed. Classifier model will read from this directory<br><br>
  /InputImages: This is where the program will read from to get the image to process and classify; will be emptied after 
      the image is processed, classified, and printed<br><br>
  /Resources.txt: All of the resources used for the project<br>
