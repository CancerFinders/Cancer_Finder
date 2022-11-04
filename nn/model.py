from pathlib import Path

import numpy
import torch

from nn.inferencers.gan_inferencer import GANInferencer
from nn.inferencers.unet_inferencer import UNetInferencer
from nn.inferencers.vae_inferencer import VAEInferencer
from nn.models.gan.gan import GAN
from nn.models.unet.unet import UNet
from nn.models.vae.vae import VAE
from nn.pipeline_parts import DatasetTraining, DatasetInference, CaseInference
from nn.trainers.gan_trainer import GANTrainer
from nn.trainers.unet_trainer import UNetTrainer
from nn.trainers.vae_trainer import VAETrainer


class MainModel:
    model: GAN
    trainer: GANTrainer
    inferencer: GANInferencer

    def __init__(self):
        self.model = GAN()
        self.trainer = GANTrainer(self.model)
        self.inferencer = GANInferencer(self.model)

    def fit(self, dataset: DatasetInference, path):
        self.trainer.train(dataset, path)

    def predict(self, dataset: DatasetInference):
        return self.inferencer.predict(dataset)

    def predict_once(self, case: CaseInference) -> numpy.array:
        return self.inferencer.predict_ones(case)

    def save(self, path: Path):
        torch.save(self.model.coder.state_dict(), path / "coder.pt")
        torch.save(self.model.decoder.state_dict(), path / "decoder.pt")
        torch.save(self.model.discriminator.state_dict(), path / "discriminator.pt")

    def load(self, path: Path):
        if not torch.cuda.is_available():
            self.model.coder.load_state_dict(torch.load(path / "coder.pt", map_location=torch.device('cpu')))
            self.model.decoder.load_state_dict(torch.load(path / "decoder.pt", map_location=torch.device('cpu')))
            self.model.discriminator.load_state_dict(torch.load(path / "discriminator.pt", map_location=torch.device('cpu')))
        else:
            self.model.coder.load_state_dict(torch.load(path / "coder.pt"))
            self.model.decoder.load_state_dict(torch.load(path / "decoder.pt"))
            self.model.discriminator.load_state_dict(torch.load(path / "discriminator.pt"))
        return True
