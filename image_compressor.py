from util import load_single_image, normalize
import cv2
import sys
import compression
from PIL import Image
import datetime
import os
import piexif

filename = sys.argv[1]

extension = filename.split(".")[-1]
name = filename.split(".")[0]
#image = cv2.imread(sys.argv[1])


if extension == "tiff" or extension == "tif":
    image_type = "tiff"
    start = datetime.datetime.now()
    im = Image.open(filename)
    converted = im.convert("RGB")
    converted.save("temp.png",'PNG',quality=100)
    test = Image.open("temp.png")
    compression.compression_engine("temp.png","",image_type)
    out = Image.open("output/_compressed_temp.png_.jpg")
    out.save("__compressed__"+name+".tiff","TIFF")
    os.remove("temp.png")
    os.remove("output/_compressed_temp.png_.jpg")
    print("DONE. time passed : ", ((datetime.datetime.now() - start).seconds) / 60, " minutes")

elif extension == "jpg" or extension == "jpeg" or extension == "png":
    start = datetime.datetime.now()
    im = Image.open(filename)
    try:
        exif_dict = piexif.load(im.info["exif"])
        w, h = im.size
        exif_dict["0th"][piexif.ImageIFD.XResolution] = (w, 1)
        exif_dict["0th"][piexif.ImageIFD.YResolution] = (h, 1)
        exif_bytes = piexif.dump(exif_dict)
        compression.compression_engine(filename,exif_bytes,"")
    except:
        compression.compression_engine(filename,"","")
    print("DONE. time passed : ", ((datetime.datetime.now() - start).seconds) / 60, " minutes")







#compression.compression_engine(sys.argv[1])

#print("DONE. time passed : ", ((datetime.datetime.now() - start).seconds) / 60, " minutes")
