from PIL import Image
from io import BytesIO
import sys

ima=Image.open("test.jpg")

img_file = BytesIO()
ima.save(img_file, format='JPEG',quality=50)
image_file_size = img_file.tell()

print("img size in memory in bytes: ", image_file_size)
