

from concurrent import futures

from joblib import Parallel, delayed
import multiprocessing

from numba import njit, prange

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('ggplot')


from get_metrics import get_metrics

#from six.moves import xrange
import os, sys
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from util import load_single_image, normalize
import sys
from PIL import Image
from io import BytesIO
import os
#import pkg_resources
#pkg_resources.require("numpy==1.15.4")
import numpy as np
from util import load_image, array2PIL, in_memory_jpeg_compression
import argparse
from scipy.stats import percentileofscore

import pandas as pd
from model import CNN
from params import HyperParams
import skimage.io
#import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


map = 'msroi_map.jpg'
find_best = 1
threshold_pct = 15
jpeg_compression = 50
output_directory = 'output'
use_convert = 0

@njit(parallel=True)
def processcal(shape1,shape2,shape3,sal_arr,q_a,low,high,img_qualities,k):
    for i in prange(shape1):
        for j in prange(shape2):
            for l in prange(shape3):
                ss = sal_arr[i,j]

                for index, q_i in enumerate(q_a):
                    if ss < q_i:
                        qq = index + 1
                        break



                if qq < low : qq = low
                if qq > high: qq = high
                k[i,j,l] = img_qualities[qq][i,j,l]

    return k





def make_quality_compression(original,sal,imgg,original1):

    #if the size of the map is not the same original image, then blow it'''
    if original.size != sal.size:
        sal = sal.resize(original.size)

    sal_arr = np.asarray(sal)
    img_qualities = []
    quality_steps = [i*10 for i in range(1,11)]

    # this temp directory will be deleted, do not use this to store your files
    os.makedirs('temp_xxx_yyy')
    for q in quality_steps:
        name = 'temp_xxx_yyy/temp_' + str(q) + '.jpg'
        if use_convert:
            os.system('convert -colorspace sRGB -filter Lanczos -interlace Plane -type truecolor -quality ' + str(q) + ' ' + image + ' ' + name)
        else:
            original.save(name, quality=q)
        img_qualities.append(np.asarray(Image.open(name)))
        os.remove(name)
    os.rmdir('temp_xxx_yyy')

    k = img_qualities[-1][:] # make sure it is a copy and not reference
    shape = k.shape

    #print("SHAPE TUPLE : ",shape)
    k.flags.writeable = True
    mx, mn = np.max(sal_arr), np.mean(sal_arr)

    sal_flatten = sal_arr.flatten()

    q_a = [np.percentile(sal_arr, j) for j in quality_steps]
    low, med, high = 1, 5, 9



    k = processcal(shape[0],shape[1],shape[2],sal_arr,q_a,low,high,img_qualities,k)

    original_size = in_memory_jpeg_compression(original,50)


    #print("Original_size",original_size)

    out_img = array2PIL(k)

    qua = 0
    if find_best:
        out_name = output_directory + '/' + '_compressed_' + imgg.split('/')[-1] + '_' + '.jpg'
        for qual in range(90,20,-1):
            out_img = out_img.convert("RGB")
            #out_img.save(out_name, quality=qual)
            current_size = in_memory_jpeg_compression(out_img,qual)
            if current_size<= original_size*(1 + threshold_pct/100.0):
                qua = qual
                break
        else:
            pass

        out_img.save(out_name, quality=qua)

    return out_name




def compression_engine(img):

    image = load_single_image(img)

    #print("INPUT IMAGE ARRAY ",image.shape)

    hyper = HyperParams(verbose=False)
    images_tf = tf.placeholder(tf.float32, [None, hyper.image_h, hyper.image_w, hyper.image_c], name="images")
    class_tf  = tf.placeholder(tf.int64, [None], name='class')

    cnn = CNN()
    if hyper.fine_tuning:
        cnn.load_vgg_weights()

    conv_last, gap, class_prob = cnn.build(images_tf)
    classmap = cnn.get_classmap(class_tf, conv_last)

    with tf.Session() as sess:
        tf.train.Saver().restore( sess, hyper.model_path )
        conv_last_val, class_prob_val = sess.run([conv_last, class_prob], feed_dict={images_tf: image})

        # use argsort instead of argmax to get all the classes
        class_predictions_all = class_prob_val.argsort(axis=1)

        roi_map = None
        for i in range(-1 * hyper.top_k,0):

            current_class = class_predictions_all[:,i]
            classmap_vals = sess.run(classmap, feed_dict={class_tf: current_class, conv_last: conv_last_val})
            normalized_classmap = normalize(classmap_vals[0])

            if roi_map is None:
                roi_map = 1.2 * normalized_classmap
            else:
                # simple exponential ranking
                roi_map = (roi_map + normalized_classmap)/2
        roi_map = normalize(roi_map)


    # Plot the heatmap on top of image
    fig, ax = plt.subplots(1, 1, figsize=(12, 9))
    ax.margins(0)
    plt.axis('off')
    plt.imshow( roi_map, cmap=plt.cm.jet, interpolation='nearest' )
    plt.imshow( image[0], alpha=0.4)

    # save the plot and the map
    if not os.path.exists('output'):
        os.makedirs('output')
    plt.savefig('output/overlayed_heatmap.png')
    skimage.io.imsave( 'msroi_map.jpg', roi_map )
    plt.clf()
    print("MSROI TYPE : ",type(roi_map))
    plt.close()




    from glob import glob
    # make the output directory to store the Q level images,

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)


    original = Image.open(img)

    #print("ORIGINAL : ",original)
    sal = Image.open('msroi_map.jpg')

    out_name = make_quality_compression(original,sal,img,original)

    return out_name
