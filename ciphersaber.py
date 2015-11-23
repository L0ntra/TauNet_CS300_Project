# Implimentation copyright (c) 2015 Gregory Gaston
##
# Ciphersaber2 algorythm and pseudo code source copyright (c) 
# 2015 Bart Massey (https://github.com/BartMassey/ciphersaber2)
# Copyright (c) 2015 Bart Massey
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.



import sys, string, random



# genorates key stream
# n = size of key stream
# r = number of times to randomize
# k = key
def rc4(n, r, k):
  l = len(k)
  ## Initialize the array.
  s = [0 for q in range(256)]
  for i in range(0, 255):
      s[i] = i
  ## Do key scheduling.
  j = 0
  for r in range(0, r):
    for i in range(0, 255):
      j = (j + s[i] + k[i % l]) % 256
      temp = s[i]
      s[i] = s[j]
      s[j] = temp
  ## Finally, produce the stream.
  keystream = [0 for q in range(0, n)]
  j = 0
  for i in range(0, n-1):
    i2 = (i + 1) % 256
    j = (j + s[i2]) % 256
    temp = s[i2]
    s[i2] = s[j]
    s[j] = s[i2]
    keystream[i] = s[(s[i2] + s[j]) % 256]
  return keystream


# INPUT:
# Plain Text Message
# Times to repeast RC4
# encrpythion key
# OUTPUT:
# (10 byte IV + Encrypted Message)

def encrypt(message, repeat, key):
  length = len(message)
  iv = '0123456789' ## 10 byte random initial value
  keyiv = key + iv
  print(keyiv)
  keystream = rc4(length, repeat, keyiv.encode())
  ciphertext = '' #[0 for i in range(0, length +10)]
  for i in range(0,10):
    ciphertext = ciphertext + iv[i]
  for i in range(0, length):
    ciphertext = ciphertext + chr(ord(message[i]) ^ keystream[i])
  return ciphertext


# INPUT:
# (10 byte IV + Encrypted Message)
# OUTPUT:
# Plain Text Message
def decrypt(ivmessage, repeat, key):
  length = len(ivmessage)-10
  iv = ''
  message = ''
  for i in range(0,10):
    iv = iv + ivmessage[i]
  print(iv)
  keyiv = key + iv
  print(keyiv)
  keystream = rc4(length, repeat, keyiv.encode())
  plaintext = '' #[0 for i in range(0, length)]
  for i in range(10, length+10):
    message = message + ivmessage[i]
  for i in range(0, length):
    plaintext = plaintext + chr(ord(message[i]) ^ keystream[i])
  return plaintext  


def main():
  k = 'password'
  s = rc4(16, 10, k.encode())
  print(s)
#  print(rc4(16, 25, k.encode()))
#  print(rc4(16, 50, k.encode()))
#  print(rc4(16, 100, k.encode()))
#  print(rc4(16, 250, k.encode()))
#  print(s)
  t = encrypt("1234567890qwertyuiop[]asdfghjkl;'zxcvbnm,.!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:ZXCVBNM<>?~`", 20, 'passworded')
#  print(str(t))
  u = decrypt(t, 20, 'passworded')
  print(u)

  return



if __name__ == '__main__':
  main()
