import torch.nn as tnn
from torchsummary import summary


class DoubleConv(tnn.Module):
    """(convolution => [BN] => ReLU) * 2"""

    def __init__(self, in_channels, out_channels, mid_channels=None):
        super().__init__()
        if not mid_channels:
            mid_channels = out_channels
        self.double_conv = tnn.Sequential(
            tnn.Conv2d(in_channels, mid_channels, kernel_size=3, padding=1, bias=False),
            tnn.BatchNorm2d(mid_channels),
            tnn.ReLU(inplace=True),
            tnn.Conv2d(mid_channels, out_channels, kernel_size=3, padding=1, bias=False),
            tnn.BatchNorm2d(out_channels),
            tnn.ReLU(inplace=True)
        )

    def forward(self, x):
        return self.double_conv(x)


class Down(tnn.Module):
    """Downscaling with maxpool then double conv"""

    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.maxpool_conv = tnn.Sequential(
            tnn.MaxPool2d(2),
            DoubleConv(in_channels, out_channels)
        )

    def forward(self, x):
        return self.maxpool_conv(x)


class Up(tnn.Module):
    """Upscaling then double conv"""

    def __init__(self, in_channels, out_channels, bilinear=True):
        super().__init__()
        if bilinear:
            self.up = tnn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
            self.conv = DoubleConv(in_channels, out_channels, in_channels // 2)
        else:
            self.up = tnn.ConvTranspose2d(in_channels, in_channels // 2, kernel_size=2, stride=2)
            self.conv = DoubleConv(in_channels, out_channels)

    def forward(self, x):
        return self.conv(self.up(x))


class OutConv(tnn.Module):
    def __init__(self, in_channels, out_channels):
        super(OutConv, self).__init__()
        self.conv = tnn.Conv2d(in_channels, out_channels, kernel_size=1)

    def forward(self, x):
        return self.conv(x)


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
        self.bottleneck = DoubleConv(512, 512, 256)
        # self.up0 = Up(512, 512)
        self.up1 = Up(512, 256)
        self.up2 = Up(256, 128)
        self.up3 = Up(128, 64)
        self.up4 = Up(64, 32)
        self.outc = OutConv(32, 1)

    def forward(self, x):
        x = self.bottleneck(x)
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
