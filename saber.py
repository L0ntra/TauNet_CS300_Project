# Copyright (c) 2015 Gregory Gaston
# License: https://opensource.org/licenses/MIT
#
# This file impliments the ciphersaber2 encryption algorythm
# Code based off of Bart Massy's pseudo code:
#   https://github.com/BartMassey/ciphersaber2
# With additional insperation from:
#   https://web.archive.org/web/20050129124628/http://www.xs4all.nl/~cg/ciphersaber/comp/python.txt
# Test strings provided by:
#   http://ciphersaber.gurus.org/
# and:
#   http://www.cypherspace.org/adam/csvec/

## License infomation for Bart Massy's pseudo code:
##  Copyright (c) 2015 Bart Massey
##
##  Permission is hereby granted, free of charge, to any person obtaining
##  a copy of this software and associated documentation files (the
##  "Software"), to deal in the Software without restriction, including
##  without limitation the rights to use, copy, modify, merge, publish,
##  distribute, sublicense, and/or sell copies of the Software, and to
##  permit persons to whom the Software is furnished to do so, subject to
##  the following conditions:
##
##  The above copyright notice and this permission notice shall be included
##  in all copies or substantial portions of the Software.
##
##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
##  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
##  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
##  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
##  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
##  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
##  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##


import random, time

# Produce an RC4 keystream of length 'n'
def rc4(n, rounds, key):
  length = len(key)
  s = [i for i in range(256)]

  # key scheduling.
  j = 0
  for discard_keys in range(rounds):
    for i in range(256):
      j = (j + s[i] + key[i % length]) % 256
      s[i], s[j] = s[j], s[i] # Easy way to switch vars

  # Produce keystream.
  keystream = [0 for i in range(n)]
  j = 0
  for i in range(n):
    k = (i + 1) % 256
    j = (j + s[k]) % 256
    s[k], s[j] = s[j], s[k]
    keystream[i] = s[(s[k] + s[j]) % 256]
  return keystream


# Ciphersaber-2 decrypt ciphertext
# 20 round of key scheduling in standard
def decrypt(ivmessage, rounds, key):
  length = len(ivmessage) - 10
  iv = ivmessage[:10] # chars 0 - 9
  message = ivmessage[10:] # chars 10-n

  keyiv = [] # dynamicly sized list
  keyiv[:len(key)] = map(ord, key)  # map 'runs' ord on all elements of key
  keyiv[len(key):] = iv

  keystream = rc4(length, rounds, keyiv)
  plaintext = [0 for i in range(length)]# "zero-based array of" n - 10 "bytes"
  for i in range(length):
    plaintext[i] = message[i] ^ keystream[i]
  return plaintext


# Ciphersaber-2 encrypt ciphertext
# 20 rounds of key scheduling is standard
def encrypt(message, rounds, key):
  length = len(message)
  # Throw out the large numbs from time and use <1 sec numbers for the seed
  random.seed(int(float(str(time.time())[:0:-1])))
  # create 10 byte random number
  iv = [random.randrange(0,255) for i in range(0,10)]  
  keyiv, keyiv[:len(key)], keyiv[len(key):] = [], map(ord, key), iv
  keystream = rc4(length, rounds, keyiv)
  ciphertext= [0 for i in range(length+10)]
  ciphertext[:10] = iv
  for i in range(length):
    ciphertext[i+10] = message[i] ^ keystream[i]
  return ciphertext
