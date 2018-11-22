version = 'linear_v2.2'
import sys
import pickle
import os
import tensorflow as tf
import numpy as np
from scipy.io import wavfile

def notetofrq(note, A4=440):
    octave = int(note[0])-4
    note = note[1:]
    table = {'C':-9, 'C#':-8, 'D':-7, 'D#':-6, 'E':-5, 'F':-4, 'F#':-3, 'G':-2, 'G#':-1, 'A':0, 'A#':1, 'B':2}
    return A4*2**(octave+float(table[note]/12))
FileName = sys.argv[1]
fs, y = wavfile.read(FileName)
AudioFileName = os.path.basename(FileName)[:os.path.basename(FileName).rfind('.')]
PlayingStyle = AudioFileName[5:AudioFileName.find('_')]#first 5 letters are '151VN'
Dynamics = AudioFileName[AudioFileName.find('_')-1:AudioFileName.find('_')]
String = AudioFileName[AudioFileName.rfind('_')-2:AudioFileName.rfind('_')]
NoteName = AudioFileName[AudioFileName.rfind('_')+1:]
f = notetofrq(NoteName)
N = int(fs/2/f)-1
frameSize = int(fs/f)*2
hopSize = frameSize//2
Frames = int(len(y)//hopSize-1)
num_steps = 1000


#creat tensorflow structure
t = tf.range(frameSize)
t = tf.cast(t, tf.float32)
with tf.name_scope('yt'):
    yt = tf.placeholder(tf.float32, shape=(frameSize,))
with tf.name_scope('A'):
    A = [tf.Variable(0.0) for i in range(N)]
with tf.name_scope('B'):
    B = [tf.Variable(0.0) for i in range(N)]
with tf.name_scope('C'):
    C = tf.Variable(0.0)
with tf.name_scope('w0'):
    w0 = tf.placeholder(tf.float32, shape=(frameSize,))
with tf.name_scope('Weights'):
    W = tf.add(tf.multiply(C, t), w0)
Y = 0.0
for i in range(N):
    Y = tf.add(Y, tf.add(tf.multiply(A[i], tf.sin(tf.multiply(2*np.pi*W*(i+1)/fs, t))), tf.multiply(B[i], tf.cos(tf.multiply(2*np.pi*W*(i+1)/fs, t)))))
with tf.name_scope('Loss'):
    loss = tf.reduce_mean(tf.square(Y-yt))
with tf.name_scope('Train'):
    optimizer = tf.train.AdamOptimizer(learning_rate = 1e-3)
    train = optimizer.minimize(loss)

init = tf.global_variables_initializer()
sess = tf.Session()
writer = tf.summary.FileWriter("TensorBoard/", graph=sess.graph)
w_list = []
A_list = []
B_list = []
for frame in range(10):
    print(frame)
    sess.run(init)
    
    start = frame*hopSize
    end = start+frameSize
    #run
    cur_w0 = np.ones(frameSize, dtype='float32')*f
    for i in range(num_steps):
        sess.run(train, feed_dict={yt:y[start:end], w0:cur_w0})

    A_list.append(sess.run(A))
    B_list.append(sess.run(B))
    w_list += list(sess.run(W,feed_dict={w0:cur_w0}))
    f = w_list[-hopSize]

sess.close()
