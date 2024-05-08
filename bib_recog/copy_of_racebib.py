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
    reader = easyocr.Reader(["en"])
    text = ""
    img = deskew(img)  # Deskew the image
    try:
        result = reader.readtext(img)

        # Clean and extract text
        for detection in result:
            pattern = re.compile(r"[^a-zA-Z0-9\s]")
            clean_text = re.sub(pattern, "", detection[1])
            if clean_text.isdigit():
                text = detection[1]
    except Exception as e:
        print("Error occurred:", e)
    return text


def scale_roi(x, y, w, h, image_shape, size=1.1):
    # Function to scale the ROI
    expansion_factor = size
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


def images(event, bibnumber):
    filenames = []
    current_directory = os.getcwd()

    # Assuming you have dynamic variables for the cascade file and input folder
    detected_texts = os.path.join(
        current_directory, "static", "gallery", event
    )
    if not os.path.exists(detected_texts):
            os.makedirs(detected_texts)
    detected_texts = os.path.join(detected_texts, 'detected_texts.dat')
    # Create the output file if it doesn't exist
    if not os.path.exists(detected_texts):
        with open(detected_texts, "w") as f:
            pass  # Create an empty file

    # Open the file for reading
    with open(detected_texts, "r") as f:
        # Iterate over each line in the file
        for line in f:
            # Split the line into its components (path, filename, texts)
            components = line.split(" ")

            detected = components[2].split(",")
            for txt in detected:
                txt = txt.replace("'","")
                txt = txt.replace("[","")
                txt = txt.replace("]","")
                if txt == '':
                    continue
                if txt.find(bibnumber) != -1 or bibnumber.find(txt) != -1:
                    filenames.append({"path": components[0], "filename": components[1]})
                    
    return filenames

def generate(event,photog,files):
    # Load the cascade
    # Get the current working directory
    current_directory = os.getcwd()

    # Assuming you have dynamic variables for the cascade file and input folder
    cascade_file_path = os.path.join(
        current_directory, "bib_recog", "cascade1.xml"
    )
    input_folder = os.path.join(
        current_directory, "static", "gallery", event,photog
    )
    cascade = cv2.CascadeClassifier(
        cascade_file_path
    )
    filenames = []
    texts = []
    output_file_path = "detected_texts.dat"  # Output file path
    text_output = os.path.join(
        current_directory, "static", "gallery", event, 'detected_texts.dat'
    )
    
    # Create the output file if it doesn't exist
    if not os.path.exists(output_file_path):
        with open(output_file_path, "w") as f:
            pass  # Create an empty file

    with open(text_output, "a") as f:
        for file in files:
            if file.filename.endswith(".jpg"):
                image_path = os.path.join(input_folder, file.filename)
                image = cv2.imread(image_path)
                if image is None:
                    continue

                # Convert the image to grayscale
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Detect objects in the image
                objects = cascade.detectMultiScale(
                    gray, scaleFactor=1.15, minNeighbors=7, minSize=(55, 50)
                )

                for x, y, w, h in objects:
                    if w < 100 or h < 100:
                        continue
                    new_x, new_y, new_w, new_h = scale_roi(x, y, w, h, gray.shape)
                    roi = gray[
                        new_y : new_y + new_h, new_x : new_x + new_w
                    ]  # Extract the region of interest
                    if new_y + new_h < gray.shape[0] - 100:
                        if new_x > 100 and new_x < gray.shape[1] - 100:
                            roi_image = image[new_y : new_y + new_h, new_x : new_x + new_w]
                            if roi_image.shape[0] > 0 and roi_image.shape[1] > 0:
                                text = easy(roi_image)  # Perform OCR
                                # text = "uhh"
                                print("text in file: " + file.filename + " " + text)
                                if len(text) == 1 or len(text) == 0:
                                    new_x, new_y, new_w, new_h = scale_roi(
                                        x, y, w, h, gray.shape, 1.5
                                    )
                                    scale = cv2.GaussianBlur(roi_image, (5, 5), 0)
                                    scale = cv2.Canny(scale, 90, 130)
                                    scale = cv2.GaussianBlur(scale, (5, 5), 0)
                                    scale = cv2.threshold(
                                        scale, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
                                    )[1]
                                    scale = cv2.resize(
                                        scale,
                                        None,
                                        fx=2,
                                        fy=2,
                                        interpolation=cv2.INTER_CUBIC,
                                    )
                                    # scale = cv2.threshold(scale, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                                    scale = cv2.erode(
                                        scale, (7, 7), iterations=2
                                    )  # for colored bg
                                    scale = cv2.morphologyEx(scale, cv2.MORPH_CLOSE, (7, 7))
                                    text = easy(scale)  # Perform OCR
                                if text == "":
                                    continue
                                texts.append(text)
                                texts_str = ",".join(texts)
            f.write(f"{event}\{photog} {file.filename} {texts_str}\n")
            texts = []
    return filenames