from pathlib import Path

import numpy
import torch

from nn.inferencers.unet_inferencer import UNetInferencer
from nn.inferencers.vae_inferencer import VAEInferencer
from nn.models.unet.unet import UNet
from nn.models.vae.vae import VAE
from nn.pipeline_parts import DatasetTraining, DatasetInference, CaseInference
from nn.trainers.unet_trainer import UNetTrainer
from nn.trainers.vae_trainer import VAETrainer


class MainModel:
    model: VAE
    trainer: VAETrainer
    inferencer: VAEInferencer

    def __init__(self):
        self.model = VAE()
        self.trainer = VAETrainer(self.model)
        self.inferencer = VAEInferencer(self.model)

    def fit(self, dataset: DatasetTraining):
        self.trainer.train(dataset)

    def predict(self, dataset: DatasetInference):
        self.inferencer.predict(dataset)

    def predict_once(self, case: CaseInference) -> numpy.array:
        self.inferencer.predict_ones(case)

    def save(self, path: Path):
        torch.save(self.model.coder.state_dict(), path / "coder.pt")
        torch.save(self.model.decoder.state_dict(), path / "decoder.pt")

    def load(self, path: Path):
        self.model.coder.load_state_dict(torch.load(path / "coder.pt"))
        self.model.decoder.load_state_dict(torch.load(path / "decoder.pt"))
        return True
