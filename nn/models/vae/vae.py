from nn.models.parts import *
from torchsummary import summary


class Coder(tnn.Module):
    def __init__(self):
        super(Coder, self).__init__()

        self.inc = DoubleConv(1, 32)
        self.down1 = Down(32, 64)
        self.down2 = Down(64, 128)
        self.down3 = Down(128, 256)
        self.down4 = Down(256, 512)
        # self.down5 = Down(512, 512)

    def forward(self, x):
        x = self.inc(x)
        x = self.down1(x)
        x = self.down2(x)
        x = self.down3(x)
        x = self.down4(x)
        # x = self.down5(x)
        return x


class Decoder(tnn.Module):
    def __init__(self):
        super(Decoder, self).__init__()
        # self.bottleneck = DoubleConv(512, 512, 256)
        # self.up0 = Up(512, 512)
        self.up1 = Up(512, 256)
        self.up2 = Up(256, 128)
        self.up3 = Up(128, 64)
        self.up4 = Up(64, 32)
        self.outc = OutConv(32, 1)

    def forward(self, x):
        # x = self.bottleneck(x)
        # x = self.up0(x)
        x = self.up1(x)
        x = self.up2(x)
        x = self.up3(x)
        x = self.up4(x)
        logits = self.outc(x)
        return logits


class VAE(tnn.Module):
    def __init__(self):
        super(VAE, self).__init__()
        self.coder = Coder()
        self.decoder = Decoder()
        self.to("cuda")
        summary(self, (1, 512, 512))

    def forward(self, x):
        x = self.coder(x)
        return self.decoder(x)
