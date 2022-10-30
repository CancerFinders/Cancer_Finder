from pathlib import Path

import numpy
import torch
import torch.nn as tnn
import torch.optim as optim

from nn.models.vae.vae import VAE
from nn.pipeline_parts import DatasetTraining

batch_size = 5
epoches = 15


class VAETrainer:
    vae: VAE

    def __init__(self, model: VAE):
        self.vae = model
        self.vae.cuda()
        self.criterion = tnn.MSELoss()
        # self.criterion = tnn.CrossEntropyLoss()
        self.optimizer = optim.SGD(self.vae.parameters(), lr=0.001, momentum=0.9)

    # return loss
    def train_step(self, o: numpy.array, r: numpy.array) -> float:

        inputs = torch.Tensor(o).cuda()
        labels = torch.Tensor(r).cuda()

        # zero the parameter gradients
        self.optimizer.zero_grad()

        # forward + backward + optimize
        outputs = self.vae(inputs)
        loss = self.criterion(outputs, labels)
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def train_epoch(self, dataset: DatasetTraining) -> (int, int):
        s = False
        l = 0.0
        acc = 0
        counter = 0
        while not s:
            o, r, s = dataset.get_next_batch(batch_size)
            loss = self.train_step(o, r)
            if loss < 0.01:
                acc += 1
            l += loss
            counter += 1
            if counter % 100 == 0:
                print(f"Batch: {counter:09d} acc: {(acc / counter):05f} loss: {(l / counter):05f}")
        return acc / counter, l / counter

    def train(self, dataset: DatasetTraining, path: str):
        c = 0
        acc_prev = 0
        for i in range(epoches):
            acc, loss = self.train_epoch(dataset)
            print(f"Complete {i} acc: {acc:05f} loss: {loss:05f}")
            self.save_checkpoint(i, path)
            if acc_prev > acc:
                acc_prev = acc
                c = 0
            else:
                c += 1
                if c > 2:
                    break

    def save_checkpoint(self, epoch: int, path: str):
        p = Path(path)
        p_d = p / f"ep{epoch:03d}"
        p_d.mkdir(parents=True)
        torch.save(self.vae.coder.state_dict(), p_d / "coder.pt")
        torch.save(self.vae.decoder.state_dict(), p_d / "decoder.pt")
