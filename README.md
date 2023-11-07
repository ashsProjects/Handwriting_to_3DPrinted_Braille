# Handwriting_to_3DPrinted_Braille
Description:
  This is a project that takes in a handwritten word, parses it using a neural network to letters, and prints the
  braille-equivalent 3D-printed word. This is done using a Raspberry Pi that coordinates the device used to upload the
  image onto the Pi and a 3D printer.

Directory/File Descriptions:
  /ArchivedImages: Where images are put after being processed. Useful for report
  /ImgaesForTesting: Where images to be testes are located; can be deleted
  /IndividualLetters: This is where letters will be written to by the program after finding contours and seperating letters;
      will be emptied after each image is processed. Classifier model will read from this directory
  /InputImages: This is where the program will read from to get the image to process and classify; will be emptied after 
      the image is processed, classified, and printed
  /Resources.txt: All of the resources used for the project
