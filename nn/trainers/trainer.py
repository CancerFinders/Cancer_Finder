from nn.model import MainModel


class Trainer:
    model: MainModel

    def __init__(self, model: MainModel):
        self.reset_model(model)

    def train(self, dataset):
        for batch in dataset:
            self.train_epoch(batch)
            self.valid_epoch(batch)
            self.post_epoch_action()

    def train_epoch(self, batch):
        pass

    def valid_epoch(self, batch):
        pass

    def post_epoch_action(self):
        pass

    def reset_model(self, model):
        self.model = model