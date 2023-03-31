import torch

from vocabulary import Dimension


class Flatten:
    def __init__(self, architecture):
        self.flatten_block = FlattenBlock(architecture)

    def pytorch(self):
        return self.flatten_block.pytorch()


class FlattenBlock:
    def __init__(self, block):
        self.start_dim = block[Dimension.Start]
        self.end_dim = block[Dimension.End]

    def pytorch(self):
        return torch.nn.Flatten(start_dim=self.start_dim, end_dim=self.end_dim)
