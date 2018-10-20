#linear2.2
import sys
import os
import tensorflow as tf
import numpy as np
from scipy.io import wavfile

def notetofrq(note, A4=440):
    octave = int(note[0])-4
    note = note[1:]
    table = {'C':-9, 'C#':-8, 'D':-7, 'D#':-6, 'E':-5, 'F':-4, 'F#':-3, 'G':-2, 'G#':-1, 'A':0, 'A#':1, 'B':2}
    return A4*2**(octave+float(table[note]/12))
#data
FileName = sys.argv[1]
fs, y = wavfile.read(FileName)
AudioFileName = os.path.basename(FileName)[:os.path.basename(FileName).rfind('.')]
PlayingStyle = AudioFileName[5:AudioFileName.find('_')-1]
Dynamics = AudioFileName[AudioFileName.find('_')-1:AudioFileName.find('_')]
String = AudioFileName[AudioFileName.rfind('_')-2:AudioFileName.rfind('_')]
NoteName = AudioFileName[AudioFileName.rfind('_')+1:]
f = notetofrq(NoteName)
N = int(fs/2/f)-1
frameSize = int(fs/f)*2
hopSize = frameSize//2
Frames = int(len(y)//hopSize-1)
#num_steps = 50000
'''
#create folder
directory = os.path.join(PlayingStyle+Dynamics, AudioFileName)
if not os.path.exists(directory):
    os.makedirs(directory)

#data
data = {}
data['fs'] = fs
data['AudioFileName'] = AudioFileName
data['PlayingStyle'] = PlayingStyle
data['Dynamics'] = Dynamics
data['String'] = String
data['NoteName'] = NoteName
data['f'] = f
data['N'] = N
data['frameSize'] = frameSize
data['hopSize'] = hopSize
data['Frames'] = Frames
data['num_steps'] = num_steps
with open(directory+'/data.pickle', 'wb') as file:
    pickle.dump(data, file)
'''
#normalization
m = max(max(y), -min(y))
y = y/m

#creat tensorflow structure
t = tf.range(frameSize)
t = tf.cast(t, tf.float32)
yt = tf.placeholder(tf.float32, shape=(frameSize,))
A = [tf.Variable(0.0) for i in range(N)]
B = [tf.Variable(0.0) for i in range(N)]
C = tf.Variable(0.0)
w0 = tf.placeholder(tf.float32, shape=(frameSize,))
W = tf.add(tf.multiply(C, t), w0)
Y = 0.0
for i in range(N):
    Y = tf.add(Y, tf.add(tf.multiply(A[i], tf.sin(tf.multiply(2*np.pi*W*(i+1)/fs, t))), tf.multiply(B[i], tf.cos(tf.multiply(2*np.pi*W*(i+1)/fs, t)))))
loss = tf.reduce_mean(tf.square(Y-yt))
#optimizer = tf.train.AdadeltaOptimizer(1, 0.95, 1e-6)
optimizer = tf.train.AdamOptimizer(learning_rate = 1e-3)
train = optimizer.minimize(loss)
init = tf.global_variables_initializer()
sess = tf.Session()

w_list = [f]
A_list = []
B_list = []
error = []
for frame in range(1):
    num_steps = 1000
    frame = 1001
    f = 438.4852
    sess.run(init)

    start = frame*hopSize
    end = start+frameSize
    #run
    ym = max(y[start:end])
    ym = 1
    yn = [y[i]/ym for i in range(start,end)]
    cur_w0 = np.ones(frameSize, dtype='float32')*f
    for i in range(num_steps):
        sess.run(train, feed_dict={yt:yn, w0:cur_w0})
        error.append(sess.run(loss, feed_dict={yt:yn, w0:cur_w0}))

    A_list.append([i*ym for i in sess.run(A)])
    B_list.append([i*ym for i in sess.run(B)])
    #w_list += list(sess.run(W, feed_dict={w0:cur_w0}))
'''
with open(directory+'/A.pickle', 'wb') as file:
    pickle.dump(A_list, file)
with open(directory+'/B.pickle', 'wb') as file:
    pickle.dump(B_list, file)
with open(directory+'/w.pickle', 'wb') as file:
    pickle.dump(w_list, file)
'''
#sess.close()