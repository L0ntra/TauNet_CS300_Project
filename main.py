# Copyrigh (c) 2015 Gregory Gaston
# https://opensource.org/licenses/MIT
#


# Build in libraries
import socket, threading, time, os

# my libraries
from readfile import u_list
import protocol, saber

port = 6283
message = ''
user = ''
myip = socket.gethostbyname(socket.gethostname())
protocol_version = '0.1'
input_message = "TauNet v" + protocol_version + ">> " #Global variable
my_info = ('Lontra', '128.0.0.1')


# breaks a command in to it's pieces
# EX:
#   command = @user_name message
#   returns (user_name, message)
def read_command(command):
  length = len(command)
  i = 1 
  part1 = part2 = None
  while i < length and command[i] != ' ':
    i = i + 1
  part1 = command[1:i]
  part2 = command[i+1:length]
  return (part1, part2)

# Sends a message based on the user_info
# user_info = (user_name, user_ip)
def send_message(user_info, message, key):

  ##SENDING PROCESS
  # PACKAGE
  pay = protocol.write_message(user_info, my_info, message, protocol_version)
  # Encrypt
  enc_pay = saber.encrypt(pay.encode(), 20, key)
  #convert to string
  str_enc_pay = ''
  for i in range(len(enc_pay)):
    str_enc_pay = str_enc_pay + chr(enc_pay[i])

  #Send payload
  s = socket.socket(socket.AF_INET , socket.SOCK_STREAM) 
  s.connect((user_info[1], port)) # connet() takes tuple (user_ip, port#)
  s.send(str_enc_pay.encode()) #encode converts message to bin
  s.shutdown(1)
  s.close()

  return

# Listens for incoming messages
def listen(key):
  s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
  s.bind(('', 6283))
  while 1:
    s.listen(5)
    (conn , addr) = s.accept()
    mess = conn.recv(1024).decode() #decode convers from bin to string
                                    #Hangs untill message is recieved
    #convert to list
    mess_list = [ord(mess[i]) for i in range(len(mess))]
    # decrypt
    dec_mess = saber.decrypt(mess_list, 20, key)
    # convert to string
    message = ''
    for i in range(len(dec_mess)):
      message = message + chr(dec_mess[i])
      
    rec_mess = protocol.read_message(message, '0.1') #piece out message

    print('\n' + rec_mess[2] + '\n' + input_message, end = "")
  return



#<<<< <<<< <<<< MAIN >>>> >>>> >>>>#

def main():
  os.system('cls')
  print("                     _   __     __               ____   ___  \n" +
        "   _____ ___  __  __/ | / /__  / /_    _   __   / __ \ |__ \ \n" +
        "  /  __/ __ `/ / / /  |/ / _ \/ __/   | | / /  / / / / __/ / \n" +
        "  / /_/ /_/ / /_/ / /|  /  __/ /_     | |/ /  / /_/ / / __/  \n" +
        "  \__/\__,_/\__,_/_/ |_/\___/\__/     |___/   \____(_)____/  \n" +
        "\n")

##     ASCII TEXT ART FROM: http://patorjk.com/software/taag/#p=display&f=Slant
#    ___   ___      _____    __ __     ______   _____    _____   ____     ____     ____ 
#   <  /  |__ \    |__  /   / // /    / ____/  / ___/   /__  /  ( __ )   / __ \   / __ \
#   / /   __/ /     /_ <   / // /_   /___ \   / __ \      / /  / __  |  / /_/ /  / / / /
#  / /   / __/    ___/ /  /__  __/  ____/ /  / /_/ /     / /  / /_/ /   \__, /  / /_/ / 
# /_/   /____/   /____/     /_/    /_____/   \____/     /_/   \____/   /____/   \____/  
##

  filename = input("Enter TauNet filename: ")
  if filename == '!EXIT':
    return
  user_list = u_list(filename)
  user_info = None


  listen_thread = threading.Thread(target=listen, args = (user_list.key,))
  listen_thread.daemon = True
  listen_thread.start()


  ##Change in design:
  ##  Single command prompt "TauNet v0.1 >> "
  ##  Command   | result
  ##  ?         | Help Menu
  ##  ?string   | Search Help for string :: Last thing to impliment
  ##  @user mess| Send mess to user
  ##  @ mess    | Sends mess to last user to recieve a message
  ##  +user ip  | Add user
  ##  -user     | remove user
  ##  !EXIT     | Close program
  ##  undefined | Prompt user with how to access the help option
  while 1:
    split_command = None
    command = input(input_message)
    if command[0] == '@':
      #print("Message") #Try and send a message to user
      split_command = read_command(command)
      if(split_command[0] != ''):
        old_user = user_info
        user_info = None
        user_info = user_list.search_users(split_command[0])
      if user_info:
        send_message(user_info, split_command[1], user_list.key)
      else:
        user_info = old_user
        print("Invalid Command. ? for help\n") ##Invalid user_name
    elif command[0] == '?':
      print("  Command               | Description")
      print("  ----------------------+-------------------------------------------------------")
      print("  ?                     | Displays this dialogue")
      print("  @user_name Message    | Sends 'user_name' 'Message'")
      print("  @ Message             | Sends 'Message' to the last 'user_name' messaged")
      print("  +user_name ip_address | Adds 'user_name' to the list of users at 'ip_address.'")
      print("  -user_name            | Remove 'user_name' from the list of users.")
      print("  !EXIT                 | Exit the program")
      print("  ----------------------+-------------------------------------------------------")
    elif command[0] == '+': 
      split_command = read_command(command)
      user_list.add_user(split_command)
    elif command[0] == '-':
      user_list.remove_user(command[1:])
    elif command[0:5] == '!EXIT':
      return
    else:
      print("Invalid Command. ? for help\n")

if __name__ == "__main__":
  main()
