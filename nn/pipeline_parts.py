from typing import List

import numpy


class CaseInference:
    data: numpy.array

    def __init__(self, data):
        if self.check(data):
            self.data = data
        else:
            raise Exception("Wrong batch format")

    def check(self, data) -> bool:
        return len(data.shape) == 3


class DatasetInference:
    batch_list: List[CaseInference]

    def __init__(self, data):
        self.batch_list = []
        if len(data.shape) != 4:
            raise Exception("Wrong number of dimensions in data")
        for i in range(data.shape[0]):
            self.batch_list.append(CaseInference(data[i]))
