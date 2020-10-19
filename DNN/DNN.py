import tensorflow as tf
import numpy as np
from keras.utils import to_categorical

class DNN:
    def __init__(self,data,label,lr=0.01,train_step=1000):
        self.n=3  #阶数
        self.N=self.n*self.n  #棋子个数（包含空格）
        self.data=data #训练集
        self.label=to_categorical(label)  #标签(one_hot编码)
        self.size=len(label)  #训练集大小
        self.batch_size=425  #训练批次大小
        self.batch_num=self.size//self.batch_size+1  #训练批次数
        self.lr=lr  #学习率
        self.train_step=train_step  #训练步数
        
    #生成每一批次的样本    
    def next_batch(self,batch_size):
        index=np.random.randint(0,self.size,batch_size)
        return self.data[index],self.label[index]

    #初始化权值函数
    def weight_variable(self,shape):
        initial=tf.truncated_normal(shape,stddev=0.1)
        return tf.Variable(initial)
     
    #初始化偏置值函数
    def bias_vairable(self,shape):
        initial=tf.constant(0.1,shape=shape)
        return tf.Variable(initial)
       
    def train(self):
        x=tf.placeholder(tf.float32,[None,9])
        y=tf.placeholder(tf.float32,[None,32])
        w_fc1=self.weight_variable([9,500])
        b_fc1=self.bias_vairable([500])
        w_fc2=self.weight_variable([500,500])
        b_fc2=self.bias_vairable([500])
        w_fc3=self.weight_variable([500,500])
        b_fc3=self.bias_vairable([500])
        w_fc4=self.weight_variable([500,32])
        b_fc4=self.bias_vairable([32])
        h_fc1=tf.nn.tanh(tf.matmul(x,w_fc1)+b_fc1)
        h_fc2=tf.nn.sigmoid(tf.matmul(h_fc1,w_fc2)+b_fc2)
        h_fc3=tf.nn.relu(tf.matmul(h_fc2,w_fc3)+b_fc3)
        h_fc4=tf.matmul(h_fc3,w_fc4)+b_fc4
        loss=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y,logits=h_fc4))
        train=tf.train.AdamOptimizer(self.lr).minimize(loss)
        accuracy=tf.reduce_mean(tf.cast(tf.equal(tf.argmax(h_fc4,1),tf.argmax(y,1)),tf.float32))
        mse=tf.reduce_mean(tf.cast(tf.square(tf.argmax(h_fc4,1)-tf.argmax(y,1)),tf.float32))
        init=tf.global_variables_initializer() 
        with tf.Session() as sess:
            sess.run(init)
            x_test,y_test=self.next_batch(50000)
            for epoch in range(self.train_step):
                for i in range(self.batch_num):
                    x_,y_=self.next_batch(self.batch_size)
                    sess.run(train,feed_dict={x:x_,y:y_})
                acc,m=sess.run([accuracy,mse],feed_dict={x:x_test,y:y_test})
                print("epoch:",epoch,"accuracy:",acc,"mse:",m)
                self.w_fc1,self.b_fc1,self.w_fc2,self.b_fc2,self.w_fc3,self.b_fc3,self.w_fc4,self.b_fc4=\
                sess.run([w_fc1,b_fc1,w_fc2,b_fc2,w_fc3,b_fc3,w_fc4,b_fc4],feed_dict={x:x_test,y:y_test})
        
    def predict(self,x):
        h_fc1=tf.nn.tanh(tf.matmul(x,self.w_fc1)+self.b_fc1)
        h_fc2=tf.nn.sigmoid(tf.matmul(h_fc1,self.w_fc2)+self.b_fc2)
        h_fc3=tf.nn.relu(tf.matmul(h_fc2,self.w_fc3)+self.b_fc3)
        h_fc4=tf.matmul(h_fc3,self.w_fc4)+self.b_fc4
        pre=tf.argmax(h_fc4,1)
        with tf.Session() as sess:
            pre=sess.run(pre)
        return pre
        
    def save_para(self):
        np.savez("jie3_dnn.npz",w_fc1=self.w_fc1,b_fc1=self.b_fc1,w_fc2=self.w_fc2,b_fc2=self.b_fc2,\
                 w_fc3=self.w_fc3,b_fc3=self.b_fc3,w_fc4=self.w_fc4,b_fc4=self.b_fc4)
        

temp=np.load('jie3.npz')
data=temp['data']
label=temp['label']   
dnn=DNN(data,label,0.002,200)
dnn.train()
dnn.save_para()
x=np.array([[1,2,3,4,5,9,7,8,6]],dtype='float32')
step=dnn.predict(x)