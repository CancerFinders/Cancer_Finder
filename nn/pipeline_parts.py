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

    counter: int

    def __init__(self, orig: numpy.array, result: numpy.array):
        self.orig = orig
        self.result = result
        self.counter = 0
        if not self.is_right_dim_size():
            raise Exception("Wrong batch format")

    def is_right_dim_size(self) -> bool:
        return (len(self.orig.shape) == 4) and (len(self.result.shape) == 4)

    def get_next_batch(self, size: int) -> (numpy.array, numpy.array, bool):
        size = min(size, self.orig.shape[0] - 1 - self.counter)
        o = self.orig[self.counter: self.counter + size]
        r = self.result[self.counter: self.counter + size]
        self.counter += size
        if self.counter + 1 == self.orig.shape[0]:
            self.counter = 0
            end = True
        else:
            end = False
        return o, r, end


class DatasetTraining(Dataset):
    case_list: List[CaseTrain]
    counter = 0

    def __init__(self, data: List[List[numpy.array]]):
        self.case_list = []
        for i, case in enumerate(data):
            try:
                orig, result = case
                self.case_list.append(CaseTrain(orig, result))
            except Exception:
                logger.warning(f"Case number {i} is wrong dimension size")
        logger.warning(f"Number of cases: {len(self.case_list)}")
        # logger.warning(f"{self.case_list[0].orig.max()} {self.case_list[0].orig.min()}")

    def __getitem__(self, item: int) -> CaseTrain:
        return self.case_list[item]

    def __len__(self) -> int:
        return len(self.case_list)

    def get_next_batch(self, batch_size: int) -> (numpy.array, numpy.array, bool):
        o, r, s = self.case_list[self.counter].get_next_batch(batch_size)
        if s:
            self.counter += 1
        if self.counter == len(self.case_list):
            self.counter = 0
            end = True
        else:
            end = False
        # print(
        #     f"cd: {self.counter:05d} cds: {len((self.case_list)):05d} cc: {self.case_list[self.counter].counter:05d} ccs: {self.case_list[self.counter].orig.shape[0]:05d} b: {batch_size:05d}")
        return o, r, end
