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
from nn.api import train_vae, test_vae

train_vae()
# test_vae()
