#from __future__ import division

import os, sys
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from util import load_single_image, normalize
import sys
from PIL import Image
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

image = 'Lion.jpg'
map = 'msroi_map.jpg'
find_best = 1
threshold_pct = 1
use_convert = 0
jpeg_compression = 50
model = 3
single = 1
dataset = "kodak"
print_metrics = 0
output_directory = 'output'
modifier = ""

def make_quality_compression(original,sal,imgg):
    #sal.save("msroi.jpg")
    #skimage.io.imsave( 'msroi_map.jpg', sal )
    '''if print_metrics:
        print(image,)
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
    k.flags.writeable = True
    mx, mn = np.max(sal_arr), np.mean(sal_arr)
    #mx, mn = np.max(sal), np.mean(sal)
    sal_flatten = sal_arr.flatten()
    #sal_flatten = sal.flatten()

    #q_2,q_3,q_5,q_6,q_9 = map(lambda z: np.percentile(sal_arr, z), [20,30,50,60,90])
    #q_2,q_3,q_5,q_6,q_9 = map(lambda z: np.percentile(sal, z), [20,30,50,60,90])

    q_a = [np.percentile(sal_arr, j) for j in quality_steps]
    #q_a = [np.percentile(sal, j) for j in quality_steps]
    low, med, high = 1, 5, 9

    for i in range(shape[0]):
        for j in range(shape[1]):
            for l in range(shape[2]):
                ss = sal_arr[i,j]
                #ss = sal[i,j]

                if model == 1:
                    # model -1
                    # hard-coded model
                    if ss > mn: qq = 9
                    else: qq = 6

                elif model == 2:
                    # model -2
                    # linearly scaled technique
                    qq = (ss * 10 // mx) -1  + 3

                elif model == 3:
                    # model -3
                    # percentile based technique
                    # qq = int(percentileofscore(sal_flatten, ss)/10)
                    for index, q_i in enumerate(q_a):
                        if ss < q_i:
                            qq = index + 1
                            break

                elif model == 4:
                    # model -4
                    # discrete percentile based technique
                    # if   ss < q_2: qq = 4
                    if ss < q_2: qq = 4
                    elif ss < q_6: qq = 6
                    elif ss < q_9: qq = 8
                    else: qq = 9

                elif model == 5:
                    # model -5
                    # two way percentile
                    if ss <  q_5: qq = 2
                    else: qq = 8

                elif model == 6:
                    # model -6
                    # two way percentile - higher coverage
                    if ss <  q_5: qq = 7
                    else: qq = 9

                else:
                    raise Exception("unknown model number")

                if qq < low : qq = low
                if qq > high: qq = high
                k[i,j,l] = img_qualities[qq][i,j,l]


    # save the original file at the given quality level
    #compressed = output_directory + '/' + '_original_' + imgg.split('/')[-1] + '_' + str(jpeg_compression) + '.jpg'
    #original.save(compressed, quality=jpeg_compression)


    #original_size = os.path.getsize(compressed)
    #print("original size : ",original_size)
    #os.system('convert ' + imgg + " " + output_directory + '/temp.png')
    #uncompressed_size = os.path.getsize(output_directory + '/temp.png')
    #os.remove(output_directory + '/temp.png')

    original_size = in_memory_jpeg_compression(original)

    out_img = array2PIL(k)

    if find_best:
        out_name = output_directory + '/' + '_compressed_' + imgg.split('/')[-1] + '_' + '.jpg'
        for qual in range(90,20,-1):
            out_img = out_img.convert("RGB")
            out_img.save(out_name, quality=qual)
            current_size = os.path.getsize(out_name)
            if current_size<= original_size*(1 + threshold_pct/100.0):
                '''if print_metrics:
                    print(model, uncompressed_size, original_size, current_size, jpeg_compression, qual,' | ',)'''
                break
        else:
            '''if print_metrics:
                print(model, uncompressed_size, original_size, current_size, jpeg_compression, qual,' | ',)'''
            pass

    '''else:
        final_quality = [100, 85, 65, 45]
        for fq in final_quality:
            out_name = output_directory + '/' + modifier + imgg.split('/')[-1] + '_' + str(fq) + '.jpg'
            out_img.save(out_name, quality=fq)
    return compressed, out_name'''


    
    '''final_quality = [100, 85, 65, 45]
    for fq in final_quality:
        out_name = output_directory + '/' + modifier + imgg.split('/')[-1] + '_' + str(fq) + '.jpg'
        out_img.save(out_name, quality=fq)
    return compressed, out_name'''




def compression_engine(img):

    image = load_single_image(img)
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
    #skimage.io.imsave( 'msroi_map.jpg', roi_map )
    print("MSROI TYPE : ",type(roi_map))




    from glob import glob
    # make the output directory to store the Q level images,

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    '''if print_metrics:
        from get_metrics import get_metrics'''

    if single:
        original = Image.open(img)
        sal = Image.open('msroi_map.jpg')
        #sal = Image.fromarray((roi_map * 255).astype('uint8'), mode='L')
        #sal = sal.convert("L")
        #print("shape : ",roi_map.shape)
        #sal = myarray2PIL(roi_map)
        make_quality_compression(original,sal,img)

        '''if print_metrics:
            get_metrics(image,a,b, original.size)'''

    '''else:

        if dataset == 'kodak':
            image_path = 'images_directory/kodak/*.png'
        elif dataset == 'large':
            image_path = 'images_directory/output_large/ori_*.png'
        else:
            assert Exception("Wrong dataset choosen")

        for image_file in glob(image_path):
            if dataset == 'large':
                map_file = 'images_directory/output_large/map' + image_file.split('/')[-1][3:-4]
            elif dataset == 'kodak':
                map_file = 'images_directory/output_kodak/map_' + image_file.split('/')[-1] + '.jpg'
            image = image_file
            map   = map_file
            original = Image.open(image)
            sal = Image.open(map)
            a,b = make_quality_compression(original,sal,img)
            if print_metrics:
                get_metrics(image,a,b, original.size)'''
