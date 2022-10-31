from multiprocessing import Pool
from pathlib import Path
from typing import List

import numpy
import torch
from matplotlib import pyplot as plt
from tqdm import tqdm

from nn.datasets.covid19 import LoaderDataIll2, LoaderDataHealthy
from nn.model import MainModel
from nn.pipeline_parts import DatasetTraining, DatasetInference, CaseInference

model = MainModel()


def reload_model(path: Path) -> bool:
    return model.load(path)


# Put list of pairs, of case. Each case is numpy array with 3 dimension. It starts from z [z,x,y]
def train_loaded_model_and_save(data: List[List[numpy.array]], path: Path) -> int:
    acc = model.fit(DatasetInference(data), str(path))
    return acc


# List of cases, only orig, the same orientation as train_loaded_model_and_save
def inference(data: List[numpy.array]) -> List[numpy.array]:
    result = model.predict(DatasetInference(data))
    return result


def predict_ones(case: numpy.array) -> numpy.array:
    return model.predict_once(CaseInference(case))


def normalize(i: numpy.array) -> numpy.array:
    i[i < 0] = 0
    n = numpy.zeros((i.shape[-1], 1, i.shape[0], i.shape[1]))
    i = numpy.log(i)
    i = numpy.nan_to_num(i, nan=0.0, posinf=1.0, neginf=0.0)
    i /= i.max()
    for j in range(i.shape[2]):
        n[j, 0] = i[:, :, j]
    return n


def train_vae():
    p = "/home/kirrog/projects/Cancer_Finder/models/vae_3"
    l = LoaderDataHealthy()
    list_in = []
    # for i in l.ready_data:
    #     i = normalize(i)
    #     list_in.append([i, i])
    with Pool(16) as f:
        for i in tqdm(f.imap_unordered(normalize, l.train_data), total=len(l.train_data)):
            list_in.append([i, i])
    l = None
    d = DatasetTraining(list_in)
    print("Dataset Ready")
    model.fit(d, p)
    print("Complete")
    model.save(Path(p))


def test_vae():
    p = "/home/kirrog/projects/Cancer_Finder/models/vae_3"
    r_p = "/home/kirrog/projects/Cancer_Finder/data/results_3"
    model.load(Path(p))
    l = LoaderDataHealthy()
    case = normalize(l.test_data[0])
    for i in tqdm(range(case.shape[0]), desc="saving"):
        r = numpy.zeros((case.shape[2], case.shape[3], 3))
        r[:, :, 0] = case[i, 0]
        p_orig = Path(r_p) / "orig"
        p_orig.mkdir(parents=True, exist_ok=True)
        plt.imsave(p_orig / f"{i:03d}.png", r)
    x = model.predict_once(CaseInference(case))
    x[x < 0] = 0
    x[x > 1] = 1
    for i in tqdm(range(x.shape[0]), desc="saving"):
        r = numpy.zeros((x.shape[2], x.shape[3], 3))
        r[:, :, 0] = x[i, 0]
        p_res = Path(r_p) / "res"
        p_res.mkdir(parents=True, exist_ok=True)
        plt.imsave(p_res / f"{i:03d}.png", r)
    num = numpy.sum(numpy.abs(numpy.subtract(case, x)))
    print(num)


def train_gan():
    p_c = "/home/kirrog/projects/Cancer_Finder/models/vae_3"
    p = "/home/kirrog/projects/Cancer_Finder/models/gan_0"
    l = LoaderDataIll2()
    list_in = []
    with Pool(16) as f:
        for i in tqdm(f.map(normalize, l.ready_data), total=len(l.ready_data)):
            list_in.append(i)
    l = None
    print(list_in[0].shape)
    d = DatasetInference(list_in)
    model.model.coder.load_state_dict(torch.load(Path(p_c) / "coder.pt"))
    print("Dataset Ready")
    model.fit(d, p)
    print("Complete")
    model.save(Path(p))


def test_gan():
    p = "/home/kirrog/projects/Cancer_Finder/models/gan_0"
    r_p = "/home/kirrog/projects/Cancer_Finder/data/results_4"
    model.load(Path(p))
    l = LoaderDataHealthy()
    case = normalize(l.test_data[0])
    for i in tqdm(range(case.shape[0]), desc="saving"):
        r = numpy.zeros((case.shape[2], case.shape[3], 3))
        r[:, :, 0] = case[i, 0]
        p_orig = Path(r_p) / "orig"
        p_orig.mkdir(parents=True, exist_ok=True)
        plt.imsave(p_orig / f"{i:03d}.png", r)
    x = model.predict_once(CaseInference(case))
    x[x < 0] = 0
    x[x > 1] = 1
    for i in tqdm(range(x.shape[0]), desc="saving"):
        r = numpy.zeros((x.shape[2], x.shape[3], 3))
        r[:, :, 0] = x[i, 0]
        p_res = Path(r_p) / "res"
        p_res.mkdir(parents=True, exist_ok=True)
        plt.imsave(p_res / f"{i:03d}.png", r)
    num = numpy.sum(numpy.abs(numpy.subtract(case, x)))
    print(num)
