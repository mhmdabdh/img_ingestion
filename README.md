# img_ingestion


Name: img_ingestion

Description:
    The purpose of this source code is to read the dicome images send from customers to Annalise' system and scrub the data
of PHI and send it securely to Annalise backend.

Python Modules used:

pydicom         
- Read the metadata of dicom images using python

deid
- To get files, scrub images
  
shutil   
- Move files from one folder to another

os
- Read files from disk

pathlib
- Fetch file path

base64
- Encode png images to base64


|     |     |
|:---       :|-----|
|  pydicom   |     |
|  deid   |     |
|  shutil   |     |
|     pathlib      |     |
|     base64      |     |
|     os      |     |
