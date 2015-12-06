# Copyright (c) 2015 Gregory Gaston
# License: https://opensource.org/licenses/MIT
# This file impliments all protocol versions.
# All function calls shall be made to read_message(message)
# or write_message(user_info, my_info, message, version) which will 
# act as wrappers to handle messages of the given versions.


# <<<< <<<< <<<< READ MESSAGE FUNCTIONS >>>> >>>> >>>> #

# This is the wrapper function for reading messages
def read_message(message):
  assert message
  # Split version out of the message
  version, message = find_r(message[9:])
  # Version 0.1 and 0.2 have the same format
  if version == '0.2' or version == '0.1': 
    return read_message_0_1(message[8:], version)
  return None

# Reads messages formateed using protocol v0.1
def read_message_0_1(message, version = '0.2'):
  assert message
  #Version has been removed already
  #message == '\r\nfrom: user_name\r\n...'
  sender, message = find_r(message)
  #message == '\r\nto: user_name\r\n...'
  reciever, message = find_r(message[6:])
  #message == '\r\n\r\nmessage'
  message = message[4:].strip(' \t')
  return ((sender, ''), (reciever, ''), message, version)


# search a message for a \r
# split messages in to two pieces before \r and after \r
def find_r(message):
  assert message
  length = len(message)
  for i in range(length):
    if message[i] == '\r':
      return(message[:i], message[i:])
  # \r not found. The rest of the message is 'before' the \r
  return(message, '')


# <<<< <<<< <<<< WRITE MESSAGE FUNCTIONS >>>> >>>> >>>> #

# This is the wrapper function for writing messages
def write_message(user_info, my_info, message, version):
  assert user_info and my_info and message and version
  # Version 0.2 and 0.1 have the same format
  if version == '0.2' or version == '0.1':
    return write_message_0_1(user_info, my_info, message, version)
  return None

# Compose message based off protocol v0.1
def write_message_0_1(user_info, my_info, message, version):
  assert user_info and my_info and message and version
  #  version: 0.1\r\nfrom: my_name\r\nto: your_name\r\nmessage
  return "version: " + version + "\r\nfrom: " + my_info[0] + "\r\nto: "+ user_info[0] + "\r\n\r\n" + message


## Main for testing.
def main():
  print('\n\n')
  message = (('Reciever', '127.0.0.1'), ('Sender', '127.0.0.1'), 'This is a test - 1234567890 abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ `[]\;,./~!@#$%^&*()_+{}|:"<>?' + "'", '0.2')
  sent_message = write_message(message[0], message[1], message[2], message[3])
  rec_message = read_message(sent_message)
  print("Message object")
  print(message)
  print("\nComplosed message\n" + sent_message)
  print("\nRecieved message\n")
  print(rec_message)
  print('\n\n')
  #read_message('version: 0.1\r\nfrom: sender\r\nto: reciever\r\n\r\nmessage'))
  return

if __name__ == "__main__":
  main()
