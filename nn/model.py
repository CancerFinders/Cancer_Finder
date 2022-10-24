from pathlib import Path

import torch

from nn.inferencers.unet_inferencer import UNetInferencer
from nn.trainers.unet_trainer import UNetTrainer
from nn.unet.unet import UNet


class MainModel:
    unet: UNet
    unet_trainer: UNetTrainer
    unet_inferencer: UNetInferencer

    def __init__(self):
        self.unet = UNet(1, 1, True)

    def fit(self, dataset):
        self.unet_trainer.train(dataset)

    def predict(self, dataset):
        self.unet_inferencer.predict(dataset)

    def save(self, path: Path):
        torch.save(self.unet.state_dict(), path)

    def load(self, path: Path):
        self.unet.load_state_dict(torch.load(path))
        return True
