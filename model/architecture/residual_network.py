from model.architecture.layers import Conv2d, Pool, ActivationFunction


class ResNet:
    def __init__(self, architecture):
        body = [BodyBlock(block) for block in architecture[1:-1]]
        self.architecture = [InputBlock(architecture[0])] + body + [OutputBlock(architecture[-1])]


class InputBlock:
    def __init__(self, block):
        self.conv = Conv2d(block["kernel_conv"], block["in_channels"], block["out_channels"],
                           block["stride_conv"], block["padding_conv"])
        self.pool = Pool(block["kernel_pool"], block["stride_pool"],
                         block["padding"], block["pool_type"])

    def pytorch(self):
        return self.conv.pytorch(), self.pool.pytorch()


class BodyBlock:
    def __init__(self, residual_blocks):
        self.stages = [Stage([ResidualBlock(block) for _ in range(block["number"])]) for block in residual_blocks]

    def pytorch(self):
        return [stage.pytorch() for stage in self.stages]


class Stage:
    def __init__(self, residual_blocks):
        self.blocks = residual_blocks

    def pytorch(self):
        return [block.pytorch() for block in self.blocks]


class ResidualBlock:
    def __init__(self, block):
        self.conv1 = Conv2d(block["kernel_conv"], block["in_channels"],
                            block["out_channels"], block["stride"], block["padding"])
        self.activation = ActivationFunction(block["activation_function"])
        self.conv2 = Conv2d(block["kernel_conv"], block["in_channels"],
                            block["out_channels"], block["stride"], block["padding"])

    def pytorch(self):
        return self.conv1.pytorch(), self.activation.pytorch(), self.conv2.pytorch()


class OutputBlock:
    def __init__(self, block):
        self.activation = Pool(block["kernel_pool"], block["stride_pool"],
                               block["padding_pool"], block["pooling_type"])

    def pytorch(self):
        return self.activation.pytorch()
