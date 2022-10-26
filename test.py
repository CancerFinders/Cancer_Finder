import requests

answer = requests.post('http://127.0.0.1:5000/setimg', json={
                                                            "filename":"1.png",
                                                            "imgType": "chest",
                                                            "isCancer": "False",
                                                            "cancerType": "normal",
                                                            "comment": "Test Text" })

print(answer)
# import numpy as np
# import cv2
# import pydicom as dicom
# import numpy
# from skimage import exposure
#
# ds = dicom.dcmread('static/unmarked_img/chest/slice0.dcm', force=True)
# print(ds)
# ds.file_meta.TransferSyntaxUID = dicom.uid.ImplicitVRLittleEndian
# dcm_sample=ds.pixel_array
#
# dcm_sample=exposure.equalize_adapthist(dcm_sample)
# print(ds.pixel_array)
#
#
# import matplotlib.pyplot as plt
# plt.imshow(ds.pixel_array, cmap="gray")
# plt.show()