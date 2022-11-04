from os import getcwd
print(getcwd())



# # from nn.datasets.covid19 import LoaderDataHealthy
# #
# # l = LoaderDataHealthy()
# # print(len(l.ready_data))
# import numpy.random
# import torch
# from nn.models.vae.vae import VAE
# device = "cuda"
#
# v = VAE()
# v.to(device)
# r = numpy.random.rand(5, 1, 512, 512)
# t = torch.Tensor(r).data
# t_n = t.to(device)
# d = v(t_n).cpu()
# print(d.shape)
# from nn.api import train_gan, test_gan
# from nn.models.gan.gan import Discriminator, GAN
# from nn.models.vae.vae import VAE
# 
# train_gan()
# test_gan()

# import requests
#
# answer = requests.post('http://127.0.0.1:5000/sendjson', json={
#                                                             "filename":"1.png",
#                                                             "imgType": "chest",
#                                                             "isCancer": "False",
#                                                             "cancerType": "normal",
#                                                             "comment": "Test Text" })
#
# print(answer)
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
