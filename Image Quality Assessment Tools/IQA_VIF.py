'''
Mayur Deshmukh

usage -  IQA_VIF.py original_image.jpg jpeg_compressed_image.jpg perceptual_compressed_image.jpg


''' 

import numpy
import scipy.signal
import scipy.ndimage
import cv2
import sys
import matplotlib.pyplot as plt

def vifp_mscale(ref, dist):
    sigma_nsq=2
    eps = 1e-10

    num = 0.0
    den = 0.0
    for scale in range(1, 5):
       
        N = 2**(4-scale+1) + 1
        sd = N/5.0

        if (scale > 1):
            ref = scipy.ndimage.gaussian_filter(ref, sd)
            dist = scipy.ndimage.gaussian_filter(dist, sd)
            ref = ref[::2, ::2]
            dist = dist[::2, ::2]
                
        mu1 = scipy.ndimage.gaussian_filter(ref, sd)
        mu2 = scipy.ndimage.gaussian_filter(dist, sd)
        mu1_sq = mu1 * mu1
        mu2_sq = mu2 * mu2
        mu1_mu2 = mu1 * mu2
        sigma1_sq = scipy.ndimage.gaussian_filter(ref * ref, sd) - mu1_sq
        sigma2_sq = scipy.ndimage.gaussian_filter(dist * dist, sd) - mu2_sq
        sigma12 = scipy.ndimage.gaussian_filter(ref * dist, sd) - mu1_mu2
        
        sigma1_sq[sigma1_sq<0] = 0
        sigma2_sq[sigma2_sq<0] = 0
        
        g = sigma12 / (sigma1_sq + eps)
        sv_sq = sigma2_sq - g * sigma12
        
        g[sigma1_sq<eps] = 0
        sv_sq[sigma1_sq<eps] = sigma2_sq[sigma1_sq<eps]
        sigma1_sq[sigma1_sq<eps] = 0
        
        g[sigma2_sq<eps] = 0
        sv_sq[sigma2_sq<eps] = 0
        
        sv_sq[g<0] = sigma2_sq[g<0]
        g[g<0] = 0
        sv_sq[sv_sq<=eps] = eps
        
        num += numpy.sum(numpy.log10(1 + g * g * sigma1_sq / (sv_sq + sigma_nsq)))
        den += numpy.sum(numpy.log10(1 + sigma1_sq / sigma_nsq))
        
    vifp = num/den

    return vifp


def compare_images(original_image,jpeg_compressed,our_compressed):

    psnr1 = vifp_mscale(original_image,jpeg_compressed)

    psnr2 = vifp_mscale(original_image,our_compressed)

    fig = plt.figure("Standard JPEG vs Perceptual Compression")

    plt.suptitle("Standard JPEG VIF: %.2f, Perceptual Compression VIF: %.2f" % (psnr1, psnr2))

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
