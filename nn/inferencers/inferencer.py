from nn.model import MainModel


class Inferencer:
    model: MainModel

    def __init__(self, model: MainModel):
        self.reset_model(model)

    def infer(self, data):
        pass

    def reset_model(self, model):
        self.model = model
