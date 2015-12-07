# Copyright (c) 2015 Gregory Gaston
# License: https://opensource.org/licenses/MIT
# This file contains the main() function for the TauNet system as
# well as many of the basic functions involved with sending messages
# recieving messages, and the program interface.

# Built in libraries
import socket, threading, time, os
# my libraries
import protocol, saber, messages, user_func


# <<<< <<<< <<<< Globals Variable >>>> >>>> >>>> #
port = 6283
myip = socket.gethostbyname(socket.gethostname())
my_user_name = ''
TauNet_version = '1.0'
protocol_version = '0.2'
input_message = "TauNet v" + TauNet_version + ">> " #Global variable
TIMEOUT = 8
key = ''



# <<<< <<<< <<<< MESSAGING FUNCTIONS >>>> >>>> >>>> #
# Functions dealing with the sending and recieveing of messages.

# Sends a message based on the user_info
def send_message(user_info, my_info, message, key):
  # Package
  pay = protocol.write_message(user_info, my_info, message, protocol_version)
  # Encrypt
  enc_pay = saber.encrypt(pay.encode(), 20, key)
  # Convert to string
  str_enc_pay = ''
  for i in range(len(enc_pay)):
    str_enc_pay = str_enc_pay + chr(enc_pay[i])
  # Send payload
  s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
  s.settimeout(TIMEOUT)
  s.connect((user_info[1], port)) # connet() takes tuple (user_ip, port#)
  assert s
  s.send(str_enc_pay.encode()) #encode converts message to bin
  s.shutdown(1)
  s.close()
  return


# Listens for incoming messages
# Run as a seporate thread
def listen(user_list, message_hist):
  s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
  assert s
  s.bind(('', 6283))
  while 1:
    s.listen(1)
    assert s
    (conn , addr) = s.accept()
    mess = conn.recv(1024).decode() #decode convers from bin to string
                                    #Hangs untill message is recieved
    assert mess                                    
    ## FORK HERE TO DECODE WHILE STILL BEING ABLE TO ACCEPT A NEW MESSAGE
    #convert to list
    mess_list = [ord(mess[i]) for i in range(len(mess))]
    # decrypt
    dec_mess = saber.decrypt(mess_list, 20, user_list.key)
    # convert to string
    message = ''
    for i in range(len(dec_mess)):
      message = message + chr(dec_mess[i])
     
    rec_mess = protocol.read_message(message) #piece out message
    if rec_mess[2] == '' or rec_mess[2] == '\n': ##Empty message recieved
      None
    elif(user_list.search_users(rec_mess[0][0])):
      print('\n' + rec_mess[0][0] + ':\t' + rec_mess[2] + '\n' + input_message, end = '')
      message_hist.add_message(rec_mess[0][0], rec_mess[1][0], rec_mess[2])
    else:
      #Send error message
      print('\n<<Message recieved from unknon user and discarded>>\n' + input_message, end = '')
  return


# <<<< <<<< <<<< COMMAND FUNCTIONS >>>> >>>> >>>> #
# This section contains functions pertaining to the different
# commands that are accepted by the TauNet command prompt.

# Breaks a command in to it's pieces
def read_command(command):
  if not command:
    return None
  length = len(command)
  i = 1 
  part1 = part2 = None
  while i < length and command[i] != ' ':
    i = i + 1
  part1 = command[1:i]
  part2 = command[i+1:length]
  return (part1, part2)


#@user message
def at(user_info, message):
  message_end = None
  while message:
    if len(message) > 600:
      message_end = message[600:]
      message = message[:600]
    else:
      message_end = None
        
    resend = True
    while resend:
      try:
        send_message(user_info, (my_user_name, myip), message, key)
      except:# TimeoutError:
        if input("Error:\n * Unable to send message to " + user_info[0] + ". Attempt to resend message? (y/n) " ) == 'n':
          resend = False
      else:
        resend = False
    message = message_end
    time.sleep(0.1) #make sure we don't overload someone else's reciever
  return None


# Help menu
def help_menu():
  print(" Command               | Description")
  print(" ----------------------+-------------------------------------------------------")
  print(" ?                     | Displays this dialogue")
  print(" @user_name Message    | Sends 'user_name' 'Message'")
  print(" @ Message             | Sends 'Message' to the last 'user_name' messaged")
  print(" +user_name ip_address | Adds 'user_name' to the list of users at 'ip_address.'")
  print(" -user_name            | Remove 'user_name' from the list of users.")
  print(" #n                    | Displays the last 'n' messages from 1 to 20")
  print("                       | if n is not specified prints the last message")
