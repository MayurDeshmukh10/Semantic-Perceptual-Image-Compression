import cv2
import sys

from matplotlib import pyplot as plt

img = cv2.imread(sys.argv[1],0)

histr = cv2.calcHist([img],[0],None,[256],[0,256])

plt.plot(histr)
plt.show()
