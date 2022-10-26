from pathlib import Path
from typing import List

import numpy
import numpy as np
from tqdm import tqdm

from nn.datasets.covid19 import LoaderDataHealthy
from nn.model import MainModel
from nn.pipeline_parts import DatasetInference, DatasetTraining, CaseInference

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


def train_vae():
    l = LoaderDataHealthy()
    list_in = []
    for i in tqdm(l.ready_data):
        i[i < 0] = 0
        i /= i.max()
        i = np.reshape(i, (i.shape[-1], 1, i.shape[0], i.shape[1]))
        list_in.append([i, i])
    d = DatasetTraining(list_in)
    print("Dataset Ready")
    model.fit(d)
    print("Complete")
    model.save(Path("/home/kirrog/projects/Cancer_Finder/models/vae"))
