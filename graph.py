import pandas as pd

import matplotlib.pyplot as plt

original_data = pd.read_csv("original_images_size.csv")
original_data_list = original_data.values.tolist()

jpeg_data = pd.read_csv('jpeg_compressed_size.csv')
jpeg_data_list = jpeg_data.values.tolist()

semantic_data = pd.read_csv('semantic_compressed_size.csv')
semantic_data_list = semantic_data.values.tolist()

image = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24]]
print("jpeg", jpeg_data_list)
print("semantic", semantic_data_list)
print("image", image)

image.pop()

plt.plot(image,original_data_list, color='b')
plt.plot(image,jpeg_data_list, color='g')
plt.plot(image,semantic_data_list,color='r')
plt.xlabel("Kodak Dataset Images")
plt.ylabel("Original vs JPEG vs Semantic Size")
plt.savefig("size_saved.png")

'''jpeg_msssim = pd.read_csv('jpeg_msssim.csv')
jpeg_msssim_list = jpeg_msssim.values.tolist()

semantic_msssim = pd.read_csv('semantic_msssim.csv')
semantic_msssim_list = semantic_msssim.values.tolist()

plt.plot(image,jpeg_msssim_list, color='g')
plt.plot(image,semantic_msssim_list,color='r')
plt.xlabel("Kodak Dataset Images")
plt.ylabel("JPEG vs Semantic")
plt.savefig("msssim.png")'''

