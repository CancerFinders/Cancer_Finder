from typing import List

import numpy

from nn.models.vae.vae import VAE
from nn.pipeline_parts import DatasetInference, CaseInference


class VAEInferencer:
    vae: VAE

    def __init__(self, vae: VAE):
        self.vae = vae

    def predict(self, data: DatasetInference) -> List[numpy.array]:
        result = []
        for case in data.case_list:
            result.append(self.vae(case.data).cpu())
        return result

    def predict_ones(self, case: CaseInference) -> numpy.array:
        return self.vae(case.data).cpu()
