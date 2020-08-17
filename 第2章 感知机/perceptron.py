'''
2020-8-17
Yanjie Ze
'''

import numpy as np

# 定义了感知机类,使用感知机学习算法的原始形式
class perceptron:
    def __init__(self, dimension, learning_rate=0.1):
        self.dimension = dimension
        self.w = np.zeros(dimension)
        self.b = np.zeros(1)
        self.learning_rate = learning_rate

    def f(self,x):
        fx = np.dot(x, self.w) + self.b
        return fx

    def fit(self, x_train, y_train):
        dataNum = len(x_train)
        allRight = False
        while not allRight:
            errorCount = 0
            for i in range(dataNum):
                x = x_train[i]
                y = y_train[i]
                if y * self.f(x) <= 0:
                    #更新参数
                    self.w = self.w + self.learning_rate * np.dot(y,x)
                    self.b = self.b + self.learning_rate * y
                    errorCount += 1
            if errorCount == 0:
                    allRight = True
        return allRight



if __name__ == '__main__':

    model = perceptron(dimension=2)
    # 书中的数据
    x_train = np.array([[3,3],[4,3],[1,1]])
    y_train = np.array([1,1,-1])

    success = model.fit(x_train=x_train, y_train=y_train)
    if success:
        print(model.w, "x+", model.b)
