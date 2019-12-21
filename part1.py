"""
This module parses the source image from the 1.png file
into independent objects, which are placed as masks in the masks directory.
For this:
1. Point the upper left corner and lower right corner in the original image
 with 2 clicks of the left mouse button to crop unnecessary fields. Press "a"
 and 2 times "Escape" to complete execution.
2. The cropped image is converted to binary.
3. The output binary image is written in 5.png for control.
 After that, we perform labeling using the label function.
4. The process of disassembling a marked image into disconnected objects
 is performed in cycles. Each figure is written to its own mask file.
 The zero file contains the background mask. All masks are located in 
 the masks directory next to the module.
© Vadim Stetsenko, 2019
 """
import cv2
import numpy as np
from scipy.ndimage import label,generate_binary_structure
import os

    #small class for setting ROI points
class CoordinateStore:
    def __init__(self):
        self.points=[]
    def select_point(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDBLCLK :
            cv2.circle(img,(x,y),3,(255,0,0),-1)
            self.points.append((x,y))
			
    #perform crop for our region and save the gray file as 4.png
def crop_and_store(frame,mouth_coordinates,name):  #frame this is what we will cut,mouth_coordinates array created by mouse clicks
    global mouth_roi   
    [x,y,w,h] = cv2.boundingRect(mouth_coordinates) #perform trimming a rectangular area
    mouth_roi = frame[y:y + h, x:x + w] #this is what we have after trimming
    h, w, channels = mouth_roi.shape
        # If the cropped region is very small, ignore this case.
    if h < 10 or w < 10:
                  return
    cv2.imwrite(name, mouth_roi)    
    

CoordinateStore1=CoordinateStore()  #create a new instance of the class

img=cv2.imread("1.png")

if (not(os.path.isdir('.\\masks'))):   #checking the existence of the masks folder and creating if necessary
    os.makedirs('.\\masks')
cv2.namedWindow('image')
cv2.setMouseCallback('image',CoordinateStore1.select_point) #callback function bundle
while(1):
    cv2.imshow('image',img)
    k=cv2.waitKey(20)&0xFF #low bit selection
    if k == 27:            #exit by pressing Esc
        break
    elif k == ord('a'):    #if "a" is pressed, then the pnts array is prepared 
        pnts=np.array([CoordinateStore1.points],np.float32) #and passed to the crop function. 
        crop_and_store(img, pnts, "4.png")	#The result is saved in the 4.png file

gray_image = cv2.cvtColor(mouth_roi, cv2.COLOR_BGR2GRAY)#translate our region to gray scale
ret, threshold_image = cv2.threshold(gray_image, 95, 255, 0)#image binarization with standard cv2 function

cv2.imwrite("5.png", threshold_image)	

img1=cv2.imread("5.png",0)
a=np.array(img1)
labeled_array, num_features = label(a)         #mark up the image objects and get their number
print(num_features)		
xmax,ymax = img1.shape
for n in range (0, num_features,1):        #create all masks
        labeled_array_mask=labeled_array.copy()
        for x in range(1,xmax,1):
                for y in range(1,ymax,1):
                    a1 = int(labeled_array_mask[x,y])                         
                    if a1 == n:
                         labeled_array_mask[x,y]=255   #define light gray to display a simple object
                    else:
                        labeled_array_mask[x,y]=0				
        l=np.array(labeled_array_mask,dtype='uint8')
        cv2.imwrite('.\masks\{}mask.png'.format(n), labeled_array_mask)#set the name of the mask file 
                                                                       #in accordance with the number 
																	   #of the object and write it
cv2.waitKey(0)																	   