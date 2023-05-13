import os
import subprocess
import warnings
import pickle
import numpy as np

warnings.filterwarnings('ignore')
BUFFER_SIZE=100
c=0
FILENAME='/Users/rachitdas/Desktop/monitor/flows.csv'

model=pickle.load(open('/Users/rachitdas/Desktop/prototype_ps/model2.pkl','rb'))

layer_2=[]
for i in os.listdir('/Users/rachitdas/Desktop/prototype_ps/layer_2'):
    layer_2.append('/Users/rachitdas/Desktop/prototype_ps/layer_2/'+i)

times=0
exists=False
lines_buffer=[]
tail_process=subprocess.Popen(['tail','-F','/Users/rachitdas/Desktop/monitor/flows.csv'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
while True:
    if os.path.exists("/Users/rachitdas/Desktop/monitor/flows.csv"):
        exists=True
        break
    else:
        print("File does not exist")

if(exists):
    print("File exists")
    initial_timestamp=os.path.getmtime("/Users/rachitdas/Desktop/monitor/flows.csv")
    while True:
        current_timestamp=os.path.getmtime("/Users/rachitdas/Desktop/monitor/flows.csv")
        if(initial_timestamp!=current_timestamp):
            line=tail_process.stdout.readline()
            if(line):
                data=line.decode()
                c+=1
                data=data.split(',')
                data.pop(0)
                data.pop(0)
                data.pop(0)
                data.pop(2)
                data.pop(3)
                data.pop(3)
                data[-1]=data[-1].strip('/r/n')
                if(c>1):
                    data=[float(i) for i in data]
                    pred=model.predict(np.array(data).reshape(1,-1))
                    if(pred==1):
                        print("Anamoly detected. Detecting type of probable attack now....")
                        for layer in layer_2:
                            l=[]
                            current_layer=pickle.load(open(layer,'rb'))
                            pred=current_layer.predict(np.array(data).reshape(1,-1))
                            if(pred==-1):
                                l.append(layer[39:-5])
                        print(f'Probable Attacks: {l}')
                    else:
                        print("No attack detected")
                print(c)    