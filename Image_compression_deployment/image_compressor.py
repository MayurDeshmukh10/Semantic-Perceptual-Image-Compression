from util import load_single_image, normalize
import cv2
import sys
import compression
from PIL import Image
import datetime
import os
import piexif



class image_compressor:

    def __init__(self):
        self.image_type = "tiff"

    

    def image_compression(self,file):


        filename = file
        compression.compression_engine(filename)






