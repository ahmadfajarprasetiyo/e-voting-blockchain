import math
import csv
import hashlib
import os


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

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 121, 127, 131, 137, 139, 143, 149, 151, 157, 163, 167, 169, 173, 179, 181, 187, 191, 193]

p = 197
q = 199

n = p * q
x = lcm(p - 1,q - 1)

data_res = [['n', 'e', 'saldo']]
data_private_key = [['n', 'e', 'd']]

for e in primes:
    d = inverse_mod(e, x)
    if d is not None:
        data_res.append([n, e, 10])
        data_private_key.append([n, e, d])


with open('1.res', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(data_res)

with open('key.pri', 'w') as writeFile:
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

os.system("cp 1.hash node2/1.hash")
os.system("cp 1.res node2/1.res")
os.system("cp 1.trx node2/1.trx")

os.system("cp 1.hash node3/1.hash")
os.system("cp 1.res node3/1.res")
os.system("cp 1.trx node3/1.trx")

os.system("cp 1.hash node4/1.hash")
os.system("cp 1.res node4/1.res")
os.system("cp 1.trx node4/1.trx")

os.system("cp 1.hash node5/1.hash")
os.system("cp 1.res node5/1.res")
os.system("cp 1.trx node5/1.trx")





