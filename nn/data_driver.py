from pathlib import Path
from typing import List

import nibabel as nib


class NiftiEntity:

    def __init__(self, d):
        self.data = d


class NiftiDirectoryLoader:
    directory: Path
    nifties_paths: List[Path]
    size: int
    counter: int

    def __init__(self, path_to_dir: Path):
        if not path_to_dir.is_dir():
            raise Exception("Not a dir")
        self.directory = path_to_dir
        self.counter = 0
        self.nifties_paths = list(sorted([Path(x) for x in list(path_to_dir.glob("*.nii.gz"))]))
        self.size = len(self.nifties_paths)

    def __iter__(self) -> NiftiEntity:
        img = nib.load(self.nifties_paths[self.counter])
        self.counter += 1
        if self.counter == self.size:
            self.counter = 0
        return NiftiEntity(img)
