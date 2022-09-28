from skimage import measure, io, img_as_ubyte
import matplotlib.pyplot as plt
from skimage.color import label2rgb, rgb2gray
import numpy as np
import cv2
import matplotlib as mpl #for macos
mpl.use('macOsX') #for macos


# The input image.
image = img_as_ubyte(rgb2gray(io.imread("images/1_1.jpg")))
image = cv2.imread("images/1_1.jpg")
plt.imshow(image, cmap='gray')

scale = 0.6 #microns/pixel

plt.hist(image.flat, bins=100, range=(0, 255))

from skimage.filters import threshold_otsu
threshold = threshold_otsu(image)

#Generate thresholded image
thresholded_img = image < threshold
plt.imshow(thresholded_img, cmap ='gray')

#Remove edge touching regions
#from skimage.segmentation import clear_border
#edge_touching_removed = clear_border(thresholded_img)
#plt.imshow(edge_touching_removed)