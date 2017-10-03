from findObject import * 
import time
import cv2

scaleFactor = 0.1 

t1 = time.time()
res, img = analyzeImage("img/other files/img2greens.jpg", scaleFactor, True)
print time.time() - t1
print res
cv2.imwrite("img/Hueimg/Test.png", img)


"""
fullSize = 0 

def loadImage(path, scaleFactor, returnSize=False):
  img = cv2.imread(path)
  local_fullsize = (img.shape[0], img.shape[1])
  resized = cv2.resize(img, (0,0), fx=scaleFactor, fy=scaleFactor)
  if returnSize:
    return resized, local_fullsize
  else:
    return resized
  

# load some images
img1, fullSize= loadImage("img/imgfirst.jpg", scaleFactor, True)
#img2 = loadImage("img/imgsecond.jpg",     scaleFactor )
#img3 = loadImage("img/img2greens.jpg",    scaleFactor )
#img4 = loadImage("img/imgbordtennis.jpg", scaleFactor )
#img5 = loadImage("img/imgbordtennis2.jpg",scaleFactor )
#img6 = loadImage("img/img50cm.png",       scaleFactor )
#img7 = loadImage("img/img45_deg.png",     scaleFactor )
# noisy shapes img
#img8 = cv2.imread("img/noisy_shapes.png")

images = [img1]#, img2, img3, img4, img5, img6, img7, img8]

print "Finding green objects"
outputs = []
analyze_times = []
for i in range(len(images)):
  print "Analyzing: image %d" %(i+1)
  ts = time.time()
  outputs.append(findObjects(images[i]))
  analyze_times.append(time.time() - ts)

print "Average analysis time: %f\n" %(sum(analyze_times)/len(analyze_times))

contours = []
contour_times = []
biggestObjects = []
for i in range(len(outputs)):
  print "Finding contours: image %d" %(i+1)
  ts = time.time()
  cnts, bigObject = findRectangles(outputs[i])
  contours.append(cnts)
  biggestObjects.append(bigObject)
  contour_times.append(time.time() - ts)

print "Average time finding contours: %f\n" %(sum(contour_times)/len(contour_times))

both_times = [a + b for a, b in zip(analyze_times, contour_times)]

print "Average total time: %f" %(sum(both_times)/len(both_times))

def makeResultObject(x, y, w, h, img_size, scaleFactor):
  centerX = (x/scaleFactor + (h/scaleFactor)/2)
  centerY = (y/scaleFactor + (w/scaleFactor)/2)
  lenA = centerY
  lenB = img_size[1] - lenA

  return Presult(b_h/scaleFactor, centerX, centerY, True, lenA, lenB)

print "\nShowing images"
for i in range(len(outputs)):
  print "image %d" %i
  if (len(contours[i]) > 0):
    cv2.drawContours(outputs[i], contours[i],-1,(0,0,255),3)
    cv2.drawContours(outputs[i], [biggestObjects[i]], -1, (0,255,0),3)
    print "The biggest rectangular object has following properties:"
    (b_x, b_y, b_w, b_h) = cv2.boundingRect(biggestObjects[i])
    res = makeResultObject(b_x, b_y, b_w, b_h, fullSize, scaleFactor) # Presult(b_w, b_h, b_x, b_y, False, , 2)
    print res
    #print "Position = (%d, %d)" %(b_x * 1.0/scaleFactor , b_y * 1.0/scaleFactor)
    #print "Width: %d" %(b_w * 1.0/scaleFactor)
    #print "Height: %d" %(b_h * 1.0/scaleFactor)
    #print
  else:
    #print "No valid contours found\n"
    res = Presult(0, 0, 0, False ,0, 0, 0)
    print res
  #cv2.imshow('result with valid contours', outputs[i])
  cv2.imwrite("img/{0}_output.png".format(i), outputs[i])
  #cv2.imshow('img', images[i])


  cv2.waitKey(0)
"""
