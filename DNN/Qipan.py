import numpy as np
from Prediction import Prediction


class Qipan:
    def __init__(self):
        self.n = 3
        self.N = self.n * self.n
        self.init = np.arange(1, self.N + 1).reshape(self.n, self.n)
        self.qipan = self.init.copy()
        self.bk_x = self.n - 2
        self.bk_y = self.n - 2
        self.bk_x_p = -1
        self.bk_y_p = -1
        self.pre = Prediction()
        self.started = False  # 标记是否开始
        self.X = [-1, 0, 1, 0]
        self.Y = [0, -1, 0, 1]

    def make_qipan(self):  # 生成随机棋盘
        max_step = np.random.randint(40000, 80000)  # 随机生成移动棋子步数
        step = 0
        while step < max_step or self.qipan[self.n - 2][self.n - 2] != 5:
            i = np.random.randint(4)
            x = self.bk_x + self.X[i]
            y = self.bk_y + self.Y[i]
            self.move(x, y)
            step += 1
        self.bk_x_p = -1
        self.bk_y_p = -1
        self.step = 0  # 提示计步
        self.started = True  # 标记是否开始

    def move(self, x, y):  # 移动棋子
        if x < 0 or x >= self.n or y < 0 or y >= self.n:
            return
        self.qipan[self.bk_x][self.bk_y] = self.qipan[x][y]
        self.qipan[x][y] = 5
        self.bk_x_p = self.bk_x
        self.bk_y_p = self.bk_y
        self.bk_x = x
        self.bk_y = y

    def is_finish(self):  # 判断游戏是否结束
        for i in range(self.n):
            for j in range(self.n):
                if self.qipan[i][j] != self.init[i][j]:
                    return False
        return True

    def show(self):  # 打印当前棋盘状态
        s = ""
        for i in range(self.n):
            for j in range(self.n):
                if self.qipan[i][j] == 5:
                    s += "  "
                else:
                    s += str(self.qipan[i][j]) + " "
            s += "\n"
        print(s)

    def tips(self):  # 提示一步
        i = self.pre.pre_next(self.qipan, self.bk_x, self.bk_y, self.bk_x_p, self.bk_y_p)
        x = self.bk_x + self.X[i]
        y = self.bk_y + self.Y[i]
        self.move(x, y)
        self.step += 1
        print("step", self.step)
        self.show()
