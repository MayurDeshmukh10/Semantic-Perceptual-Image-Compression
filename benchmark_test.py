from compression import *
from get_metrics import get_metrics
from glob import glob
from PIL import Image
from jpeg_compression import jpeg_compression
import matplotlib.pyplot as plt
import pandas as pd

image_path = "dataset/kodak/*.png"
#image_path = "BenchmarkIMAGES/BenchmarkIMAGES/*.jpg"
jpeg_compression_quality = 50

count = 0
image = []
for image_file in glob(image_path):
    count = count + 1
    d = []
    d.append(count)
    image.append(d)
    out_name = compression_engine(image_file)
    jpeg_compression(image_file,jpeg_compression_quality)
    map_file = "msroi_map.jpg"
    original_image = image_file
    original = Image.open(original_image)
    get_metrics(original_image,"jpeg_compressed.jpg",out_name,original.size)


image.pop()



jpeg_data = pd.read_csv('jpeg_psnr.csv')
jpeg_data_list = jpeg_data.values.tolist()

semantic_data = pd.read_csv('semantic_psnr.csv')
semantic_data_list = semantic_data.values.tolist()

plt.plot(image,jpeg_data_list, color='g')
plt.plot(image,semantic_data_list,color='r')
plt.xlabel("Kodak Dataset Images")
plt.ylabel("JPEG vs Semantic")
plt.savefig("saved.png")
