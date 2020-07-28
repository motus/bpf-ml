import torch
from torch.autograd import Variable
from torch.nn import functional as F

# x_data = Variable(torch.Tensor([[10.0], [9.0], [3.0], [2.0]]))
# y_data = Variable(torch.Tensor([[90.0], [80.0], [50.0], [30.0]]))

torch.manual_seed(1)
input_dim = 1
output_dim = 1
data_size = 10
x_data = torch.randn(100, 1) * data_size
y_data = torch.FloatTensor(map(lambda x: 1 if x > 0 else 0, x_data))

print x_data, y_data


class LinearRegression(torch.nn.Module):
    def __init__(self, input_dim, output_dim):
        super(LinearRegression, self).__init__()
        self.linear = torch.nn.Linear(input_dim, output_dim)

    def forward(self, x):
        y_pred = self.linear(x)
        return y_pred


class LogisticRegression(torch.nn.Module):
    def __init__(self, input_dim, output_dim):
        super(LogisticRegression, self).__init__()
        self.linear = torch.nn.Linear(input_dim, output_dim)

    def forward(self, x):
        y_pred = torch.sigmoid(self.linear(x))
        return y_pred


# model = LinearRegression(input_dim, output_dim)
model = LogisticRegression(input_dim, output_dim)
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

new_x = Variable(torch.Tensor([[-5.0], [4.0]]))
y_pred = model(new_x)
print("predicted Y value: ", y_pred.data)

input_names = ["actual_input_1"] + ["learned_%d" % i for i in range(2)]
output_names = ["output1"]
torch.onnx.export(model, x_data, "alexnet.onnx", verbose=True,
                  input_names=input_names, output_names=output_names)
