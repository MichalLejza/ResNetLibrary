import torch
import torch.nn as nn
import torch.nn.functional as F
from Models.ResNet import ResNet
from Models.Blocks import BasicBlock


class ResNet18(ResNet):
    def __init__(self):
        super().__init__()

    def __make_layer(self):
        pass

    def foward(self, x):
        pass
