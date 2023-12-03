import pydicom
from deid.dicom import get_files
import shutil


img_location = "./local_dcm"

def img_basic(img_path):
    read_img = pydicom.dcmread(img_path)
    print(read_img)
    # print(read_img.PatientAge)
    # print(dir(read_img))

def img_dataset_cleanup(img_location):
    # Read dataset from C-Store location
    dicom_files = list(get_files(img_location, pattern="*.dcm"))
    print(dicom_files)

    ###### PRINT BEFORE CLEANUP
    for dcm_img in dicom_files:
        dcm_metadata = pydicom.dcmread(dcm_img)
        print(dcm_metadata)

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


if __name__ == '__main__':
    #img_basic("./local_dcm/dicom_00000001_000.dcm")
    img_dataset_cleanup(img_location)
