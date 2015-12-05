# Copyright (c) 2015 Gregory Gaston
# 
# This file impliments all protocol versions.
# All function calls shall be made to read_message(message, version)
# or write_message(user_info, my_info, message, version) which will 
# act as wrappers to handle messages of the given versions.


# <<<< <<<< <<<< READ MESSAGE FUNCTIONS >>>> >>>> >>>> #

#This is the wrapper function for reading messages
def read_message(message):
  version, message = find_r(message[9:])
  # Version 0.1 and 0.2 have the same format
  if version == '0.2' or version == '0.1': 
    return read_message_0_1(message[8:])
  return None


def read_message_0_1(message):
  #Version has been removed already
  #message == '\r\nfrom: user_name\r\n...'
  #             0 12345678
  sender, message = find_r(message)
  #message == '\r\nto: user_name\r\n...'
  #             0 123456
  reciever, message = find_r(message[6:])
  #message == '\r\n\r\nmessage'
  #             0 1 2 34
  message = message[4:].strip(' \t')
  return ((sender, ''), (reciever, ''), message, '0.1')


# search a message for a \r
# split messages in to two pieces before \r and after \r
def find_r(message):
  length = len(message)
  for i in range(length):
    if message[i] == '\r':
      return(message[:i], message[i:])
  # \r not found. The rest of the message is 'before' the \r
  return(message, '')


# <<<< <<<< <<<< WRITE MESSAGE FUNCTIONS >>>> >>>> >>>> #

#This is the wrapper function for writing messages
def write_message(user_info, my_info, message, version):
  # Version 0.2 and 0.1 have the same format
  if version == '0.2' or version == '0.1':
    return write_message_0_1(user_info, my_info, message, version)
  return None


def write_message_0_1(user_info, my_info, message, version):
  #  version: 0.1\r\nfrom: my_name\r\nto: your_name\r\nmessage
  return "version: " + version + "\r\nfrom: " + my_info[0] + "\r\nto: "+ user_info[0] + "\r\n\r\n" + message


## Main for testing.
def main():
  read_message('version: 0.1\r\nfrom: sender\r\nto: reciever\r\n\r\nmessage') 
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
