import pydicom
from deid.dicom import get_files, DicomCleaner
import shutil
import os
import pathlib
import base64


img_location = "./local_dcm"
# Read dataset from C-Store location
dicom_files = list(get_files(img_location, pattern="*.dcm"))
# print(dicom_files)

cleaned_location = "./local_dcm_dicomcleaner"
# print(cleaned_location)

encoding_files = list(get_files(cleaned_location, pattern="*.jpg"))
print(encoding_files)


def poll_dcm_directory():
    cust_directory = []
    count = 0
    for fol in sorted(os.scandir('./local_dcm'), key=lambda sortdir: sortdir.name):
        print(fol.name)
        cust_directory.append(fol.name)
    # print(cust_directory)
    for dir_name in cust_directory:
        dir_name = (
                "./local_dcm/" + (dir_name) + "/")
        print(dir_name)
        if len(os.listdir(dir_name)) == 0:
            print("No new images to process!")
        else:
            print("New images received for processing.....")
            count +=1
    print(count)
    if count ==0:
        exit()
    else:
        encoding_lasttry()

def img_dataset_cleanup():
    cleaned_path = "./local_dcm_cleaned/"
    cleanup_metadata = ['Modality', 'PatientAge', 'PatientID', 'PatientSex', 'PhotometricInterpretation', 'SOPClassUID',
                        'SOPInstanceUID', 'SeriesInstanceUID', 'StudyDescription', 'StudyInstanceUID']

    for each_image in dicom_files:
        image_metadata = pydicom.dcmread(each_image)
        for val in cleanup_metadata:
            print(val)
            print(getattr(image_metadata, val))
            setattr(image_metadata, val, None)

        filename = each_image
        image_metadata.save_as(filename)
        image_cleaned = pydicom.dcmread(filename)
        print(image_cleaned)

        dcm_filename = pathlib.Path(each_image).stem
        dcm_filename = (dcm_filename + ".dcm")
        print(dcm_filename)
        shutil.move(each_image, cleaned_path)


def image_dicomecleaner(img_source):
    images_path = os.listdir(img_source)
    print(images_path)
    for each_image in dicom_files:
        # client = DicomCleaner(output_folder="./local_dcm_dicomcleaner")
        client = DicomCleaner(output_folder=".")
        client.detect(each_image)
        client.clean()
        client.save_png()
        client.save_dicom()



def encoding_lasttry():
    print("buzz1")
    cleaned_location = "./local_dcm_dicomcleaner"
    print(cleaned_location)
    path = './local_dcm_dicomcleaner'
    files = [x for x in os.listdir(path) if x.endswith('.png')]
    print(files)
    # print(encoding_files)
    for each_image in files:
        print("Encoding......", each_image)
        with open(each_image, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        print(encoded_string)


if __name__ == '__main__':
    poll_dcm_directory()
    img_dataset_cleanup() #manual scrub to deidentify data
    # image_dicomecleaner(img_location) #f4 does everything except, base64 try it
    encoding_lasttry()
