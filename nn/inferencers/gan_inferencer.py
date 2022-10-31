from typing import List

import numpy
import torch

from nn.models.gan.gan import GAN
from nn.pipeline_parts import DatasetInference, CaseInference


class GANInferencer:
    gan: GAN

    def __init__(self, gan: GAN):
        self.gan = gan

    def predict(self, data: DatasetInference) -> List[numpy.array]:
        result = []
        for case in data.case_list:
            result.append(self.predict_ones(case))
        return result

    def predict_ones(self, case: CaseInference) -> numpy.array:
        r = numpy.zeros(case.data.shape)
        d = numpy.zeros((1, case.data.shape[1], case.data.shape[2], case.data.shape[3]))
        for i in range(case.data.shape[0]):
            d[0] = case.data[i]
            r[i] = self.gan.generate(torch.Tensor(d).cuda())
        return r
