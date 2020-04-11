import skimage.io
import skimage.transform
import numpy as np
from PIL import Image
from io import BytesIO
import imageio


#performs in-memory jpeg compression and returns compressed size of image
def in_memory_jpeg_compression(img,qual):                    

    img_file = BytesIO()
    img.save(img_file, format='JPEG',quality=qual)

    #print("IN MEMORY COMPRESSION FORMAT : ",type(img))

    arr = np.asarray(img)

    #print("IN MEMORY COMPRESSION ARRAY : ",arr)
    image_file_size = img_file.tell()

    return image_file_size


def chunker(seq, size):
    # http://stackoverflow.com/a/25701576/1189865
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

def load_image(path):
    print("PATH IN UITLS : ",path)
    #img = skimage.io.imread( path ).astype(np.float)
    img = imageio.imread(path).astype(np.float)    
    print("Image : ",img)
    img /= 255.0
    X = img.shape[0]
    Y = img.shape[1]
    S = min(X,Y)
    XX = int((X - S) / 2)
    YY = int((Y - S) / 2)

    # if black and white image, repeat the channels
    if len(img.shape) == 2: img=np.tile(img[:,:,None], 3)
    return skimage.transform.resize( img[XX:XX+S, YY:YY+S], [224,224] )

def load_single_image(image):
    return np.expand_dims(load_image(image),0)

# def load_image_tensorflow(path):
#     img = skimage.io.imread( path ).astype( float )
#     img_resized = tf.image.resize_image_with_crop_or_pad(tf.convert_to_tensor(img, dtype=tf.float32), 224, 224)
#     img_resized = tf.expand_dims(img_resized, 0)
#     return img_resized, img


def array2PIL(arr):
    mode = 'RGBA'
    shape = arr.shape
    arr = arr.reshape(arr.shape[0]*arr.shape[1], arr.shape[2])
    if len(arr[0]) == 3:
        arr = np.c_[arr, 255*np.ones((len(arr),1), np.uint8)]

    return Image.frombuffer(mode, (shape[1], shape[0]), arr.tostring(), 'raw', mode, 0, 1)

def myarray2PIL(arr, size):
    mode = 'RGBA'
    arr = arr.reshape(arr.shape[0]*arr.shape[1], arr.shape[2])
    if len(arr[0]) == 3:
        arr = numpy.c_[arr, 255*numpy.ones((len(arr),1), numpy.uint8)]
    return Image.frombuffer(mode, size, arr.tostring(), 'raw', mode, 0, 1)

def normalize(x):
    min = np.min(x)
    max = np.max(x)
    return (x-min)/(max-min)
