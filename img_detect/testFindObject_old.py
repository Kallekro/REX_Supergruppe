
from findObject import * 
import time

scaleFactor = 0.1 
# load some images
img1 = cv2.resize(cv2.imread("img/imgfirst.jpg"), (0,0),       fx=scaleFactor, fy=scaleFactor)
img2 = cv2.resize(cv2.imread("img/imgsecond.jpg"), (0,0),      fx=scaleFactor, fy=scaleFactor)
img3 = cv2.resize(cv2.imread("img/img2greens.jpg"), (0,0),     fx=scaleFactor, fy=scaleFactor)
img4 = cv2.resize(cv2.imread("img/imgbordtennis.jpg"), (0,0),  fx=scaleFactor, fy=scaleFactor)
img5 = cv2.resize(cv2.imread("img/imgbordtennis2.jpg"), (0,0), fx=scaleFactor, fy=scaleFactor)
# noisy shapes img
img6 = cv2.imread("img/noisy_shapes.png")

images = [img1, img2, img3, img4, img5, img6]

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

print "\nShowing images"
for i in range(len(outputs)):
  print "image %d" %i
  if (len(contours[i]) > 0):
    cv2.drawContours(outputs[i], contours[i],-1,(0,0,255),3)
    cv2.drawContours(outputs[i], [biggestObjects[i]], -1, (0,255,0),3)
    print "The biggest rectangular object has following properties:"
    (b_x, b_y, b_w, b_h) = cv2.boundingRect(biggestObjects[i])
    print "Position = (%d, %d)" %(b_x * 1.0/scaleFactor , b_y * 1.0/scaleFactor)
    print "Width: %d" %(b_w * 1.0/scaleFactor)
    print "Height: %d" %(b_h * 1.0/scaleFactor)
    print
  else:
    print "No valid contours found\n"
  cv2.imshow('result with valid contours', outputs[i])
  cv2.imwrite("img/{0}_output.png".format(i), outputs[i])
  cv2.imshow('img', images[i])


  cv2.waitKey(0)
