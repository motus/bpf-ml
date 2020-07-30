#!/usr/bin/env python3

import random
import pickle

import torch
from torch.autograd import Variable
from torch.quantization import QuantStub, DeQuantStub
from torch.nn import functional as F


_DIM_INPUT = 34  # 14 bytes Ethernet header + 20 bytes IP
_DIM_OUTPUT = 1  # it's a binary classifier


def _read_file(fname, trim=_DIM_INPUT):
    with open(fname, "rb") as pkfile:
        data = pickle.load(pkfile)
        return [d[:trim] for d in data]


def _read_data(dtype=torch.float32):

    data_spam = _read_file("data/nmap.pk")
    data_ham = _read_file("data/wget.pk")

    x_data = data_spam + data_ham
    y_data = [[1]] * len(data_spam) + [[0]] * len(data_ham)

    data = list(zip(x_data, y_data))
    random.shuffle(data)

    return (torch.tensor([d[0] for d in data], dtype=dtype),
            torch.tensor([d[1] for d in data], dtype=dtype))


class LinearRegression(torch.nn.Module):

    def __init__(self, input_dim, output_dim):
        super(LinearRegression, self).__init__()
        self.linear = torch.nn.Linear(input_dim, output_dim)
        self.quant = QuantStub()
        self.dequant = DeQuantStub()

    def forward(self, x):
        x = self.quant(x)
        y = self.linear(x)
        y = self.dequant(y)
        return y


class LogisticRegression(torch.nn.Module):

    def __init__(self, input_dim, output_dim):
        super(LogisticRegression, self).__init__()
        self.linear = torch.nn.Linear(input_dim, output_dim)
        self.quant = QuantStub()
        self.dequant = DeQuantStub()

    def forward(self, x):
        x = self.quant(x)
        y = self.linear(x)
        y = torch.sigmoid(y)
        y = self.dequant(y)
        return y


def _evaluate(model, data, criterion):
    loss = 0.0
    with torch.no_grad():
        for (x, y_target) in data:
            y = model(x)
            loss += criterion(y, y_target)
    return loss


def _train(x_data, y_data):

    data_size = len(x_data)

    # model = LinearRegression(_DIM_INPUT, _DIM_OUTPUT)
    # criterion = torch.nn.MSELoss()

    model = LogisticRegression(_DIM_INPUT, _DIM_OUTPUT)
    criterion = torch.nn.BCELoss(reduction="sum")

    optimizer = torch.optim.SGD(model.parameters(), lr=0.015)

    for epoch in range(1000):
        model.train()
        optimizer.zero_grad()
        # Forward pass
        y_pred = model(x_data)
        # Compute Loss
        loss = criterion(y_pred, y_data)
        # Backward pass
        loss.backward()
        optimizer.step()
        if epoch % 100 == 0:
            print('epoch {}, loss {}'.format(epoch, loss.item() / data_size))

    torch.backends.quantized.engine = 'qnnpack'
    model.qconfig = torch.quantization.default_qconfig
    torch.quantization.prepare(model, inplace=True)

    test_idx = torch.randint(0, len(x_data), [1000])
    # Also serves as calibration for the dynamic quantization:
    acc = _evaluate(model, zip(x_data[test_idx], y_data[test_idx]), lambda a, b: abs(a - b))
    print("\nAccuracy: %.2f%%\n" % (acc * 100.0 / len(test_idx)))

    torch.quantization.convert(model, inplace=True)

    return model


if __name__ == "__main__":

    x_data, y_data = _read_data()
    print("Read data: X: %s Y: %s\n" % (x_data.shape, y_data.shape))

    model = _train(x_data, y_data)

    print(model, "\n")

    for (key, val) in model.state_dict().items():
        print(key, "=", val)

    # Glow does not support dynamic dimensions - make sure sample size is 1.
    torch.onnx.export(
        model, x_data[:1], "model/logistic_34b_v1.onnx", verbose=True,
        input_names=["input", "weights", "bias"], output_names=["output"])
