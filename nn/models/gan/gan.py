import numpy.random
import torch
import torch.nn as tnn
from torch.nn import Linear, Flatten
from torchsummary import summary
import numpy as np

from nn.models.parts import *
from nn.models.vae.vae import Coder, Decoder

attempts_number = 5

np.random.seed(42)

bottleneck_size = (512, 32, 32)

model_device = "cpu"
if torch.cuda.is_available():
    model_device = "cuda"

class Discriminator(tnn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()

        self.inc = DoubleConv(1, 32)
        self.down1 = Down(32, 64)
        self.down2 = Down(64, 64)
        self.down3 = Down(64, 128)
        self.down4 = Down(128, 64)
        self.down5 = Down(64, 32)
        self.flat = Flatten(1, 3)
        self.pyr1 = Linear(32 * 16 * 16, 1)

    def forward(self, x):
        x = self.inc(x)
        x = self.down1(x)
        x = self.down2(x)
        x = self.down3(x)
        x = self.down4(x)
        x = self.down5(x)
        x = self.flat(x)
        x = self.pyr1(x)
        return x


class GAN(tnn.Module):
    def __init__(self):
        super(GAN, self).__init__()
        self.coder = Coder()
        self.decoder = Decoder()
        self.discriminator = Discriminator()

        self.coder.to(model_device)
        self.to(model_device)
        print("Coder")
        summary(self.coder, (1, 512, 512))
        print("GAN")
        summary(self, bottleneck_size)

    def forward(self, x):
        x = self.decoder(x)
        x = self.discriminator(x)
        return x

    def generate(self, x: torch.Tensor) -> numpy.array:
        best = None
        score = 0
        m = self.coder(x).cpu().detach().numpy()
        for i in range(attempts_number):
            bias = numpy.random.random(bottleneck_size) / 10
            r = self.decoder(torch.Tensor(m + bias).cuda())
            s = float(self.discriminator(r).cpu().detach().numpy())
            if s > score:
                best = r.cpu().detach().numpy()
        return best
