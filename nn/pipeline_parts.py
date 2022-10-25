import logging
from typing import List

import numpy
from torch.utils.data import Dataset

logger = logging.getLogger("pipeline_parts")


class CaseInference:
    data: numpy.array

    def __init__(self, data: numpy.array):
        self.data = data
        if not self.is_right_dim_size():
            raise Exception("Wrong batch format")

    def is_right_dim_size(self) -> bool:
        return len(self.data.shape) == 3


class DatasetInference(Dataset):
    case_list: List[CaseInference]

    def __init__(self, data: List[numpy.array]):
        self.case_list = []
        for i, case in enumerate(data):
            try:
                self.case_list.append(CaseInference(case))
            except Exception:
                logger.warning(f"Case number {i} is wrong dimension size")

    def __getitem__(self, item: int) -> CaseInference:
        return self.case_list[item]

    def __len__(self) -> int:
        return len(self.case_list)


class CaseTrain:
    orig: numpy.array
    result: numpy.array

    def __init__(self, orig: numpy.array, result: numpy.array):
        self.orig = orig
        self.result = result
        if not self.is_right_dim_size():
            raise Exception("Wrong batch format")

    def is_right_dim_size(self) -> bool:
        return (len(self.orig.shape) == 3) and (len(self.result.shape) == 3)


class DatasetTraining(Dataset):
    case_list: List[CaseTrain]

    def __init__(self, data: List[List[numpy.array]]):
        self.case_list = []
        for i, case in enumerate(data):
            try:
                orig, result = case
                self.case_list.append(CaseTrain(orig, result))
            except Exception:
                logger.warning(f"Case number {i} is wrong dimension size")

    def __getitem__(self, item: int) -> CaseTrain:
        return self.case_list[item]

    def __len__(self) -> int:
        return len(self.case_list)
