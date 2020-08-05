#!/usr/bin/env python3

import random
import pickle

import torch
from torch.autograd import Variable
from torch.quantization import QuantStub, DeQuantStub
from torch.nn import functional as F


_DIM_INPUT = 40  # [SKIP: 14 bytes Ethernet header] + 20 bytes IP + 20 bytes TCP
_DIM_OUTPUT = 1  # it's a binary classifier


def read_file(fname):
    with open(fname, "rb") as pkfile:
        data = pickle.load(pkfile)
        return [d[14:54] for d in data if d[23] == 6]  # TCP packets only


def read_data(dtype=torch.float32):

    data_spam = read_file("data/nmap.pk")
    data_ham = read_file("data/scp.pk")

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


def evaluate(model, data, criterion):
    loss = 0.0
    with torch.no_grad():
        for (x, y_target) in data:
            y = model(x)
            loss += criterion(y, y_target)
    return loss


def train(x_data, y_data):

    # model = LinearRegression(_DIM_INPUT, _DIM_OUTPUT)
    # criterion = torch.nn.MSELoss()

    model = LogisticRegression(_DIM_INPUT, _DIM_OUTPUT)
    criterion = torch.nn.BCELoss(reduction="sum")

    optimizer = torch.optim.Adagrad(model.parameters())

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
            print('epoch {}, loss {}'.format(epoch, loss.item() / len(x_data)))

    return model


def quantize(model, x_data, y_data):

    torch.backends.quantized.engine = 'qnnpack'
    model.qconfig = torch.quantization.default_qconfig
    model = torch.quantization.prepare(model, inplace=False)

    # test_idx = torch.randint(0, len(x_data), [1000])
    # (x_test, y_test) = (x_data[test_idx], y_data[test_idx])
    (x_test, y_test) = (x_data, y_data)
    num_correct = (y_test == (model(x_test) > 0.5)).sum()
    print("\nTest on %d samples: %d spam, predicted correctly %d or %.2f%%\n" % (
        len(y_test), y_test.sum(), num_correct, num_correct * 100.0 / len(y_test)))

    model = torch.quantization.convert(model, inplace=False)

    return model


if __name__ == "__main__":

    x_data, y_data = read_data()
    print("Read data: X: %s Y: %s\n" % (x_data.shape, y_data.shape))

    model = train(x_data, y_data)

    # (x_test, y_test) = (x_data, y_data)
    # num_correct = (y_test == (model(x_test) > 0.5)).sum()
    # print("\nTest on %d samples: %d spam, predicted correctly %d or %.2f%%\n" % (
    #     len(y_test), y_test.sum(), num_correct, num_correct * 100.0 / len(y_test)))

    model = quantize(model, x_data, y_data)

    print(model, "\n")

    for (key, val) in model.state_dict().items():
        print(key, "=", val)

    print("\n*** Quantized weights:")

    w = model.linear.weight()
    qw = (w.dequantize() / w.q_scale() + w.q_zero_point()).int()
    qb = (model.linear.bias() / w.q_scale() + w.q_zero_point()).int()

    print("w =", qw[0].tolist())
    print("bias =", int(qb))

    # print("\n*** Export to ONNX:\n")

    # # Glow does not support dynamic dimensions - make sure sample size is 1.
    # torch.onnx.export(
    #     model, x_data[:1], "model/logistic_34b_v1.onnx", verbose=True,
    #     input_names=["input", "weights", "bias"], output_names=["output"])
