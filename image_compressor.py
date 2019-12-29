from util import load_single_image, normalize
import cv2
import sys
import compression
from PIL import Image
import datetime
import os

filename = sys.argv[1]

extension = filename.split(".")[-1]
name = filename.split(".")[0]
#image = cv2.imread(sys.argv[1])


if extension == "tiff" or extension == "tif":
    start = datetime.datetime.now()
    im = Image.open(filename)
    converted = im.convert("RGB")
    print("SIZE",im.size)
    converted.save("temp.png",'PNG',quality=100)
    test = Image.open("temp.png")
    print("temp size : ",test.size)
    compression.compression_engine("temp.png")
    out = Image.open("output/_compressed_temp.png_.jpg")
    out.save("__compressed__"+name+".tiff","TIFF")
    os.remove("temp.png")
    os.remove("output/_compressed_temp.png_.jpg")
    print("DONE. time passed : ", ((datetime.datetime.now() - start).seconds) / 60, " minutes")

elif extension == "jpg" or extension == "jpeg" or extension == "png":
    start = datetime.datetime.now()
    compression.compression_engine(filename)
    print("DONE. time passed : ", ((datetime.datetime.now() - start).seconds) / 60, " minutes")







#compression.compression_engine(sys.argv[1])

#print("DONE. time passed : ", ((datetime.datetime.now() - start).seconds) / 60, " minutes")
