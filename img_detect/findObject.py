from __future__ import division
import cv2
import numpy as np

class Presult (object):
  def __init__(self, height, posX, posY, isBox, lenA, lenB):
    self.height = height
    self.posX = posX
    self.posY = posY
    self.isBox = isBox
    self.lenA = lenA
    self.lenB = lenB
    
  def __str__(self):  
    res = ""
    res += "Height: %d\n" %self.height
    res += "Position: (%d, %d)\n" %(self.posX, self.posY)
    res += "Found box?: %r\n" %self.isBox
    res += "Length A: %d\n" %self.lenA
    res += "Length B: %d\n" %self.lenB
    return res

def findObjects(img):
  # convert img to hsv
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

  # find the lower and upper values for the green color in the mask
  puregreen = np.uint8([[[0,255,0]]])
  hsv_green = cv2.cvtColor(puregreen, cv2.COLOR_BGR2HSV)
  lower_green = [hsv_green[0,0,0] - 30, 45, 45] 
  upper_green = [hsv_green[0,0,0] + 30, 255, 255]
  # get mask
  green_mask = cv2.inRange(hsv, np.array(lower_green), np.array(upper_green))

  # extract hue, value and saturation
  h = hsv[:,:,0]/255.0
  s = hsv[:,:,1]/255.0
  v = hsv[:,:,2]/255.0
  

  # parameters for green color
  T1, T2, T3 = 0.25, 0.2, 0.1
  # find the specified greens
  green = ((abs(h - 0.33) < T1) & (v > T2) & (s > T3)).astype(float)

  # apply mask
  masked = cv2.bitwise_and(green,green,mask=green_mask)

  # erode image
  eroded = cv2.erode(masked, np.ones((15,15)))
  
  # dilate image
  result = cv2.dilate(eroded, np.ones((20, 20)))

  # set hue, value and saturation to the found values 
  # when we do this the image is effectively a rgb img not hsv, and it is greyscaled (actually just black and white) 
  # it is however not in the greyscale format (Dx, Dy) but rgb/hsv format (Dx, Dy, 3)
  hsv[:,:,0] = result*255.0
  hsv[:,:,1] = result*255.0
  hsv[:,:,2] = result*255.0
  
  return hsv

def findRectangles(img):
  def detectRectangle(cntAppr):
    (b_x, b_y, b_w, b_h) = cv2.boundingRect(cntAppr)

    aspect_ratio = b_w / b_h;
    # if aspect ratio is appr 1 shape is square (and we're looking for rects)
    #if aspect_ratio >= 0.95 and aspect_ratio <= 1.05:
    #  return False
    
    b_area = b_w*b_h
    # if the contour area fills over around 60% of the bounding rect it is probably a weird-shaped-but-still-rectangle  
    if b_area - cv2.contourArea(cntAppr) < b_area * 0.4:
      return True 
    
    elif len(cntAppr) != 4:
      return False
    return True

  # convert img to grayscale
  # we know that this img is black and white already, so no need to threshold before
  # we do however need to convert to grayscale because the format is different
  gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
  # find contours in image
  contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]

  # validRectContours = []
  # contourAreas = []
  # # remove contours that are not rectangle-ish shaped
  # for i in range(len(contours)):
  #   # instead of using the real contour we use an approximation with much fewer points
  #   # number of points in approximation is 4 if the shape is rect-shaped
  #   contours[i] = cv2.approxPolyDP(contours[i], 0.05*cv2.arcLength(contours[i], True), True)
  #   if (detectRectangle(contours[i])):
  #     validRectContours.append(contours[i])
  #     # store area to use in average contour size
  #     contourAreas.append(cv2.contourArea(contours[i]))

  # if len(validRectContours) == 0:
  #   # No valid contours found
  #   return [], None

  # validContours = []
  # # Remove the found contours that are smaller than 1/7 of the largest contour found
  # biggestObject = validRectContours[0] 
  # maxArea = max(contourAreas)
  # for i in range(len(contourAreas)):
  #   if maxArea - contourAreas[i] < maxArea * 0.7 and contourAreas[i] > 600:
  #     validContours.append(validRectContours[i])
  #   if maxArea == contourAreas[i]:
  #     biggestObject = validRectContours[i]

  #return validContours, biggestObject
  return contours, contours[0]


def loadImage(path, scaleFactor, returnSize=False):
  img = cv2.imread(path)
  local_fullsize = (img.shape[0], img.shape[1])
  resized = cv2.resize(img, (0,0), fx=scaleFactor, fy=scaleFactor)
  if returnSize:
    return resized, local_fullsize
  else:
    return resized

def makeResultObject(x, y, w, h, img_size, scaleFactor):
  centerX = (x/scaleFactor + (h/scaleFactor)/2)
  centerY = (y/scaleFactor + (w/scaleFactor)/2)
  lenA = centerX
  lenB = img_size[1] - lenA

  return Presult(h/scaleFactor, centerX, centerY, True, lenA, lenB)

def analyzeImage(path, scaleFactor, extraStuff=False):
  img, size = loadImage(path, scaleFactor, True)
  hsv_img = findObjects(img)
  valid_cnts, biggestCnt = findRectangles(hsv_img)
  if len(valid_cnts) > 0:
    (b_x, b_y, b_w, b_h) = cv2.boundingRect(biggestCnt)  
    res = makeResultObject(b_x, b_y, b_w, b_h, size, scaleFactor)
  else:
    res = Presult(0,0,0,False,0,0) #makeResultObject(0,0,0,0,[0,0],1)
  if extraStuff:  
    if len(valid_cnts) > 0:
      cv2.drawContours(hsv_img, valid_cnts, -1, (0,0,255), 3)
      cv2.drawContours(hsv_img, [biggestCnt], -1, (0,255,0), 3)
    return res, hsv_img
  else:
    return res


