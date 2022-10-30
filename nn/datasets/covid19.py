from pathlib import Path
from typing import List

import numpy
from tqdm import tqdm

from nn.data_driver import NiftiDirectoryLoader
from sklearn.model_selection import train_test_split


class Config:
    root = Path("/media/kirrog/workdata/core_ct_lung/COVID19_1110")
    masks_path = root / "masks"
    studies = root / "studies/"
    stud_0 = studies / "CT-0"
    stud_1 = studies / "CT-1"
    stud_2 = studies / "CT-2"
    stud_3 = studies / "CT-3"
    stud_4 = studies / "CT-4"


class LoaderDataHealthy:
    c = Config()
    ready_data: List[numpy.array]
    train_data: List[numpy.array]
    test_data: List[numpy.array]

    def __init__(self):
        self.ready_data = []
        n = NiftiDirectoryLoader(self.c.stud_0)
        for _ in tqdm(range(n.size)):
            self.ready_data.append(n.__iter__().data.get_fdata())
        self.train_data, self.test_data = train_test_split(self.ready_data, test_size=0.10, random_state=42)
