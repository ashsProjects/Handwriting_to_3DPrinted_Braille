import cv2
import os
import random

def seperate_letters():
    #read the one image from Images folder
    try:
        image_path = os.listdir('InputImage')[0]
    except:
        print('There are no files in Images.')
    image = cv2.imread('InputImage/'+image_path, 0)
    image_copy = image.copy()

    #Apply Gaussian blur to reduce noise-Used ChatGPT to do this
    blurred_image = cv2.GaussianBlur(image, (5,5),0)

    #Adjust contrast and brightness
    processed_image = cv2.convertScaleAbs(blurred_image, alpha=1.5, beta=10)

    #color-inversion
    inverted_image = 255-processed_image
    inverted_image[inverted_image < 150] = 0
    
    # Find contours in the binary image
    contours, _ = cv2.findContours(inverted_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #Sort the contours based on x-values so the letters are in order
    sorted_contours = sorted(contours, key=lambda contour: cv2.boundingRect(contour)[0])
    
    #Use image copy instead of image so the contour lines are not printed
    padding = 5  # You can change this value

    for i, contour in enumerate(sorted_contours):
        # Filter out small contours that may be noise
        if cv2.contourArea(contour) > 200:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
            
            # Add padding to the bounding box
            x -= padding
            y -= padding
            w += 2 * padding
            h += 2 * padding

            # Ensure the bounding box stays within the image boundaries
            x = max(0, x)
            y = max(0, y)
            w = min(image_copy.shape[1] - x, w)
            h = min(image_copy.shape[0] - y, h)
            
            # Extract the letter from the original image with padding
            letter = image_copy[y:y+h, x:x+w]
            
            #resize the images to 25x25 so there are 500 features
            letter = cv2.resize(letter, (28,28))
            
            # Save the letter as a separate image
            cv2.imwrite(f"IndividualLetters/letter_{i}.png", letter)
    cv2.imwrite(f'ArchivedImages/image_with_contours{random.randint(1,1000)}.jpg', image)