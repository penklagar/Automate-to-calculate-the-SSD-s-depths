#!/usr/bin/env python
# coding: utf-8

# In[283]:


# using texture for segmentation
# scratch array single image segmentation

import matplotlib.pyplot as plt
from skimage import io


# In[284]:


import numpy as np
from skimage.filters import threshold_otsu
import cv2


# In[285]:


# use glob to import multiple images and load them
import glob


# In[310]:


#select the path
path = "test_images/imgs/*.*"
img_number = 1  #Start an iterator for image number.
#This number can be later added to output image file names.


# In[311]:


for file in glob.glob(path):
    print(file)     #just stop here to see all file names printed
    img = cv2.imread(file, 0)  #now, we can read each file since we have the full path



#Gabor filter

ksize=45
theta=np.pi/3
kernel = cv2.getGaborKernel((ksize, ksize), 1, theta, 75, 50, 0, ktype=cv2.CV_32F)

filtered_image = cv2.filter2D(img, cv2.CV_8UC3, kernel)
plt.imshow(filtered_image, cmap='gray')


# In[293]:


# Entropy filter
from skimage.filters.rank import entropy
from skimage.morphology import disk

entropy_img = entropy(img, disk(60))
plt.imshow(entropy_img)


# In[294]:


plt.hist(entropy_img.flat, bins=100, range=(0,5))


# In[295]:


thresh = threshold_otsu(entropy_img)


# In[296]:


# binarize the entropy image

binary = entropy_img <= thresh
plt.imshow(binary)


# In[297]:


#diameter measurement
image = binary
scale = 0.3 #microns/pixel (assumed, need to be changed)


# In[298]:


#Remove edge touching regions (if there is breaks in borders, this filter will remove it)
from skimage.segmentation import clear_border
edge_touching_removed = clear_border(image)
plt.imshow(edge_touching_removed, cmap='gray')


# In[299]:


# assigns the connected objects and labels
from skimage import measure, io, img_as_ubyte
label_image = measure.label(edge_touching_removed, connectivity=image.ndim)
plt.imshow(label_image)


# In[300]:


# to change the color if there are multiple connected objects in the image
from skimage.color import label2rgb, rgb2gray
image_label_overlay = label2rgb(label_image, image=image)


# In[301]:


plt.imsave("labeled/labeled_SSD.jpg", image_label_overlay)
plt.imshow(image_label_overlay)


# In[305]:


measured_image = image_label_overlay
cv2.imwrite("test_images/measured/measured_image"+str(img_number)+".jpg", measured_image)
img_number +=1


# In[306]:


props = measure.regionprops_table(label_image,image, properties =['label', 'area', 'equivalent_diameter'])


# In[307]:


import pandas as pd
df = pd.DataFrame(props)
print(df.head())


# In[308]:


#to delete small regions
df = df[df['area'] > 50]
print(df.head())


# In[309]:


df['equivalent_diameter_microns'] = df['equivalent_diameter']*(scale)
print(df.head())


# In[ ]:




