from typing import List

import numpy

from nn.models.unet.unet import UNet
from nn.pipeline_parts import CaseInference, DatasetInference


class UNetInferencer:
    unet: UNet

    def __init__(self, unet: UNet):
        self.unet = unet

    def predict(self, data: DatasetInference) -> List[numpy.array]:
        pass

    def predict_ones(self, case: CaseInference) -> numpy.array:
        pass
