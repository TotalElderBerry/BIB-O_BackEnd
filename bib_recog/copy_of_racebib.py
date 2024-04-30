import easyocr
import cv2
import os
import numpy as np
from PIL import Image
import re
from deskew import determine_skew
from skimage import io
from skimage.transform import rotate

def deskew(image):
    # Function to deskew the image
    angle = determine_skew(image)
    if angle is None:
        return image
    else:
        # Rotate the image to correct skew
        rotated = rotate(image, angle, resize=False) * 255
        return rotated.astype(np.uint8)

def easy(img):
    # Function to perform OCR using EasyOCR
    reader = easyocr.Reader(['en'])
    text = ""
    img = deskew(img)  # Deskew the image
    try:
        result = reader.readtext(img)

        # Clean and extract text
        for detection in result:
            pattern = re.compile(r'[^a-zA-Z0-9\s]')
            clean_text = re.sub(pattern, '', detection[1])
            if clean_text.isdigit():
                text = detection[1]
    except Exception as e:
        print("Error occurred:", e)
    return text

def scale_roi(x, y, w, h, image_shape):
    # Function to scale the ROI
    expansion_factor = 1.1
    new_x = int(x - (w * (expansion_factor - 1) / 2))
    new_y = int(y - (h * (expansion_factor - 1) / 2))
    new_w = int(w * expansion_factor)
    new_h = int(h * expansion_factor)
    # Ensure the new coordinates are within the image boundaries
    new_x = max(new_x, 0)
    new_y = max(new_y, 0)
    new_w = min(new_w, image_shape[1] - new_x)
    new_h = min(new_h, image_shape[0] - new_y)
    return new_x, new_y, new_w, new_h


def images(folder, bibnumber):
    # Load the cascade
    cascade = cv2.CascadeClassifier('C:/Users/PC/Desktop/BIB-O_BackEnd/bib_recog/cascade.xml')
    filenames = []
    # Folder paths
    input_folder = 'C:/Users/PC/Desktop/BIB-O_BackEnd/gallery/'+folder

    # Iterate through each file in the folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg"):
            # Read the input image
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)
            if image is None:
                continue

            # Convert the image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Detect objects in the image
            objects = cascade.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=7, minSize=(55, 50))

            for (x, y, w, h) in objects:
                if w < 100 or h < 100:
                    continue
                new_x, new_y, new_w, new_h = scale_roi(x, y, w, h, gray.shape)
                roi = gray[new_y:new_y+new_h, new_x:new_x+new_w]  # Extract the region of interest
                if new_y + new_h < gray.shape[0] - 100:
                    if new_x > 100 and new_x < gray.shape[1] - 100:
                        roi_image = image[new_y:new_y+new_h, new_x:new_x+new_w]
                        if roi_image.shape[0] > 0 and roi_image.shape[1] > 0:
                            text = easy(roi_image)  # Perform OCR
                            # text = "uhh"
                            if text and text.find(bibnumber) != -1 or bibnumber.find(text) != -1:
                                filenames.append(filename)
                                print(filename)
                                print(text)
                                    # cv2.rectangle(image, (new_x, new_y), (new_x+new_w, new_y+new_h), (255, 0, 0), 2)
                                    # cv2.putText(image, text, (new_x, new_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (123, 255, 123), 8)
                                    # output_path = os.path.join(output_folder, filename)
                                    # cv2.imwrite(output_path, image)
    
    return filenames
    # Display the result (if needed)
    # cv2.imshow("Result", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
