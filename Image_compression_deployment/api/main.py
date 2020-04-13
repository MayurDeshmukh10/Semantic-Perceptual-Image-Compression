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

	print("headers : ",headers)

	content_type = headers['content-type']

	print("Content-type : ",content_type)

	imagedata = args['__ow_body']

	print("original : ",imagedata)


	inputfile = ""
	
	data_bytes = imagedata.encode('ascii')

	message_bytes = base64.b64decode(data_bytes)

	data = message_bytes.decode('ascii')

	print("FIRST DECODING : ",data)

	data = data.split("jpg\"\r\n\r\n")

	data = data[1]
	
	data = data[:-36]

	print(data)
	
	try:
	
		base64_image = data.split("base64,")[1]

	except:
		base64_image = data


	data_bytes = bytes(base64_image,'utf-8')

	if content_type == "image/jpg":
		inputfile = "inputfile.jpg" 
		with open(inputfile,"wb") as f:
			f.write(base64.decodebytes(data_bytes))
	else:
		inputfile = "inputfile.png"
		with open(inputfile,"wb") as f:
			f.write(base64.decodebytes(data_bytes))


	
	print("SIZE OF FILE : ",os.stat(inputfile).st_size)

	
	print("FILES AFTER :",os.listdir())

	compression_engine(inputfile)


	print("AFTER COMPRESSION : ",os.listdir())

	with open("compressed_image.jpg", "rb") as img_file:
		my_string = base64.b64encode(img_file.read())


	return {'headers': { 'Content-Type': "image/jpeg",'Access-Control-Allow-Origin': '*',"Access-Control-Allow-Headers":"*" },'body' : my_string}
    


    
