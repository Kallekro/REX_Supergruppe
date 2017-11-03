#What need to be changed in order for the exercise 6

# Landmarks. Their coordinates are in cm.
landmarks = [(0.0, 0.0), (0.0, 300.0), (400.0, 0.0), (400.0, 300.0)]

visitedLM = [False, False, False, False]
#It looks like the blue color cordinates is the most significant change between the green og the red box. Therefore green is less
# than 0.35 and red is above

if colourProb[0] <0.30:
    print 'The box is green'
else: 
    print 'The box is red'

if (objectType == 'vertical'):
    if colourProb[0] >0.30:
        lm = landmarks[1]
        lastSeenLM = 1
    else:
        lm = landmarks[2]
        lastSeenLM = 2
        
if (objectType == 'horizontal'):
    if colourProb[0] <0.30:
        lm = landmarks[3]
        lastSeenLM = 3
    else:
        lm = landmarks[4]
        lastSeenLM = 4

#LMInSight = True
#lastMeasuredAngle = measured_angle
        

#if weightMean > 0.6 and LMInSight and not visitedLM[lastSeenLM]:

if weightMean > 0.6 and LMInSight:
    if lastSeenLM =1 and not visitedLM[0] and not visitedLM[1] and not visitedLM[2] and not visitedLM[3]: #note that the  visitedLM[] starts it index at 0. So e.g. visitedLM[3] is the fourth landmark
        print 'Driving towards landmark 1'
        
    elif lastSeenLM =2 and visitedLM[0] and not visitedLM[1] and not visitedLM[2] and not visitedLM[3]: #note that the  visitedLM[] starts it index at 0. So e.g. visitedLM[3] is the fourth landmark
        print 'Driving towards landmark 2'
    elif lastSeenLM =3 and visitedLM[0] and visitedLM[1] and not visitedLM[2] and not visitedLM[3]: #note that the  visitedLM[] starts it index at 0. So e.g. visitedLM[3] is the fourth landmark
        print 'Driving towards landmark 3'
    elif lastSeenLM =4 and visitedLM[0] and visitedLM[1] and  visitedLM[2] and not visitedLM[3]: #note that the  visitedLM[] starts it index at 0. So e.g. visitedLM[3] is the fourth landmark
        print 'Driving towards landmark 4'
    elif lastSeenLM =4 and visitedLM[0] and visitedLM[1] and visitedLM[2] and visitedLM[3]: #note that the  visitedLM[] starts it index at 0. So e.g. visitedLM[3] is the fourth landmark
        print 'THE MAP IS COMPLETED'