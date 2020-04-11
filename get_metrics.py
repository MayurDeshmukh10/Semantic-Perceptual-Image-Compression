import os
from csv import writer
# header
# filename, model_number, uncompressed_size, jpeg_size, current_size, jpeg_compression, current_compression,
# (JPEG) PSNR SSIM MSSSIM VIFP PSNRHVS PSNRHVSM
# (model) PSNR SSIM MSSSIM VIFP PSNRHVS PSNRHVSM
count = 0
s = []


def append_list_as_row(file_name, list_of_elem):

    #print(list_of_elem)
    #f = list(float(list_of_elem))
    # Open file in append mode
    with open(file_name, 'a') as write_obj:
            # Create a writer object from csv module
        csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
            #write_obj.write(list_of_elem)

def get_metrics(original, compressed, out_name, size):

    ol = []
    cl = []
    out_l = []
    original_size = os.path.getsize(original)/1000
    ol.append(str(original_size))
    compressed_size = os.path.getsize(compressed)/1000
    cl.append(str(compressed_size))
    out_size = os.path.getsize(out_name)/1000
    out_l.append(str(out_size))

    append_list_as_row("original_images_size.csv",ol)
    append_list_as_row("jpeg_compressed_size.csv",cl)
    append_list_as_row("semantic_compressed_size.csv",out_l)

    metrics = "PSNR SSIM MSSSIM VIFP PSNRHVS PSNRHVSM".lower().split(' ')

    size_x = str(size[0] - size[0]%16 )# this is to make sure we can get MS-SSIM
    size_y = str(size[1] - size[1]%16) # metrics from VQMT, which requires divisible by 16

    for x in [original, compressed, out_name]:
        yuv_convert_command = "ffmpeg -hide_banner -loglevel panic -y -i " + x +" -s " + size_x + "x" + size_y + " -pix_fmt yuv420p " + x +".yuv"

        if os.system(yuv_convert_command) != 0:
            raise Exception("FFMPEG was not found")
        # print command

    img_com = compressed
    command_metrics = "/home/mayur/Music/Image_compression_benchmarks/VQMT/build/bin/Release/vqmt " + \
                        original+".yuv " + \
                        img_com+".yuv " + \
                        str(size_x) + " " + \
                        str(size_y) + " " + \
                        "1 1 out PSNR SSIM MSSSIM VIFP PSNRHVS PSNRHVSM"


    print("COMMAND: ",command_metrics)

    if os.system(command_metrics) != 0:
        raise Exception("VQMT was not found, please install it from https://github.com/Rolinh/VQMT")
    for m in metrics:
        f = open('out_' + m + '.csv').read().splitlines()[1].split(',')[1]
        os.remove('out_'+m+'.csv')
        print(f)
        l = []
        l.append(f)
            #print(type(f))
            #l = list(f)
            #print("list",l)
        append_list_as_row("jpeg_"+m+'.csv',l)
    print(' | ')
    print('')


    img_com = out_name
    command_metrics = "/home/mayur/Music/Image_compression_benchmarks/VQMT/build/bin/Release/vqmt " + \
                          original+".yuv " + \
                          img_com+".yuv " + \
                          str(size_x) + " " + \
                          str(size_y) + " " + \
                          "1 1 out PSNR SSIM MSSSIM VIFP PSNRHVS PSNRHVSM"

    print("COMMAND: ",command_metrics)

    if os.system(command_metrics) != 0:
        raise Exception("VQMT was not found, please install it from https://github.com/Rolinh/VQMT")

    for m in metrics:
        f = open('out_'+m+'.csv').read().splitlines()[1].split(',')[1]
        os.remove('out_'+m+'.csv')
        print(f)
        l = []
        l.append(f)
        append_list_as_row("semantic_"+m+'.csv',l)

    print(" | ")
    print('')
