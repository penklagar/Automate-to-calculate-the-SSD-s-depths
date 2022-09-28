from skimage import measure, io, img_as_ubyte
import matplotlib.pyplot as plt
from skimage.color import label2rgb, rgb2gray
import numpy as np
import cv2

# The input image.
image = img_as_ubyte(rgb2gray(io.imread("images/1_2.jpg")))
image = cv2.imread("images/1_2.jpg")
plt.imshow(image, cmap='gray')
scale = 0.6 #microns/pixel

#plt.hist(blue_channel.flat, bins=100, range=(0,150))  #.flat returns the flattened numpy array (1D)

from skimage.filters import threshold_otsu
threshold = threshold_otsu(image)

#Generate thresholded image
thresholded_img = image < threshold
plt.imshow(thresholded_img)

#Remove edge touching regions
from skimage.segmentation import clear_border
edge_touching_removed = clear_border(thresholded_img)
plt.imshow(edge_touching_removed)

#Label connected regions of an integer array using measure.label
#Labels each connected entity as one object
#Connectivity = Maximum number of orthogonal hops to consider a pixel/voxel as a neighbor. 
#If None, a full connectivity of input.ndim is used, number of dimensions of the image
#For 2D image it would be 2

label_image = measure.label(edge_touching_removed, connectivity=image.ndim)

plt.imshow(label_image)
#Return an RGB image where color-coded labels are painted over the image.
#Using label2rgb

image_label_overlay = label2rgb(label_image, image=image)
plt.imshow(image_label_overlay)

plt.imsave("labeled_cast_iron.jpg", image_label_overlay) 

#################################################
#Calculate properties
#Using regionprops or regionprops_table
all_props=measure.regionprops(label_image, image)
#Can print various parameters for all objects
for prop in all_props:
    print('Label: {} Area: {}'.format(prop.label, prop.area))

#Compute image properties and return them as a pandas-compatible table.
#Available regionprops: area, bbox, centroid, convex_area, coords, eccentricity,
# equivalent diameter, euler number, label, intensity image, major axis length, 
#max intensity, mean intensity, moments, orientation, perimeter, solidity, and many more

props = measure.regionprops_table(label_image, image, 
                          properties=['label',
                                      'area', 'equivalent_diameter',
                                      'mean_intensity', 'solidity'])

import pandas as pd
df = pd.DataFrame(props)
print(df.head())

#To delete small regions...
df = df[df['area'] > 50]
print(df.head())

#######################################################
#Convert to micron scale
df['area_sq_microns'] = df['area'] * (scale**2)
df['equivalent_diameter_microns'] = df['equivalent_diameter'] * (scale)
print(df.head())

df.to_csv('data/cast_iron_measurements.csv')
