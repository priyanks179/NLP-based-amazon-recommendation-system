import cv2
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
#Display an image
def display_img(url):
    # we get the url of the apparel and download it
    response = requests.get(url)
    image_stream = BytesIO(response.content)
    image_stream.seek(0)
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    #cv2.imshow('image',img)
    # we will display it in notebook 
    plt.imshow(img)
    plt.waitforbuttonpress(0.2)
    
