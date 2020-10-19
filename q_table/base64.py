import base64
with open("D:\\pycharm\\三阶数字华容道最优解（更新版）\\三阶数字华容道最优解（更新版）\\q_table\\test.txt","r") as f:
    imgdata = base64.b64decode(f.read())
    file = open('D:\\pycharm\\三阶数字华容道最优解（更新版）\\三阶数字华容道最优解（更新版）\\img2\\img\\test.jpg','wb') # 本地
    file.write(imgdata)
    file.close()
