import os
import sys
from pathlib import Path

import nibabel
import tqdm as tqdm
import pydicom

# nifti_dir = sys.argv[1]


# nifti_file = nibabel.load(nifti_dir)
# nifti_array = nifti_file.get_fdata()


def convertNsave(arr, file_dir, index=0):
    """
    `arr`: parameter will take a numpy array that represents only one slice.
    `file_dir`: parameter will take the path to save the slices
    `index`: parameter will represent the index of the slice, so this parameter will be used to put
    the name of each slice while using a for loop to convert all the slices
    """

    dicom_file = pydicom.Dataset()
    dicom_file.is_little_endian = True
    dicom_file.is_implicit_VR = False
    arr = arr.astype('uint16')
    dicom_file.Rows = arr.shape[0]
    dicom_file.Columns = arr.shape[1]
    dicom_file.PhotometricInterpretation = "MONOCHROME2"
    dicom_file.SamplesPerPixel = 1
    dicom_file.BitsStored = 16
    dicom_file.BitsAllocated = 16
    dicom_file.HighBit = 15
    dicom_file.PixelRepresentation = 1
    dicom_file.PixelData = arr.tobytes()
    dicom_file.save_as(os.path.join(file_dir, f'slice{index}.dcm'))


def nifti2dicom_1file(nifti_dir, out_dir):
    """
    This function is to convert only one nifti file into dicom series
    `nifti_dir`: the path to the one nifti file
    `out_dir`: the path to output
    """
    Path(out_dir).mkdir(exist_ok=True, parents=True)
    nifti_file = nibabel.load(nifti_dir)
    nifti_array = nifti_file.get_fdata()
    number_slices = nifti_array.shape[2]

    for slice_ in tqdm.tqdm(range(number_slices)):
        convertNsave(nifti_array[:, :, slice_], out_dir, slice_)


nifti2dicom_1file("/media/kirrog/workdata/core_ct_lung/COVID19_1110/studies/CT-0/study_0010.nii.gz",
                  "/home/kirrog/Documents/study_0010")
nifti2dicom_1file("/media/kirrog/workdata/core_ct_lung/COVID19_1110/studies/CT-0/study_0210.nii.gz",
                  "/home/kirrog/Documents/study_0210")
nifti2dicom_1file("/media/kirrog/workdata/core_ct_lung/COVID19_1110/studies/CT-1/study_0410.nii.gz",
                  "/home/kirrog/Documents/study_0410")
nifti2dicom_1file("/media/kirrog/workdata/core_ct_lung/COVID19_1110/studies/CT-1/study_0610.nii.gz",
                  "/home/kirrog/Documents/study_0610")
nifti2dicom_1file("/media/kirrog/workdata/core_ct_lung/COVID19_1110/studies/CT-1/study_0710.nii.gz",
                  "/home/kirrog/Documents/study_0710")
nifti2dicom_1file("/media/kirrog/workdata/core_ct_lung/COVID19_1110/studies/CT-1/study_0810.nii.gz",
                  "/home/kirrog/Documents/study_0810")
