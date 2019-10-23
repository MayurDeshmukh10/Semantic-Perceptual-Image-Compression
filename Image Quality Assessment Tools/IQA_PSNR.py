'''
Mayur Deshmukh

usage -  IQA_PSNR.py original_image.jpg jpeg_compressed_image.jpg perceptual_compressed_image.jpg


''' 



import sys
import matplotlib.pyplot as plt
import cv2
from skimage import measure



def measure_psnr(original_image,compressed):

    score = measure.compare_psnr(original_image,compressed)

    return score




def compare_images(original_image,jpeg_compressed,our_compressed):

    psnr1 = measure_psnr(original_image,jpeg_compressed)

    psnr2 = measure_psnr(original_image,our_compressed)

    fig = plt.figure("Standard JPEG vs Perceptual Compression")

    plt.suptitle("Standard JPEG PSNR: %.2f, Perceptual Compression PSNR: %.2f" % (psnr1, psnr2))

    ax = fig.add_subplot(1,3,1)
    fig.add_subplot
    plt.imshow(original_image)
    plt.axis("off")

    ax = fig.add_subplot(1,3,2)
    plt.imshow(jpeg_compressed)
    plt.axis("off")

    ax = fig.add_subplot(1,3,3)
    plt.imshow(our_compressed)
    plt.axis("off")


    plt.show()








original_image = cv2.imread(sys.argv[1])
jpeg_compressed = cv2.imread(sys.argv[2])
ps_compressed = cv2.imread(sys.argv[3])

compare_images(original_image,jpeg_compressed,ps_compressed)








