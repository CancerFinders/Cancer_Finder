import torch.nn as tnn


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

