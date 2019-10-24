# Image-Compression


#Install Required Dependencies

First install CUDA Toolkit

<code> pip3 install -r requirements.txt </code>


##How to Run

#Generating MS-ROI Map

<code> python3 generate_map.py input_image </code>

Note - map file is generated in output folder


#Compressing Image 

<code> python3 combine_images.py -map msroi_map.jpg -image input_image </code>

#Compressing Image using compression Library

usage - 

<code>import compression</code>

<code>compression.compression_engine("image_to_compress")</code>



Compressed image will be saved in Output folder

Note - run program with sudo 