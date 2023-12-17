Name: img_ingestion

Description:
The purpose of this source code is to read the dicom images send from customers to Annalise' system and scrub the data
of PHI and send it securely to Annalise backend.

HIGH LEVEL DESIGN:

Receive .dcm file --> De-identify and save as a new .dcm file --> Convert to .png --> Apply base64 encoding on png files
-->  Make a POST API call to send the encoded file to Annalise backend

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
ingestion.py - The main fail where images are read, scrubbed, encoded and sent to the backend. filetransfer.py - To send
the encoded images to the backend via OpenAPI (not working)

Functions:

1. **poll_dcm_directory()**
   Each customer will have a unique directory located under **_"./local_dcm"_**. The purpose of this function is to poll
   customers' directories and identify if there are any new dicom images received from a customer. When images are
   found, this functions makes a call to **_image_dicomcleaner()_** with the image location.

2. **image_dicomcleaner()**
   Each of the images are selected for de-identification and scrubbed using the **_deid_** module. The cleaned .dcm
   images are saved in a new directory. The images are also converted from .dcm to .png for size reduction and easier
   viewing. This function calls **_file_encoding()_** to encode the .png files

3. **file_encoding()**
   Each png file is encoded into base64 format and stored as a text file. For example file name image.png will be stored
   as image.png.txt . These .txt files have to be sent to the backend via OpenAPI and can be decoded at the destination.
   There were issues in the swagger function so unable to perform the POST request.

4. img_manual_scrub()
   The initial implementation of deidentification was carried out manually. It appears that the DicomCleaner is not
   cleaning the images properly (based on test results). Even after scrubbing, if we read the metadata we are able to
   see the PHI. This function is retained to demonstrate that we can choose our fields and deidentify them. An
   observation, is that manually deidentified dicom images provide clean metadata once saved as a new dicom image.
   However, this cannot be viewed on dicom viewer nor can it be converted to jpg or png. This is an isolated function
   and has a direct call from **_main_** if required, otherwise not necessarily a part of the program.

GATEWAY_BUNDLE The gateway_bundle.yaml was converted to python using the swagger function. The purpose of swagger client
is to send these encoded files to the destination server using REST API calls. This requirement could not be met due to
lack of experience with OpenAPI.

HOW TO RUN THE PROGRAM:

1. Clone the repo to local machine
2. Open terminal and run as follows:    
   $ python3 ingestion.py
3. Dicom Images will be picked from customer folders, cleaned, converted and saved in ./local_dcm_dicomcleaner
4. PNG images will be picked from ./local_dcm_dicomcleaner base64 encoded and saved in ./encoded_images
5. Missing function - pushing the base64 encoded files to backend.
6. Sample output:
   terminal$ python3 ingestion.py New images received for processing..... Scrubbing
   ./local_dcm/customer_2/dicom_00000005_000.dcm. Scrubbing ./local_dcm/customer_2/dicom_00000004_000.dcm.
   Encoding...... cleaned-dicom_00000005_000.png 226700 Encoding...... cleaned-dicom_00000004_000.png 226700

PART 2:
• What would your ideal environment look like and how does this fit into it? The ideal environment would be like this:
S3 for receiving the images, Orchestration tool (Jenkins/GitLab CI) to read the bucket contents, processing will happen
on the tool itself (instance or container) and processed filed will be pushed. • How are subsequent deployments made?
The python scripts are stored in GitHub, all changes to be done via SCM. This automation need not be hosted on any
server, it can be converted into a docker image and stored in ECR. The orchestration tool can pull the image from ECR
and execute the ingestion.py inside a container which will have access to EFS for storing the files. The files will be
pushed from EFS to the backend system. • How could you avoid downtime during deployments? We can adopt a GitOps model as
well. This can be deployed in EKS pods which will pull the image and always be in live state.

• Assuming a stateless application, what does immutable infrastructure look like? The ingestion application needs no
front end module, is only going to pull dicom images based on some type of cron schedule, process them in a particular
infrastructure and them push them to the infrastructure. In AWS terms, as stated earlier, S3, EC2, EKS, IAM, ECR would
be sufficient to run this. • What was missed in this implementation? The functionality of pushing the encoded images via
API to another system. Reg de-identification, it is still not clear why DicomCleaner is not cleaning up as per this
file:
https://github.com/pydicom/deid/blob/467b8bd76c6578683c47600b7194e3caed500fd9/deid/data/deid.dicom#L829
• What would you have liked to have added? 1. Cleanup policy for each of the directories 2. Archival system for all dcm
files received from customers 3. Error handling in case fof junk files/very large files received

References:

https://pydicom.github.io/pynetdicom/stable/reference/generated/pynetdicom.association.Association.html#pynetdicom.association.Association.send_c_store

https://products.groupdocs.app/viewer/app/?lang=en&file=f4039a68-038d-40e7-91a6-c90069c798cb%2Fdicom_00000001_000.dcm

https://www.youtube.com/watch?v=To7v7i7eB0A

https://cloud.google.com/architecture/de-identification-of-medical-images-through-the-cloud-healthcare-api

https://stackoverflow.com/questions/2157035/accessing-an-attribute-using-a-variable-in-python

https://www.programiz.com/python-programming/methods/built-in/setattr

https://annalise.ai/wp-content/uploads/2023/06/OPT-PRM-028-Annalise-Enterprise-Administration-Guide.pdf

https://swagger.io/docs/specification/describing-request-body/file-upload/

https://editor.swagger.io/?_ga=2.265863117.397287199.1701537195-1953585220.1701537193

https://github.com/pydicom/deid/blob/master/Dockerfile

https://stackoverflow.com/questions/3715493/encoding-an-image-file-with-base64

https://www.reddit.com/r/learnpython/comments/a2alh9/osscandir_reading_in_random_order/
