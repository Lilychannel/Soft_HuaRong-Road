import numpy as np
import sys
from Prediction import Prediction

class Qipan:
    def __init__(self):
        self.n=3
        self.N=self.n*self.n
        self.init=np.arange(1,self.N+1).reshape(self.n,self.n)
        self.qipan = self.init.copy()
        self.bk_x=0 # 打乱后的空格位置一定要改
        self.bk_y=2 # 打乱后的空格位置一定要改。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。
        self.bk_x_p=-1
        self.bk_y_p=-1
        self.pre=Prediction()
        self.started=False  #标记是否开始
        self.X=[-1,0,1,0]
        self.Y=[0,-1,0,1]
        self.dir = []

    def make_qipan(self):  #生成棋盘
        print("请输入待解数组")
        string = sys.stdin.readline().strip()
        arr = []
        count = 0
        for i in string:
            try:
                arr.append(int(i))
            except:
                if i == '[':
                    count += 1
                pass
        cols = int(len(arr) / count)
        grid = []
        cur = []
        for i in arr:
            if len(cur) <= cols:
                cur.append(i)
            else:
                grid.append(cur)
                cur = []
                cur.append(i)
        grid.append(cur)
        self.qipan=grid
        self.step=0  #提示计步
        self.started=True  #标记是否开始

    def move(self,x,y):  #移动棋子
        if x<0 or x>=self.n or y<0 or y>=self.n:
            return
        self.qipan[self.bk_x][self.bk_y]=self.qipan[x][y]       # 交换值
        self.qipan[x][y]=1      # 空格位置的值。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。
        self.bk_x_p=self.bk_x   #交换位置
        self.bk_y_p=self.bk_y
        self.bk_x=x
        self.bk_y=y

    def change_move(self,a,b,c,d):  # 交换棋子
        t = self.qipan[a][b]
        self.qipan[a][b] = self.qipan[c][d]
        self.qipan[c][d] = t

    def is_finish(self):  #判断游戏是否结束
        for i in range(self.n):
            for j in range(self.n):
                if self.qipan[i][j]!=self.init[i][j]:
                    return False
        print("".join(self.dir))
        return True

    def show(self):  #打印当前棋盘状态
        s=""
        for i in range(self.n):
            for j in range(self.n):
                if self.qipan[i][j]==1:     # 当位置是空格处的值时，打印空格。。。。。。。。。。。。。。。。。。。。
                    s+="  "
                else:
                    s+=str(self.qipan[i][j])+" "
            s+="\n"
        print(s)

    def direction(self,i):
        if i == 0:
            print("w")
            dire = 'w'
        if i == 1:
            print("a")
            dire = 'a'
        if i == 2:
            print("s")
            dire = 's'
        if i == 3:
            print("d")
            dire = 'd'
        self.dir.append(dire)

    def tips(self):
        if self.step != 13-1: # 不在强制交换的步数中....................................................................
            i = self.pre.pre_next(self.qipan, self.bk_x, self.bk_y, self.bk_x_p, self.bk_y_p)
            x = self.bk_x + self.X[i]
            y = self.bk_y + self.Y[i]
            self.move(x, y)
            self.direction(i)
            self.step += 1
            print("step", self.step)
            print("进行交换的棋子：", "(", x, ",", y, ")")
            self.show()
        else: # 在强制交换的步数中
            self.show()
            print("请输入要交换的值的坐标：两个")
            print("第一个")
            a, b = map(eval, input('两个值:').split())
            print("第二个")
            c, d = map(eval, input('两个值:').split())
            self.change_move(a,b,c,d)      # 移动强制交换的两个值
            s = self.pre.pre_step(self.qipan) # 移动后确定是否有解
            if s == -1: #强制交换后无解
                print("无解,需要进行手动交换")
                # 打印棋盘
                self.show()
                print("请选择需要交换的数值")
                # 输入两个值
                p = -1 # 因为无解返回-1
                while(p == -1): # 当为-1即为无解时，进入循环
                    print("请输入要交换的值的坐标：两个")
                    print("第一个")
                    g, h = map(eval, input('两个值:').split())
                    print("第二个")
                    z, c = map(eval, input('两个值:').split())
                    self.change_move(g,h,z,c)
                    p = self.pre.pre_step(self.qipan)    # 如果有解那p将不为-1，退出循环
                    self.change_move(z,c,g,h)
                # 退出循环说明有解了
                print("开始正常运行")
                self.change_move(g,h,z,c)
                i = self.pre.pre_next(self.qipan, self.bk_x, self.bk_y, self.bk_x_p, self.bk_y_p)
                x = self.bk_x + self.X[i]
                y = self.bk_y + self.Y[i]
                self.move(x, y)
                self.direction(i)
                self.step += 1
                print("step", self.step)
                print("进行交换的棋子：", "(", x, ",", y, ")")
                self.show()
            else: #强制交换后有解
                i = self.pre.pre_next(self.qipan, self.bk_x, self.bk_y, self.bk_x_p, self.bk_y_p)
                x = self.bk_x + self.X[i]
                y = self.bk_y + self.Y[i]
                self.move(x, y)
                self.direction(i)
                self.step += 1
                print("step", self.step)
                print("进行交换的棋子：", "(", x, ",", y, ")")
                self.show()


