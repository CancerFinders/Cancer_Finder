from pathlib import Path
from typing import List

import numpy

from nn.inferencer import Inferencer
from nn.model import MainModel
from nn.trainer import Trainer

model = MainModel()

trainer = Trainer(model)
inferencer = Inferencer(model)


def reload_model(path) -> bool:
    status = model.load(path)
    status &= trainer.reset_model(model)
    status &= inferencer.reset_model(model)
    return status


# Put list of pairs, of case. Each case is numpy array with 3 dimension. It starts from z [z,x,y]
def train_loaded_model_and_save(data: List[List[numpy.array]], path: Path) -> int:
    acc = trainer.train(data)
    model.save(path)
    return acc


# List of cases, only orig, the same orientation as train_loaded_model_and_save
def inference(data: List[numpy.array]) -> List[numpy.array]:
    result = inferencer.infer(data)
    return result
