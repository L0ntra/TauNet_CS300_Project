## Copyright (c) 2015 Gregory Gaston
##
## This file impliments the ciphersaber encryption algorythm


## "Produce an RC4 keystream of length" n "with"
## r "rounds of key scheduling given key" k
def rc4(n, rounds, key):
  length = len(key)
  s = [i for i in range(256)]
  ## key scheduling.
  j = 0
  for discard_keys in range(rounds):
    for i in range(256):
      j = (j + s[i] + key[i % length]) % 256
      s[i], s[j] = s[j], s[i] # Easy way to switch vars

  ## Produce keystream.
  keystream = [0 for i in range(n)]
  j = 0
  for i in range(n):
    i2 = (i + 1) % 256
    j = (j + s[i2]) % 256
    s[i2], s[j] = s[j], s[i2]
    keystream[i] = s[(s[i2] + s[j]) % 256]
  return keystream


## Ciphersaber-2 decrypt ciphertext
## 20 round of key scheduling in standard
def decrypt(ivmessage, rounds, key):
  length = len(ivmessage) - 10
  iv = ivmessage[:10] #chars 0 - 9
  message = ivmessage[10:] #chars 10-n

  keyiv = [] #dynamicly sized list
  keyiv[:len(key)] = map(ord, key) #map 'runs' ord on all elements of key
  keyiv[len(key):] = iv

  keystream = rc4(length, rounds, keyiv)
  plaintext = [0 for i in range(length)]# "zero-based array of" n - 10 "bytes"
  for i in range(length):
    plaintext[i] = message[i] ^ keystream[i]
  return plaintext

## Ciphersaber-2 encrypt ciphertext
## 20 rounds of key scheduling is standard
def encrypt(message, rounds, key):
  length = len(message)
  iv = [0xba, 0x9a, 0xb4, 0xcf, 0xfb, 0x77, 0x00, 0xe6, 0x18, 0xe3] #10 byte random number
  keyiv, keyiv[:len(key)], keyiv[len(key):] = [], map(ord, key), iv
  keystream = rc4(length, rounds, keyiv)
  ciphertext= [0 for i in range(length+10)]
  ciphertext[:10] = iv
  for i in range(length):
    ciphertext[i+10] = message[i] ^ keystream[i]
  return ciphertext

def main():
  a='This is a test of CipherSaber-2.'
  c = [ord(a[i]) for i in range(len(a))]
  c2 = a.encode()
  b = encrypt(c, 10, 'asdfg')
  b2 = encrypt(c2, 10, 'asdfg')
  b3 = ''
  for i in range(len(b2)):
    b3 = b3 + chr(b2[i])
  b4 = [ord(b3[i]) for i in range(len(b3))]
  d = decrypt(b4, 10, 'asdfg')
  e = ''
  for i in range(0, len(d)):
    e = e + chr(d[i])
  print("Encrypt then decrypt 'This is a test of CipherSaber-2.':")
  print("Encrypted String: ", b)
  print("Decrypted String: ", e, "\n\n")

  print("Decrypt test encodings:" )
## This is a test of CipherSaber-2.
  m = [0xba, 0x9a, 0xb4, 0xcf, 0xfb, 0x77, 0x00, 0xe6, 0x18, 0xe3, 0x82, 
       0xe8, 0xfc, 0xc5, 0xab, 0x98, 0x13, 0xb1, 0xab, 0xc4, 0x36, 0xba, 
       0x7d, 0x5c, 0xde, 0xa1, 0xa3, 0x1f, 0xb7, 0x2f, 0xb5, 0x76, 0x3c, 
       0x44, 0xcf, 0xc2, 0xac, 0x77, 0xaf, 0xee, 0x19, 0xad]

  n = decrypt(m, 10, 'asdfg')
  o = ''
  for i in range(0, len(n)):
    o = o + chr(n[i])
  print("Decrypted Test String: ", o)

  z = 'Al Dakota buys'
  y = [ord(z[i]) for i in range(len(z))]
  x = decrypt(y, 20, 'Al')
  v = ''
  for i in range(0, len(x)):
    v = v + chr(x[i])
  print("Decrypted Test String 2: ",v, '\n\n')

  print("Test encoding properties: ")
  print('ord() is equiv to .encode() for encrypt? ', (b == b2))
  print("Test Encryption == source Encryption: ", m == b)

if __name__ == "__main__":
  main()
