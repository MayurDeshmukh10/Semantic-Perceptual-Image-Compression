from image_compressor import *
import base64
import tensorflow as tf




def main(args):
    decoded = args['__ow_body']

    my_str_as_bytes = bytes(decoded,'utf-8')

    with open("input.jpg","wb") as fh:
        fh.write(base64.decodebytes(my_str_as_bytes))

    ic = image_compressor()
    ic.image_compression('input.jpg')

    with open("compressed_image.jpg", "rb") as img_file:
        my_string = base64.b64encode(img_file.read())


    return {'body' : my_string}
    #return { "version" : tf.__version__ }

    

