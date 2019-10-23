import sys
import matplotlib.pyplot as plt
import cv2
#from SSIM_PIL import compare_ssim
from PIL import Image
#from skimage.metrics import structural_similarity as ssim

from skimage import measure




def measure_psnr(original_image,compressed):

    '''mse = numpy.mean((original_image-compressed)** 2)

    if mse == 0:
        return 100

    
    PIXEL_MAX = 255.0

    return 20 * math.log10(PIXEL_MAX/math.sqrt(mse))'''


    score = measure.compare_ssim(original_image,compressed,multichannel=True)

    #score = ssim(original_image,compressed)

    return score



def compare_images(original_image,jpeg_compressed,our_compressed):

    psnr1 = measure_psnr(original_image,jpeg_compressed)

    psnr2 = measure_psnr(original_image,our_compressed)

    fig = plt.figure("Standard JPEG vs Perceptual Compression")

    plt.suptitle("Standard JPEG SSIM: %.2f, Perceptual Compression SSIM: %.2f" % (psnr1, psnr2))

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

'''original_image = Image.open(sys.argv[1])
jpeg_compressed = Image.open(sys.argv[2])
ps_compressed = Image.open(sys.argv[3])'''


compare_images(original_image,jpeg_compressed,ps_compressed)