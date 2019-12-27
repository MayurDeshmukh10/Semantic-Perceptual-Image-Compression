from util import load_single_image, normalize
import cv2
import sys
import compression
import datetime

#image = cv2.imread(sys.argv[1])

start = datetime.datetime.now()

compression.compression_engine(sys.argv[1])

print("DONE. time passed : ", ((datetime.datetime.now() - start).seconds) / 60, " minutes")
