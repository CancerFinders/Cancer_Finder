import torch.nn as tnn
import torch.optim as optim

from nn.models.unet.unet import UNet


class UNetTrainer:
    unet: UNet

    def __init__(self, model: UNet):
        self.unet = model
        self.criterion = tnn.CrossEntropyLoss()
        self.optimizer = optim.SGD(self.unet.parameters(), lr=0.001, momentum=0.9)

    # return loss
    def train_step(self, batch) -> float:
        inputs, labels = batch

        # zero the parameter gradients
        self.optimizer.zero_grad()

        # forward + backward + optimize
        outputs = self.unet(inputs)
        loss = self.criterion(outputs, labels)
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def train_epoch(self, dataset):
        pass

    def train(self, dataset):
        pass

