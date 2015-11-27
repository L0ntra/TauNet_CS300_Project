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
  while message[i] != ':' and i < length:
    i = i +1
  i = i + 2
  j = i
  while message[j] != '\n' and j <length:
    j = j +1
  version = message[i:j]

  #  from: their_name
  while message[i] != ':' and i < length:
    i = i +1
  i = i + 2
  j = i
  while message[j] != '\n' and j <length:
    j = j +1
  user_info = (message[i:j], None)

  #  to: my_name
  while message[i] != ':' and i < length:
    i = i +1
  i = i + 2
  j = i
  while message[j] != '\n' and j <length:
    j = j +1
  my_info = (message[i:j], None)

  #  message
  recieved_message = message[j+2:length]

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
  return "version: " + version + "\nfrom: " + my_info[0] + "\nto: "+ user_info[0] + "\n\n" + message



def main():
  message = write_message(('user1', '127.0.0.1'), ('ME!', '127.0.0.1'), "Why hello there!", '0.1')
  print(message)
  part_mess = read_message(''+message, '0.1')
  print('\n\nread_message()\nuser_info = ', end = ''); print(part_mess[0])
  print('my_info = ', end = ''); print(part_mess[1])
  print('message = ', end = ''); print(part_mess[2])
  print('version = ', end = ''); print(part_mess[3])
  return



if __name__ == "__main__":
  main()
