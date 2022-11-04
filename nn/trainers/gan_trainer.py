from pathlib import Path

import numpy
import torch
import torch.nn as tnn
import torch.optim as optim

from nn.models.gan.gan import GAN, bottleneck_size
from nn.pipeline_parts import DatasetTraining, DatasetInference

batch_size = 5
epoches = 15
early_stopping = 2
threshold = 0.2




class GANTrainer:
    gan: GAN

    def __init__(self, model: GAN):
        self.gan = model
        if not torch.cuda.is_available():
            print("At cpu it will train very slow, so code nonsupport it")
            return
        self.gan.cuda()
        self.criterion = tnn.MSELoss()
        self.optimizer = optim.Adam(self.gan.parameters(), lr=0.001)
        self.freeze_coder()

    def freeze_coder(self):
        for param in self.gan.coder.parameters():
            param.requires_grad = False

    def defreeze_decoder(self, b: bool):
        for param in self.gan.decoder.parameters():
            param.requires_grad = b

    def derfreeze_discriminator(self, b: bool):
        for param in self.gan.discriminator.parameters():
            param.requires_grad = b

    def train_step_vae(self, o: numpy.array) -> (float, float):
        inputs = torch.Tensor(o).cuda()
        self.optimizer.zero_grad()
        decoder_output = self.gan.decoder(self.gan.coder(inputs))
        loss_d = self.criterion(decoder_output, inputs)
        loss_d.backward(retain_graph=True)
        outputs = self.gan.discriminator(decoder_output)
        loss = self.criterion(outputs, torch.Tensor(numpy.ones((1))).cuda())
        loss.backward()
        self.optimizer.step()

        return loss.item(), loss_d.item()

    def train_step_discrim(self) -> float:
        shape = list(bottleneck_size)
        shape.insert(0, 1)
        inputs = torch.Tensor(numpy.random.random(shape)).cuda()
        self.optimizer.zero_grad()
        outputs = self.gan(inputs)
        loss = self.criterion(outputs, torch.Tensor(numpy.zeros((1))).cuda())
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def train_epoch(self, dataset: DatasetInference) -> (int, int):
        lv = 0.0
        ld = 0.0
        lvd = 0.0
        acc_discrim = 0
        acc_vae = 0
        counter = 0
        for i in dataset.case_list:
            for j in range(i.data.shape[0]):
                c = i.data[j:j + 1]
                loss_v_di, loss_v_de = self.train_step_vae(c)
                loss_d = self.train_step_discrim()

                if loss_v_di < 0.05:
                    acc_vae += 1
                if loss_d < 0.05:
                    acc_discrim += 1
                lvd += loss_v_de
                lv += loss_v_di
                ld += loss_d
                counter += 1
                if ((lv / counter) - (ld / counter)) < threshold:
                    self.derfreeze_discriminator(True)
                    self.defreeze_decoder(True)
                else:
                    if lv / counter > (ld / counter) + threshold:
                        self.defreeze_decoder(False)
                    else:
                        self.derfreeze_discriminator(False)
                if counter % 200 == 0:
                    print(
                        f"Batch: {counter:09d} av: {(acc_vae / counter):05f} lv: {(lv / counter):05f} ad: {(acc_discrim / counter):05f} ld: {(ld / counter):05f} lvd: {(lvd / counter):05f}")
        return (acc_vae + acc_discrim) / (counter * 2), (ld + lv) / (counter * 2)

    def train(self, dataset: DatasetInference, path: str):
        if not torch.cuda.is_available():
            print("At cpu it will train very slow, so code nonsupport it")
            return
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
                if c > early_stopping:
                    break

    def save_checkpoint(self, epoch: int, path: str):
        p = Path(path)
        p_d = p / f"ep{epoch:03d}"
        p_d.mkdir(parents=True, exist_ok=True)
        torch.save(self.gan.coder.state_dict(), p_d / "coder.pt")
        torch.save(self.gan.decoder.state_dict(), p_d / "decoder.pt")
        torch.save(self.gan.discriminator.state_dict(), p_d / "discriminator.pt")
