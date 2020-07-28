#!/usr/bin/env python3

import random
import pickle

import torch
from torch.autograd import Variable
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
        self.linear = torch.nn.Linear(_DIM_INPUT, _DIM_OUTPUT)

    def forward(self, x):
        y_pred = self.linear(x)
        return y_pred


class LogisticRegression(torch.nn.Module):

    def __init__(self, input_dim, output_dim):
        super(LogisticRegression, self).__init__()
        self.linear = torch.nn.Linear(_DIM_INPUT, _DIM_OUTPUT)

    def forward(self, x):
        y_pred = torch.sigmoid(self.linear(x))
        return y_pred


def _main():

    x_data, y_data = _read_data()
    data_size = len(x_data)
    print("Read data: X: %s Y: %s\n" % (x_data.shape, y_data.shape))

    # model = LinearRegression(input_dim, output_dim)
    model = LogisticRegression(_DIM_INPUT, _DIM_OUTPUT)
    # criterion = torch.nn.MSELoss()
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

    test_idx = 10
    new_x = x_data[test_idx]
    y_pred = model(new_x)
    print("predicted Y value: %f actual: %f" % (y_pred.data, y_data[test_idx]))

    input_names = ["actual_input_1"] + ["learned_%d" % i for i in range(2)]
    output_names = ["output1"]

    # Glow does not support dynamic dimensions - make sure sample size is 1.
    torch.onnx.export(
        model, x_data[:1], "model/lr_34b_v0.onnx", verbose=True,
        input_names=input_names, output_names=output_names)


if __name__ == "__main__":
    _main()
