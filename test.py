from pathlib import Path

import numpy as np
import pydicom
from tqdm import tqdm

from nn.api import train_gan, test_gan, inference, reload_model, predict_ones

reload_model(Path("/home/kirrog/projects/Cancer_Finder/weights"))

p = Path("/home/kirrog/projects/Cancer_Finder/data/studies_CT_Lung_anon")
r = Path("/home/kirrog/projects/Cancer_Finder/data/studies_CT_LUNG_results")


# def normalize(i: numpy.array) -> numpy.array:
#     i[i < 0] = 0
#     n = numpy.zeros((i.shape[-1], 1, i.shape[0], i.shape[1]))
#     i = numpy.log(i)
#     i = numpy.nan_to_num(i, nan=0.0, posinf=1.0, neginf=0.0)
#     i /= i.max()
#     for j in range(i.shape[2]):
#         n[j, 0] = i[:, :, j]
#     return n

def transform(ds, arr):
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


dirs = list(p.glob("*"))
for j, directory in enumerate(dirs):
    dir_prev_name = directory.name
    for dir_in in list(directory.glob("*")):
        dcms = list(dir_in.glob("*.dcm"))
        res = r / dir_prev_name / dir_in.name
        res.mkdir(parents=True, exist_ok=True)
        result_array = np.zeros((len(dcms), 1, 512, 512))
        dsc = []
        for i, dcm in tqdm(enumerate(dcms), desc=f"load:{j:02d}"):
            ds = pydicom.read_file(str(dcm), force=True)
            result_array[i, 0] = ds.pixel_array
            # ds = transform(ds)
            dsc.append(ds)
        minimal = result_array.min()
        maximum = result_array.max()
        result_array[result_array < 0] = 0
        result_array /= maximum
        result_array = predict_ones(result_array)
        result_array[result_array < 0] = 0
        result_array[result_array > 1] = 1
        result_array *= maximum
        result_array[result_array <= 0] = minimal
        for i, dcm in tqdm(enumerate(dcms), desc=f"load:{j:02d}"):
            dsc[i].PixelData = result_array[i, 0].astype('uint16').tobytes()
            dsc[i].save_as(res / dcm.name)
