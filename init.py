import math
import pickle
import csv
import hashlib
import os
import sys
import mysql.connector

def lcm(a, b):
  return a * b // math.gcd(a, b)

def inverse_mod(e, x):
  """
  python for:
  d * e mod x = 1
  """
  t = 0
  newt = 1
  r = x
  newr = e
  while newr != 0:
    q = r // newr
    t, newt = newt, t - q * newt
    r, newr = newr, r - q * newr
  if r > 1:
    return None
  if t < 0:
    t += x
  return t

blockchain_order = int(sys.argv[1])
# add record to database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="toor",
  database="evoting"
)

mycursor = db.cursor()
sql = "INSERT INTO blockchains (id, nama) VALUES (%s, %s)"
val = (blockchain_order, "Blockchain " + str(blockchain_order))
mycursor.execute(sql, val)


if blockchain_order == 1:
  primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 121, 127, 131, 137, 139, 143, 149, 151, 157, 163, 167, 169, 173, 179, 181, 187, 191, 193]

  p = 197
  q = 199

  nodes = [
    'http://localhost:3001',
    'http://localhost:3002',
    'http://localhost:3003',
    'http://localhost:3004',
    'http://localhost:3005'
  ]

else:
  primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 121, 127, 131, 137, 139, 143, 149, 151, 157, 163, 167, 169, 173, 179, 181, 187, 191, 193, 197, 199]

  p = 53
  q = 73

  nodes = [
    'http://localhost:3006',
    'http://localhost:3007',
    'http://localhost:3008',
    'http://localhost:3009',
    'http://localhost:3010'
  ]

for node in nodes:
  sql = "INSERT INTO alamat_blockchains (id_blockchain, alamat) VALUES (%s, %s)"
  val = (blockchain_order, node)
  mycursor.execute(sql, val)



n = p * q
x = lcm(p - 1,q - 1)

data_res = [['n', 'e', 'saldo']]
data_private_key = [['n', 'e', 'd']]

with open('key.pub', 'rb') as input:
  public_key = pickle.load(input)

pilihan = 1

for e in primes:
  d = inverse_mod(e, x)
  if d is not None:
    if pilihan < 3:
      sql = "INSERT INTO pilihans (id_blockchain,id_pilihan, nilai_n, nilai_e) VALUES (%s, %s, %s, %s)"
      val = (blockchain_order, pilihan, n, e)
      pilihan = pilihan + 1
    else:
      sql = "INSERT INTO map_blockchains (id_blockchain, nilai_n, nilai_e) VALUES (%s, %s, %s)"
      val = (blockchain_order, n, e)

    mycursor.execute(sql, val)
    
    data_res.append([n, e, public_key.raw_encrypt(10)])
    data_private_key.append([n, e, d])


with open('1.res', 'w') as writeFile:
  writer = csv.writer(writeFile)
  writer.writerows(data_res)

with open('key_blockchain.pri', 'w') as writeFile:
  writer = csv.writer(writeFile)
  writer.writerows(data_private_key)

trx_file = open("1.trx","w")
trx_file.close()

BLOCKSIZE = 65536
hasher = hashlib.sha3_512()
with open('1.res', 'rb') as afile:
  buf = afile.read(BLOCKSIZE)
  while len(buf) > 0:
    hasher.update(buf)
    buf = afile.read(BLOCKSIZE)

with open('1.trx', 'rb') as afile:
  buf = afile.read(BLOCKSIZE)
  while len(buf) > 0:
    hasher.update(buf)
    buf = afile.read(BLOCKSIZE)

hash_file = open("1.hash","w")
hash_file.write(hasher.hexdigest())
hash_file.close()

os.system("cp 1.hash node1/1.hash")
os.system("cp 1.res node1/1.res")
os.system("cp 1.trx node1/1.trx")
os.system("cp key.pub node1/key.pub")

os.system("cp 1.hash node2/1.hash")
os.system("cp 1.res node2/1.res")
os.system("cp 1.trx node2/1.trx")
os.system("cp key.pub node2/key.pub")

os.system("cp 1.hash node3/1.hash")
os.system("cp 1.res node3/1.res")
os.system("cp 1.trx node3/1.trx")
os.system("cp key.pub node3/key.pub")

os.system("cp 1.hash node4/1.hash")
os.system("cp 1.res node4/1.res")
os.system("cp 1.trx node4/1.trx")
os.system("cp key.pub node4/key.pub")

os.system("cp 1.hash node5/1.hash")
os.system("cp 1.res node5/1.res")
os.system("cp 1.trx node5/1.trx")
os.system("cp key.pub node5/key.pub")



db.commit()

