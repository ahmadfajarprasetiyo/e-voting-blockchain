import hashlib
import os
import csv


BLOCKSIZE = 65536

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
        with open(str(n)+'.trx', 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)

    return hasher.hexdigest()

def is_valid_block(n):
    hash_file = open(str(n)+".hash","r")
    return hash_file.readline() == calculate_hash_block(n)

def is_valid_private_key(n, e, d):
    return 10 == pow(pow(10, e, n), d, n)



def vote(sender_n, sender_e, sender_d, receiver_n, receiver_e):

    i = 1
    valid = False

    if is_valid_private_key(sender_n, sender_e, sender_d):
        valid = True
        while os.path.isfile(str(i)+'.res'):
            if not is_valid_block(i):
                valid = False
                print("File telah dimodifikasi pada block ke -", i)
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
            data_res[index_receiver][2] = int(data_res[index_receiver][2]) + 10
            data_res[index_sender][2] = 1

            #write to file
            with open(str(i)+'.res', 'w') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(data_res)

            data_trx = [['sender_n', 'sender_e', 'receiver_n', 'receiver_e', 'digital_signature']]
            data_trx.append([sender_n, sender_e, receiver_n, receiver_e, pow(10,sender_d, sender_n)])

            with open(str(i)+'.trx', 'w') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(data_trx)

            hash_file = open(str(i)+".hash","w")
            hash_file.write(calculate_hash_block(i))
            hash_file.close()



    return valid




print(vote(39203, 17, 13697, 39203, 13))
