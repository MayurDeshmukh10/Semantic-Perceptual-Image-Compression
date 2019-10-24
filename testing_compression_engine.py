from util import load_single_image, normalize
import cv2
import sys
import compression

#image = cv2.imread(sys.argv[1])

compression.compression_engine(sys.argv[1])
