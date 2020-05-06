from compression import *
import base64
import re
import os
from PIL import Image
from io import StringIO

import ibm_boto3
from ibm_botocore.client import Config, ClientError
from webptools import webplib as webp


COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud" 
COS_API_KEY_ID_DOWNLOAD = "zkT0ncxw5FhJVs0oRDkLLBujxeaAQkeK1S8kykNCNkro" 
COS_API_KEY_ID_UPLOAD = "PsiYNRatlfODo-GWMMCkEWnki7vmiTobnKUcInWzoaIn"
COS_AUTH_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"
COS_RESOURCE_CRN_DOWNLOAD = "crn:v1:bluemix:public:cloud-object-storage:global:a/339e572a879642078f0f439e696cf9af:be9ee3a0-cd5f-41ef-b5d1-472f1800bb25::"
COS_RESOURCE_CRN_UPLOAD = "crn:v1:bluemix:public:cloud-object-storage:global:a/339e572a879642078f0f439e696cf9af:be9ee3a0-cd5f-41ef-b5d1-472f1800bb25::"





def main(args):

	print("FILES AT START",os.listdir())

	if os.path.exists("inputfile.jpg"):
		os.remove("inputfile.jpg")


	imagedata = args['__ow_body']

	headers = args["__ow_headers"]
	
	image_extension = headers['content-type']

	print("Image Extension : ",image_extension)

	print("MAYUR : ",imagedata)

	try:
		imagedata = base64.b64decode(imagedata)
		imagedata = imagedata.decode('utf-8')
		unique_filename = imagedata.split("=")[1]
		
	except:
		
		unique_filename = imagedata.split("=")[1]

	print("MAYUR : ",imagedata)


	


	print("FILENAME : ",unique_filename)
	
	cos_download = ibm_boto3.resource("s3",
        ibm_api_key_id=COS_API_KEY_ID_DOWNLOAD,
        ibm_service_instance_id=COS_RESOURCE_CRN_DOWNLOAD,
        ibm_auth_endpoint=COS_AUTH_ENDPOINT,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT)
		
	try:
		file = cos_download.Object("imagecompressionuploads",unique_filename).get()
	except ClientError as be:
		print("CLIENT ERROR: {0}\n".format(be))
		return { 'statusCode': 400, 'body': be } 
	except Exception as e1: 
		print("Unable to retrieve file contents: {0}".format(e1))
		return { 'statusCode': 400, 'body': e1 }

	image_data = file["Body"].read()

	if image_extension == 'image/jpeg':
		inputfile = 'inputfile.jpg'
		with open('inputfile.jpg','wb') as f:
			f.write(image_data)
		rgba_image = Image.open("inputfile.jpg")
		rgb_image = rgba_image.convert('RGB')
		rgb_image.save("inputfile.jpg")

	elif image_extension == 'image/png':
		inputfile = 'inputfile.png'
		with open('inputfile.png','wb') as f:
			f.write(image_data)
		rgba_image = Image.open("inputfile.png")
		rgb_image = rgba_image.convert('RGB')
		rgb_image.save("inputfile.png")

	elif image_extension == "image/tiff":
		tifffile = "tifffile.tiff"
		inputfile = "inputfile.png"
		saved = 'input.png'
	
		with open(tifffile,'wb') as f:
			f.write(image_data)

		im = Image.open(tifffile)
		im.save(saved,'PNG',quality=100)
	
		imag = Image.open("input.png")
		imag_arr = np.array(imag)
		converted_arr = imag_arr[...,:3]
		con = Image.fromarray(converted_arr,'RGB')
		con.save(inputfile)
		rgba_image = Image.open("inputfile.png")
		rgb_image = rgba_image.convert('RGB')
		rgb_image.save("inputfile.png")

	elif image_extension == "image/webp":
		inputfile = "inputfile.png"
		with open("input.webp","wb") as f:
			f.write(image_data)

		im = Image.open("input.webp").convert("RGB")
		im.save(inputfile,"png")

		#webp.dwebp("input.webp",inputfile,"-o")


	
	
	print("SIZE OF FILE : ",os.stat(inputfile).st_size)

	
	

	try:

		compression_engine(inputfile)
	except Exception as m1: 
		return { 'statusCode': 400, 'body': m1 }

	print("FILES AFTER :",os.listdir())

	try:
	
		cos_upload = ibm_boto3.resource("s3",ibm_api_key_id=COS_API_KEY_ID_UPLOAD,ibm_service_instance_id=COS_RESOURCE_CRN_UPLOAD,ibm_auth_endpoint=COS_AUTH_ENDPOINT,config=Config(signature_version="oauth"),endpoint_url=COS_ENDPOINT)
		print("Starting file transfer for {0} to bucket: {1}\n".format(unique_filename, "imagecompressiondownloads"))
		part_size = 1024 * 1024 * 5
		file_threshold = 1024 * 1024 * 40
		transfer_config = ibm_boto3.s3.transfer.TransferConfig(
		    multipart_threshold=file_threshold,
		    multipart_chunksize=part_size
		)
		
		with open("heatmap.png", "rb") as file_data:
		    		cos_upload.Object("imagecompressiondownloads", "heatmap.png").upload_fileobj(
		        Fileobj=file_data,
		        Config=transfer_config
		    )

		with open("msroi_map.jpg", "rb") as file_data:
		    		cos_upload.Object("imagecompressiondownloads","msroi_map.jpg").upload_fileobj(
		        Fileobj=file_data,
		        Config=transfer_config
		    )
		if image_extension == 'image/jpeg':
			
			with open("compressed_image.jpg", "rb") as file_data:
		    		cos_upload.Object("imagecompressiondownloads", unique_filename).upload_fileobj(
		        Fileobj=file_data,
		        Config=transfer_config
		    )
		elif image_extension == 'image/png':
			op = Image.open("compressed_image.jpg")
			op.save("out.png")
			with open("out.png", "rb") as file_data:
		    		cos_upload.Object("imagecompressiondownloads", unique_filename).upload_fileobj(
		        Fileobj=file_data,
		        Config=transfer_config
		    )
		elif image_extension == 'image/tiff':
			op = Image.open("compressed_image.jpg")
			op.save("out.png")
			md = Image.open("out.png")
			md.save("tiffoutput.tiff","TIFF")
			with open("tiffoutput.tiff", "rb") as file_data:
		    		cos_upload.Object("imagecompressiondownloads", unique_filename).upload_fileobj(
		        Fileobj=file_data,
		        Config=transfer_config
		    )
		elif image_extension == 'image/webp':
			im = Image.open("compressed_image.jpg").convert("RGB")
			im.save("out.webp","webp")
			with open("out.webp", "rb") as file_data:
		    		cos_upload.Object("imagecompressiondownloads", unique_filename).upload_fileobj(
		        Fileobj=file_data,
		        Config=transfer_config
		    )
			
		print("Transfer for {0} Complete!\n".format(unique_filename))

	except ClientError as be:
		print("CLIENT ERROR: {0}\n".format(be))
		return { 'statusCode': 400, 'body': be }
	except Exception as e:
		print("Unable to complete multi-part upload: {0}".format(e))
		return { 'statusCode': 400, 'body': e }

	return { 'statusCode': 200, 'body': "Compression Successfully" } 



	
		



	
	
	

	






	


    
