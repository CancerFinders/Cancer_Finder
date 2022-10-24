from nn.unet.unet import UNet


class UNetInferencer:
    unet: UNet

    def __init__(self, unet: UNet):
        self.unet = unet

    def predict(self, data):
        pass
