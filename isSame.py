# coding=gbk
from PIL import Image
import numpy as np
import os
# import scipy
import matplotlib.pyplot as plt


def ImageToMatrix(filename):
    # 读取图片
    im = Image.open(filename)
    # 显示图片
    #     im.show()
    width, height = im.size
    im = im.convert("L")
    data = im.getdata()
    data = np.matrix(data, dtype='float') / 255.0
    # new_data = np.reshape(data,(width,height))
    new_data = np.reshape(data, (height, width))
    return new_data


#     new_im = Image.fromarray(new_data)
#     # 显示图片
#     new_im.show()
def MatrixToImage(data):
    data = data * 255
    new_im = Image.fromarray(data.astype(np.uint8))
    return new_im

def sss4():
    l = []
    path = 'D:\pycharm\三阶数字华容道最优解（更新版）/三阶数字华容道最优解（更新版）/img2/img/'
    for i in range(1,10):
        filename = path + str(i) + '.png'
        data = ImageToMatrix(filename)
        # print(data)
        l.append(data)

    l2= []
    path = 'D:/pycharm/三阶数字华容道最优解（更新版）/三阶数字华容道最优解（更新版）/wukuang/cut/'
    for i in range(1, 10):
        filename = path + str(i) + '.png'
        data = ImageToMatrix(filename)
        # print(data)
        l2.append(data)
    game=[]
    game1=[]
    count = 0
    for i in range(0,9):
        for j in range(0,9):
            if (l[i] == l2[j]).all():
                game.append(j + 1)
                count = count + 1



    if count == 8:
        print(game)
        return True
    else:
        return False

