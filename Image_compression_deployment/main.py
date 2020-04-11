from compression import *
import base64
import re
import os
from PIL import Image
from io import StringIO



def main(args):

	print("FILES AT START",os.listdir())

	if os.path.exists("inputfile.jpg"):
		os.remove("inputfile.jpg")



	headers = args["__ow_headers"]

	print("AGAINadsd")


	print("headers : ",headers)

	imagedata = args['__ow_body']


	#print("Image data : ",imagedata)
	print("Image : ",imagedata)
	


	#base64_string = bytes(args['__ow_body'],'utf-8')
	#converted = base64_string.decode('base64').strip()
	






	#with open("inputfile.jpg","wb") as f:
	#	f.write(converted)

	#print("BASE64 : ",base64_string)
	#my_str_as_bytes = bytes(base64_string,'utf-8')

	#print("AGAIN")

	#decode_str = my_str_as_bytes.decode("base64")

	#file_like = StringIO(base64_string	)

	#img = Image.open(file_like)

	#rgb_img = img.convert("RGB")

	#rgb_img.save("inputfile.jpg","JPEG")

	#my_str_as_bytes = bytes(base64_string,'utf-8')

	#with open("inputfile.jpeg","wb") as fh:
	#	fh.write(base64.decodebytes(my_str_as_bytes))

	#fh.close()
	print("AGAIN")
	
	data_bytes = imagedata.encode('ascii')

	message_bytes = base64.b64decode(data_bytes)

	data = message_bytes.decode('ascii')

	data_bytes = bytes(data,'utf-8')

	with open("inputfile.jpg","wb") as f:
		f.write(base64.decodebytes(data_bytes))



	#image_data = BytesIO(converted)

	#img = Image.open(image_data)

	#img.save("input.jpg","JPEG")
	#img_data = base64.b64decode(base64_string)


	#print("NeW")
	#decoded_str = decode_base64(imageData)

	#print("Final : ",data)

	#with open("inputfile.jpeg","w") as fh:
	#	fh.write(base64_string)
	
	print("SIZE OF FILE : ",os.stat('inputfile.jpg').st_size)

	
	print("FILES AFTER :",os.listdir())

	compression_engine("inputfile.jpg")
	#image_compression("input.jpg")


	print("AFTER COMPRESSION : ",os.listdir())

	with open("compressed_image.jpg", "rb") as img_file:
		my_string = base64.b64encode(img_file.read())


	return {'headers': { 'Content-Type': "image/jpeg",'Access-Control-Allow-Origin': '*',"Access-Control-Allow-Headers":"*" },'body' : my_string}
    


    
