# Copyrigh (c) 2015 Gregory Gaston
#
#

##BRILLIANT IDEA!!! Thanks to Renee.
#After messages is displayed print the input message again to make it feel like
#there was no interruption in the message


from readfile import u_list
import socket
import threading
import time
import os

port = 6283
message = ''
user = ''
myip = socket.gethostbyname(socket.gethostname())
protocol_version = '0.1'
input_message = "TauNet v" + protocol_version + ">> " #Global variable


# Decyphers the message in to parts
def decypher(mess):
  length = len(mess)           #message lenght
  messtype = mess[0]            #first char is message type
  i = 2                         #second char is first delim
  while mess[i] != '|':         #search for the second delim
    i = i+1
  ip = mess[2:i]
  message = mess[i+1:length]
  return (messtype,ip,message)  

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

#
def send_message(user_info, message):
  s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
  s.connect((user_info[1], port))
  s.send(('m|' + myip +'|'+ message).encode())
  s.shutdown(1)
  s.close()
  return

# Listens for incoming messages
def listen():
  s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
  s.bind(('', 6283))
  while 1:
    s.listen(5)
    (conn , addr) = s.accept()
    mess = conn.recv(1024).decode() #decode convers from bytes to string
                                    #Hangs untill message is recieved
    decy_mess = decypher(mess)
    print("\nlisten: " + decy_mess[0] + ' ' + decy_mess[1] + ' ' 
          + decy_mess[2] + '\n' + input_message, end = '')
  return

############
### MAIN ###
############
def main():
  os.system('cls')
  print("                     _   __     __               ____   ___\n" +
        "   _____ ___  __  __/ | / /__  / /_    _   __   / __ \ <  /\n" +
        "  /  __/ __ `/ / / /  |/ / _ \/ __/   | | / /  / / / / / / \n" +
        "  / /_/ /_/ / /_/ / /|  /  __/ /_     | |/ /  / /_/ / / /  \n" +
        "  \__/\__,_/\__,_/_/ |_/\___/\__/     |___/   \____(_)_/   \n" +
        "\n")
                                                                                                  
  listen_thread = threading.Thread(target=listen)
  listen_thread.daemon = True
  listen_thread.start()

  filename = input("Enter TauNet filename: ")
  user_list = u_list(filename)
  user_info = None

  ##Change in design:
  ##  Single command prompt "TauNet v0.1 >> "
  ##  Command   | result
  ##  ?         | Help Menu
  ##  ?string   | Search Help for string :: Last thing to impliment
  ##  @user mess| Send mess to user
  ##  +user ip  | Add user
  ##  -user     | remove user
  ##  !EXIT     | Close program
  ##  undefined | Prompt user with how to access the help option
  while 1:
    split_command = None
    user_info = None
    command = input(input_message)
    if command[0] == '@':
      #print("Message") #Try and send a message to user
      split_command = read_command(command)
      user_info = user_list.search_users(split_command[0])
      if user_info:
        send_message(user_info, split_command[1])
      else:
        print("Invalid Command. ? for help\n") ##Invalid user_name
    elif command[0] == '?':
      print("  Command               | Description")
      print("  ----------------------+-------------------------------------------------------")
      print("  ?                     | Displays this dialogue")
      print("  @user_name Message    | Sends 'user_name' 'Message'")
      print("  +user_name ip_address | Adds 'user_name' to the list of users at 'ip_address.'")
      print("  -user_name            | Remove 'user_name' from the list of users.")
      print("  !EXIT                 | Exit the program")
      print("  ----------------------+-------------------------------------------------------")
#   elif command[0] == '+': 
      #Add (user, ip)
#   elif command[0] == '-':
      #remove user
    elif command[0:5] == '!EXIT':
      return
    else:
      print("Invalid Command. ? for help\n")


#while message != 'EXIT':
#  user_info = None
#  input_message = "Input User Name: "
#  while not user_info:
#    user = input(input_message)
#    user_info = users.search_users(user)

  #Create function Send_message(ip, message)
#  input_message = 'Input message: '
#  message = input(input_message)
#  enco_mess = 'm|' + myip + '|' + message
#s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
#s.connect(('127.0.0.1', port))
#  s.send(enco_mess.encode())
#  s.shutdown(1)
#  s.close()



#s.send('test1'.encode()) #encode converts variable to bytes
#time.sleep(2)
#s.send('test2'.encode())
#time.sleep(2)
#s.send('test3'.encode())
#time.sleep(2)
#s.send('test4'.encode())
#time.sleep(2)
#s.send('test5'.encode())
#time.sleep(2)
#s.send('EXIT'.encode())

#l.join()

if __name__ == "__main__":
  main()
