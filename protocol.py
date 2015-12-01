# Copyright (c) 2015 Gregory Gaston
# 
# This file impliments all protocol versions.
# All function calls shall be made to read_message(message, version)
# or write_message(user_info, my_info, message, version) which will 
# act as wrappers to handle messages of the given versions.


# <<<< <<<< <<<< READ MESSAGE FUNCTIONS >>>> >>>> >>>> #

#This is the wrapper function for reading messages
def read_message(message, version):
  if version == '0.1':
    return read_message_0_1(message)
  if version == '0.2':
    return read_message_0_2(message)
  return None

#Protocol v0.2
def read_message_0_2(message):
  return None


#Protocol v0.1
def read_message_0_1(message):
  #sarch for the :, search for the new line
  length = len(message)
  i = 0 
  j = 0
  user_info = (None, None)
  my_info = (None, None)
  #  version: 0.1 
  i = 12
  j = i
  while message[j] != '\r' and j <length:
    j = j +1
  version = message[i:j]

#  from: their_name
  i = j + 8 # len('\nfrom: ')
  j = i
  while message[j] != '\r' and j <length:
    j = j +1
  user_info = (message[i:j], None)

  #  to: my_name
  i = j + 6
  j = i
  while message[j] != '\r' and j <length:
    j = j +1
  my_info = (message[i:j], None)

  #  message
  recieved_message = message[j+4:]
#  print(user_info, my_info, recieved_message, version)
  return (user_info, my_info, recieved_message, version)


# <<<< <<<< <<<< WRITE MESSAGE FUNCTIONS >>>> >>>> >>>> #

#This is the wrapper function for writing messages
def write_message(user_info, my_info, message, version):
  if version == '0.1':
    return write_message_0_1(user_info, my_info, message, version)
  return None

  #protocol v0.1
def write_message_0_1(user_info, my_info, message, version):
  #  version: 0.1
  #  from: my_name
  #  to: your_name
  #
  #  message
  return "version: " + version + "\r\nfrom: " + my_info[0] + "\r\nto: "+ user_info[0] + "\r\n\r\n" + message



def main():
  
  print('-----')
  print(ord('\n'))
  print("10" + chr(10)) 
  print('-----')
  print(ord('\r'))
  print("13" + chr(13))
  print('-----')


  return






if __name__ == "__main__":
  main()
