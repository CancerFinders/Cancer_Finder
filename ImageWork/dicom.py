import pydicom as dicom
from skimage import exposure


def get_img_dicom(path):
    try:
        ds = dicom.dcmread(path)
    except:
        ds = dicom.dcmread(path, force=True)

    ds.file_meta.TransferSyntaxUID = dicom.uid.ImplicitVRLittleEndian
    dcm_sample = ds.pixel_array
    dcm_sample = exposure.equalize_adapthist(dcm_sample)
    return dcm_sample.tolist()
