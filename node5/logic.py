import hashlib
import os
import csv
import pickle
from phe import paillier


BLOCKSIZE = 65536
with open('key.pub', 'rb') as input:
  public_key = pickle.load(input)
  cipher = public_key.raw_encrypt(10)
  encrypted_number = paillier.EncryptedNumber(public_key, cipher)

def calculate_hash_block(n):
  hasher = hashlib.sha3_512()
  
  with open(str(n)+'.res', 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
      hasher.update(buf)
      buf = afile.read(BLOCKSIZE)
  
  with open(str(n)+'.trx', 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
      hasher.update(buf)
      buf = afile.read(BLOCKSIZE)
      
  if n > 1:
    n = n - 1
    with open(str(n)+'.hash', 'rb') as afile:
      buf = afile.read(BLOCKSIZE)
      while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(BLOCKSIZE)
  
  return hasher.hexdigest()

def is_valid_block(n):
  hash_file = open(str(n)+".hash","r").read().splitlines()
  return hash_file[0] == calculate_hash_block(n)

def is_valid_private_key(n, e, d):
  return 10 == pow(pow(10, e, n), d, n)

def get_lastest_hash():
  i = 1
  while os.path.isfile(str(i)+'.hash'):
    i = i + 1 

  hash_file = open(str(i-1)+".hash","r")
  return hash_file.readline()

def vote(sender_n, sender_e, sender_d, receiver_n, receiver_e):
  i = 1
  valid = False
  
  if is_valid_private_key(sender_n, sender_e, sender_d):
    valid = True
    while os.path.isfile(str(i)+'.res'):
      if not is_valid_block(i):
        valid = False
        print("File telah dimodifikasi pada block ke -", i)
        return "-1"
        break
      
      i = i + 1
  
  if valid:
    # data_res = [['n', 'e', 'saldo']]
    is_first = True
    index_sender = 0
    index_receiver = 0
    with open(str(i-1)+'.res', 'r') as res_file:
      reader = csv.reader(res_file)
      data_res = list(reader)
      for index, line  in enumerate(data_res):
        if is_first:
          is_first = False
        else:
          if int(line[1]) == sender_e:
            if int(line[2]) > 1:
              index_sender = index
            else:
              valid = False
              break
          elif int(line[1]) == receiver_e:
            index_receiver = index
  
  if valid and index_receiver > 0 and index_sender > 0:
    data_res[index_receiver][2] = encrypted_number._raw_add(int(data_res[index_receiver][2]), int(data_res[index_sender][2]))
    data_res[index_sender][2] = 1
    
    #write to file
    with open(str(i)+'.res', 'w') as writeFile:
      writer = csv.writer(writeFile)
      writer.writerows(data_res)
      writeFile.close()
      
    data_trx = [['sender_n', 'sender_e', 'receiver_n', 'receiver_e', 'digital_signature']]
    data_trx.append([sender_n, sender_e, receiver_n, receiver_e, pow(10,sender_d, sender_n)])
    
    with open(str(i)+'.trx', 'w') as writeFile:
      writer = csv.writer(writeFile)
      writer.writerows(data_trx)
      writeFile.close()
      
    hash_file = open(str(i)+".hash","w")
    hash_file.write(calculate_hash_block(i))
    hash_file.close()
      
  if valid and index_receiver > 0 and index_sender > 0:
    return get_lastest_hash()
  else:
    return "0"


