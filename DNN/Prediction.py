import numpy as np
import tensorflow as tf

class Prediction:
    def __init__(self):
        self.n=3
        self.N=self.n*self.n
        temp=np.load('jie3_dnn.npz')
        self.w_fc1=temp['w_fc1']
        self.b_fc1=temp['b_fc1']
        self.w_fc2=temp['w_fc2']
        self.b_fc2=temp['b_fc2']
        self.w_fc3=temp['w_fc3']
        self.b_fc3=temp['b_fc3']
        self.w_fc4=temp['w_fc4']
        self.b_fc4=temp['b_fc4']
        self.X=[-1,0,1,0]
        self.Y=[0,-1,0,1]
        
    def pre_step(self,x):
        x=x.reshape(1,-1).astype('float32')
        h_fc1=tf.nn.tanh(tf.matmul(x,self.w_fc1)+self.b_fc1)
        h_fc2=tf.nn.sigmoid(tf.matmul(h_fc1,self.w_fc2)+self.b_fc2)
        h_fc3=tf.nn.relu(tf.matmul(h_fc2,self.w_fc3)+self.b_fc3)
        h_fc4=tf.matmul(h_fc3,self.w_fc4)+self.b_fc4
        pre=tf.argmax(h_fc4,1)
        with tf.Session() as sess:
            pre=sess.run(pre)
        return pre
     
    def pre_next(self,sta,bk_x,bk_y,bk_x_p,bk_y_p):
        step=[10000,10000,10000,10000]
        for i in range(4):
            x=bk_x+self.X[i]
            y=bk_y+self.Y[i]
            if x<0 or x>=self.n or y<0 or y>=self.n or x==bk_x_p and y==bk_y_p:
                continue
            t=sta[x][y]
            sta[x][y]=self.N
            sta[bk_x][bk_y]=t
            step[i]=self.pre_step(sta)
            sta[x][y]=t
            sta[bk_x][bk_y]=self.N
        return np.argmin(step)
            
            