from pathlib import Path

import numpy
import torch

from nn.inferencers.unet_inferencer import UNetInferencer
from nn.models.unet.unet import UNet
from nn.pipeline_parts import DatasetTraining, DatasetInference, CaseInference
from nn.trainers.unet_trainer import UNetTrainer


class MainModel:
    model: UNet
    trainer: UNetTrainer
    inferencer: UNetInferencer

    def __init__(self):
        self.model = UNet(1, 1, True)
        self.trainer = UNetTrainer(self.model)
        self.inferencer = UNetInferencer(self.model)

    def fit(self, dataset: DatasetTraining):
        self.trainer.train(dataset)

    def predict(self, dataset: DatasetInference):
        self.inferencer.predict(dataset)

    def predict_once(self, case: CaseInference) -> numpy.array:
        self.inferencer.predict_ones(case)

    def save(self, path: Path):
        torch.save(self.model.state_dict(), path)

    def load(self, path: Path):
        self.model.load_state_dict(torch.load(path))
        return True
