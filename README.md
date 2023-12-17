# img_ingestion


Name: img_ingestion

Description:
    The purpose of this source code is to read the dicome images send from customers to Annalise' system and scrub the data
of PHI and send it securely to Annalise backend.

Python Modules used:

pydicom         
- Read the metadata of dicom images using python

deid
- To get files, scrub images and deidentify the data
  
shutil   
- Move files from one folder to another

os
- Read files from disk

pathlib
- Fetch file path

base64
- Encode png images to base64


Important files:
ingestion.py - The main fail where images are read, scrubbed, encoded and sent to the backend.
filetransfer.py - To send the encoded images to the backend via OpenAPI (not working)

Functions:

1. **poll_dcm_directory()**
    Each customer will have a unique directory located under **_"./local_dcm"_**. The purpose of this function is to poll customers' directories and identify if there are any new dicom images received from a customer.
    When images are found, this functions makes a call to **_image_dicomcleaner()_** with the image location.
    
2. **image_dicomcleaner**
    Each of the images are selected for de-identification and scrubbed using the **_deid_** module.
    The cleaned .dcm images are saved in a new directory. The images are also converted from .dcm to .png for size reduction and easier viewing.
    This function calls **_file_encoding()_** to encode the .png files 

3. **file_encoding()**
    Each png file is encoded into base64 format and stored as a text file. For example file name image.png 
    will be stored as image.png.txt . These .txt files have to be sent to the backend via OpenAPI
    and can be decoded at the destination.
    There were issues in the swagger function so unable to perform the POST request. 

4. 

GATEWAY_BUNDLE
    The gateway_bundle.yaml was converted to python using the swagger function. The purpose of swagger client is to send 
    these encoded files to the destination server using REST API calls. This functionality could not be achieved.
