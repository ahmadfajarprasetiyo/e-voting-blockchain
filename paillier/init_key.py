from phe import paillier
import pickle
import os

public_key, private_key = paillier.generate_paillier_keypair()

with open('key.pri','wb') as output:
  pickle.dump(private_key, output, pickle.HIGHEST_PROTOCOL)

with open('key.pub','wb') as output:
  pickle.dump(public_key, output, pickle.HIGHEST_PROTOCOL)


os.system("cp key.pub ../key.pub")
#cipher = public_key.raw_encrypt(10)
#cipher2 = public_key.raw_encrypt(10)

#encrypted_number = paillier.EncryptedNumber(public_key, cipher)
#print(cipher)
#print(cipher2)

#result_add = encrypted_number._raw_add(cipher, cipher2)
#print(result_add)
#print(private_key.raw_decrypt(result_add))
