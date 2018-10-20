import pickle
import sys
if len(sys.argv) < 2:
    path = '.'
else:
    path = sys.argv[1]
with open(path+'/data.pickle','rb') as file:
    data=pickle.load(file)
for key in data:
    print(key, data[key])