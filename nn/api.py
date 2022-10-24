from pathlib import Path
from typing import List

import numpy

from nn.model import MainModel

model = MainModel()


def reload_model(path: Path) -> bool:
    return model.load(path)


# Put list of pairs, of case. Each case is numpy array with 3 dimension. It starts from z [z,x,y]
def train_loaded_model_and_save(data: List[List[numpy.array]], path: Path) -> int:
    acc = model.fit(data)
    model.save(path)
    return acc


# List of cases, only orig, the same orientation as train_loaded_model_and_save
def inference(data: List[numpy.array]) -> List[numpy.array]:
    result = model.predict(data)
    return result
