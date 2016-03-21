import cv2
import numpy as np
import sys
import random, getopt

def getThreshold(defaultThreshold=0.8):
	threshold = defaultThreshold
	try:
		opts, args = getopt.getopt(sys.argv[1:], "t:", "threshold=")
		for opt, arg in opts:
			if opt in ("-t","--threshold"):
				threshold = arg
	except Exception, e:
		pass
	return threshold

if len(sys.argv)<3:
	print "Please enter proper arguments"
	exit(0)

main = cv2.imread(sys.argv[1])
# print main
sub = cv2.imread(sys.argv[2])
# sub = main[30:40, 30:40, :]
# cv2.imwrite(sub, 'other.png')
rightOffset = 15
downOffset = 15
isRandomCoordinate = True

try:
	rightOffset = int(sys.argv[3])
except Exception, e:
	pass

try:
	downOffset = int(sys.argv[4])
except Exception, e:
	pass

try:
	isRandomCoordinate = not (int(sys.argv[5]) == 0)
except Exception, e:
	pass

result = cv2.matchTemplate(main,sub,cv2.TM_CCOEFF_NORMED)

#the get the best match fast use this:
(min_x,max_y,minloc,maxloc) = cv2.minMaxLoc(result)
(x,y) = minloc
# w, h = 10, 10

#get all the matches:
# result2 = np.reshape(result, result.shape[0]*result.shape[1])
# sort = np.argsort(result2)
# (y1, x1) = np.unravel_index(sort[0], result.shape) #best match
# (y2, x2) = np.unravel_index(sort[1], result.shape) #second best match
# print (y1,x1)
# print (y2,x2)

result = cv2.matchTemplate(main,sub,cv2.TM_CCOEFF_NORMED)
# print "result is:",result

threshold = getThreshold()
# print threshold

loc = np.where(result >= threshold)
# print "loc is:",loc
flag = True

# for pt in zip(*loc[::-1]):
# 	cv2.rectangle(main, pt, (pt[0]+w, pt[1]+h), (0,255,255),2)
# cv2.imwrite('temp.jpg', main)
# cv2.imshow('Detected', main)

for i in loc:
	if not len(i):
		flag=False
		break
if not flag:
	exit(0)


ans = np.unravel_index(result.argmax(),result.shape)
print "ans is:", str(ans)
if ans[0] == 0 and ans[1] == 0:
	pass
else:
	print str(ans[1]+rightOffset + isRandomCoordinate * random.uniform(-2.0,5.0)) + ":" +  str(ans[0]+downOffset + isRandomCoordinate * random.uniform(-2.0,5.0))