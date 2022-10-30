from multiprocessing import Pool
from pathlib import Path
from typing import List

import numpy
import numpy as np
from tqdm import tqdm

from nn.datasets.covid19 import LoaderDataHealthy
from nn.model import MainModel
from nn.pipeline_parts import DatasetInference, DatasetTraining, CaseInference
import matplotlib.pyplot as plt

model = MainModel()


def reload_model(path: Path) -> bool:
    return model.load(path)


# Put list of pairs, of case. Each case is numpy array with 3 dimension. It starts from z [z,x,y]
def train_loaded_model_and_save(data: List[List[numpy.array]], path: Path) -> int:
    acc = model.fit(DatasetTraining(data))
    model.save(path)
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
    i = np.nan_to_num(i, nan=0.0, posinf=1.0, neginf=0.0)
    i /= i.max()
    for j in range(i.shape[2]):
        n[j, 0] = i[:, :, j]
    return n


def train_vae():
    p = "/home/kirrog/projects/Cancer_Finder/models/vae"
    l = LoaderDataHealthy()
    list_in = []
    # for i in l.ready_data:
    #     i = normalize(i)
    #     list_in.append([i, i])
    with Pool(16) as f:
        for i in tqdm(f.imap_unordered(normalize, l.train_data), total=len(l.ready_data)):
            list_in.append([i, i])
    l = None
    d = DatasetTraining(list_in)
    print("Dataset Ready")
    model.fit(d, p)
    print("Complete")
    model.save(Path(p))


def test_vae():
    p = "/home/kirrog/projects/Cancer_Finder/models/vae"
    r_p = "/home/kirrog/projects/Cancer_Finder/data/results"
    model.load(Path(p))
    l = LoaderDataHealthy()
    case = normalize(l.test_data[0])
    for i in tqdm(range(case.shape[0]), desc="saving"):
        r = numpy.zeros((case.shape[2], case.shape[3], 3))
        r[:, :, 0] = case[i, 0]
        plt.imsave(Path(r_p) / "orig" / f"{i:03d}.png", r)
    x = model.predict_once(CaseInference(case))
    x[x < 0] = 0
    x[x > 1] = 1
    for i in tqdm(range(x.shape[0]), desc="saving"):
        r = numpy.zeros((x.shape[2], x.shape[3], 3))
        r[:, :, 0] = x[i, 0]
        plt.imsave(Path(r_p) / "res" / f"{i:03d}.png", r)
    print(x.mean())
    print(x.max())
    print(x.min())