#  print(" #user_name n          | Displays the last 'n' messages (to and) from user_name")
  print(" ~                     | Displays all networked users and their address")
#  print(" ~user_name            | Displays user_name's information")
  print(" !CLEAR                | Clear the Screen")
  print(" !EXIT                 | Exit the program")
  print(" ----------------------+-------------------------------------------------------")
  return None


# Clear the display:
def clear():
  try:
    if os.name == 'nt':
      clear = os.system('cls')
    else:
      clear = os.system('clear')
  except: None
  return None


# <<<< <<<< <<<< MAIN >>>> >>>> >>>> #
# The main execution branch for TauNet.
def main():
  print("                     _   __     __              ___ ____   \n" +
        "   _____ ___  __  __/ | / /__  / /_    _   __  <  // __ \  \n" +
        "  /  __/ __ `/ / / /  |/ / _ \/ __/   | | / /  / // / / /  \n" +
        "  / /_/ /_/ / /_/ / /|  /  __/ /_     | |/ /  / // /_/ /   \n" +
        "  \__/\__,_/\__,_/_/ |_/\___/\__/     |___/  /_(_)____/    \n" +
        "\n")
##     ASCII TEXT ART FROM: http://patorjk.com/software/taag/#p=display&f=Slant


  # Select file to open
  while True:
    filename = input("Enter TauNet filename: ")
    if filename == '!EXIT':
      return None
    elif filename == 'new':
      user_list = user_func.u_list()
      user_list.input_u_list()
    else:
      try:
        open(filename)
      except IOError:
        print(filename + " does not exist.")
        if input("Would you like to create it? (y/n): ") == 'y':
          user_list = user_func.u_list()
          user_list.input_u_list(filename)
          break
      else:
        user_list = user_func.u_list(filename)
        break

  # Local variables
  message_hist = messages.message_list()
  global my_user_name, key
  my_user_name = user_list.me
  key = user_list.key
  user_info = old_user = None

  # Start Listening for incoming messages
  listen_thread = threading.Thread(target=listen, args = (user_list, message_hist,))
  listen_thread.daemon = True
  listen_thread.start()

  # Long message test:
  #  message = ''
  #  for i in range(1000):
  #    message = message + str(i%10)
  #  for i in range(20):
  #    at(('user1', '127.0.0.1'), message)

  # Menu loop
  while True:
    split_command = None
    command = input(input_message)
    if command == '':
      None# Do nothing
    # Send a message to a user
    elif command[0] == '@':
      user_name, message = read_command(command)
      if(user_name != ''):
        old_user = user_info
        user_info = None
        user_info = user_list.search_users(user_name)
      if user_info: #send the message
          at(user_info, message)
      else:
        user_info = old_user
        print("Error:\n * Invalid Command. ? for help.") ##Invalid user_name

    # Add a user to the list
    elif command[0] == '+': 
      split_command = read_command(command)
      if (split_command[0] != '' and split_command[1] != '' and 
          user_func.valid_user(split_command[0]) and
          user_list.add_user(split_command)):
        user_list.write_file()
      else:
        print("Error:\n * Users name may only contain uppercase and lowercase letters from a-z, the numbers from 0-9, and the - symbol.\n * User names must also not have already been added to the list.")

    # Remove a user from the list          
    elif command[0] == '-':
      if command == '-':
        print("Error:\n * Invalid Command. ? for help.")
      elif user_list.remove_user(command[1:]):
        user_list.write_file()
        user_info = None

    # Display the last n messages
    # or the last message
    elif command[0] == '#':
      try:
        lines = int(command[1:])
      except:
        lines = -1
      if lines > 0 and lines < 21:
        message_hist.print_n(lines)
      else:
        print("Error:\n * n must be a whole number from 1 to 20 represented in digits.")

    # Display the list of users
    elif command == '~':
      user_list.print_users(); print()

    # Display help menue
    elif command == '?':
      help_menu()

    # Clear the Screen
    elif command == '!CLEAR':
      clear()

    # Exit the program      
    elif command == '!EXIT':
      return

    #Invalid command
    else:
      print("Error:\n * Invalid Command. ? for help.")


if __name__ == "__main__":
  clear()
  main()
  clear()
