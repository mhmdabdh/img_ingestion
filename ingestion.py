import pydicom as dicom
from deid.dicom import get_files
import shutil


def img_basic(img_path):
    read_img = dicom.dcmread(img_path)
    print(read_img)
    # print(read_img.PatientAge)
    # print(dir(read_img))




if __name__ == '__main__':
    img_basic("./local_dcm/dicom_00000001_000.dcm")
