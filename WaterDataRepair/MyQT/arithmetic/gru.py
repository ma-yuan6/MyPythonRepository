import pandas as pd
import numpy as np
import torch
import torch.nn as nn


# 定义 GRU 模型
class GRUModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(GRUModel, self).__init__()
        self.hidden_size = hidden_size
        self.gru = nn.GRU(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.gru(x)
        out = self.fc(out[:, -1, :])
        return out


def prepare_data(file_path):
    """"数据预处理"""
    testdata = pd.read_csv(file_path, header=None)
    data = testdata[2]
    date = testdata[0]

    total_data = len(data)
    print(total_data)

    # 设置每个输入序列的长度（这里设为5）
    input_sequence_length = 5

    # 准备训练数据
    X_train = []
    y_train = []

    for i in range(total_data - input_sequence_length):
        X_train.append(data[i:i + input_sequence_length])
        y_train.append(data[i + input_sequence_length])

    X_train = np.array(X_train)
    y_train = np.array(y_train)

    # 打印出训练数据的形状
    print("训练数据 X 的形状:", X_train.shape)
    print("训练数据 y 的形状:", y_train.shape)

    # 准备测试数据（使用后96个数据）
    X_test = []
    y_test = []

    plot_date = date[-96:]
    print(plot_date.shape)

    for i in range(total_data - 96 - input_sequence_length, total_data - input_sequence_length):
        X_test.append(data[i:i + input_sequence_length])
        y_test.append(data[i + input_sequence_length])

    X_test = np.array(X_test)
    y_test = np.array(y_test)
    return X_train, y_train, X_test, y_test, data, plot_date


def train(train_data, plot_date, epochs):
    """
    训练模型
    :param train_data:训练集数据、标签,测试集数据、标签
    :param plot_date:y轴刻度
    :return:
    """
    X_train, y_train, X_test, y_test = train_data
    # 打印出测试数据的形状
    print("测试数据 X 的形状:", X_test.shape)
    print("测试数据 y 的形状:", y_test.shape)

    # 将 numpy 数据转换为 PyTorch 张量
    X_train = torch.from_numpy(X_train).float()
    y_train = torch.from_numpy(y_train).float()
    X_test = torch.from_numpy(X_test).float()
    y_test = torch.from_numpy(y_test).float()

    # 定义模型参数
    input_size = 1
    hidden_size = 64
    output_size = 1

    # 初始化模型
    model = GRUModel(input_size, hidden_size, output_size)

    # 定义损失函数和优化器
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # 训练模型
    epochs = epochs
    losses = []

    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(X_train.unsqueeze(-1))
        loss = criterion(outputs.squeeze(), y_train)
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
        print(f'Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}')

    # 测试模型
    with torch.no_grad():
        test_outputs = model(X_test.unsqueeze(-1))
        test_loss = criterion(test_outputs.squeeze(), y_test)
        print('测试集上的损失:', test_loss.item())

        return plot_date, y_test.numpy(), test_outputs.numpy(),


if __name__ == '__main__':
    *data, date = preprocess_data('../../data/data.csv')
    train(data, date, 2)
