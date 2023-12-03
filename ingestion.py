import pydicom
from deid.dicom import get_files
import shutil
import os
import numpy as np
from PIL import Image
import pathlib

img_location = "./local_dcm"
#Read dataset from C-Store location
dicom_files = list(get_files(img_location, pattern="*.dcm"))
print(dicom_files)

def img_basic(img_path):
    read_img = pydicom.dcmread(img_path)
    print(read_img)
    # print(read_img.PatientAge)
    # print(dir(read_img))

def img_dataset_cleanup():

    cleaned_path="./local_dcm_cleaned/"
    cleanup_metadata = [ 'Modality', 'PatientAge', 'PatientID', 'PatientSex', 'PhotometricInterpretation', 'SOPClassUID', 'SOPInstanceUID', 'SeriesInstanceUID', 'StudyDescription', 'StudyInstanceUID']

    for each_image in dicom_files:
        print(each_image)
        image_metadata = pydicom.dcmread(each_image)
        #print(image_metadata.PatientAge)
        for val in cleanup_metadata:
                print(val)
                #print(image_metadata.val)
                print (getattr(image_metadata, val))
                setattr(image_metadata, val, None)

        filename = (each_image)
        print(filename)
        image_metadata.save_as(filename)
        image_cleaned = pydicom.dcmread(filename)
        print(image_cleaned)
        shutil.move(filename, cleaned_path)


def img_convert_jpg(img_location):
    images_path = os.listdir(img_location)
    print(images_path)

    for each_image in dicom_files:
        ds = pydicom.dcmread(each_image)
        new_image = ds.pixel_array.astype(float)
        scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0
        scaled_image = np.uint8(scaled_image)
        final_image = Image.fromarray(scaled_image)
        new_filename = pathlib.Path(each_image).stem
        #final_image.show()
        final_image.save("./local_dcm_converted/" + new_filename + ".jpg")


if __name__ == '__main__':
    #img_basic("./local_dcm/dicom_00000001_000.dcm")
    img_convert_jpg(img_location)
    img_dataset_cleanup()
