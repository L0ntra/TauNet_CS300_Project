# Copyright (c) 2015 Gregory Gaston
# License: https://opensource.org/licenses/MIT
# The purpouse of this file is to test, as fully is as reasonable, all 
# functions in the TauNet program.

# My Libs
import main, saber, messages, protocol, user_func
# Built in Libs
import time, threading

## saber.py
print("<<<< <<<< <<<< Testing Saber.py >>>> >>>> >>>>")
print("Testing encryption:")
test_string = "1234567890 abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ `~!@#$%^&*()_+-=[]\{}|;,./<>? '" + '"'
print("Unencrypted Test String: " + test_string)
t_string = [ord(test_string[i]) for i in range(len(test_string))]
enc_test_string = saber.encrypt(t_string, 20, 'password')
print("Testing decryption:")
dec_t_string = saber.decrypt(enc_test_string, 20, 'password')
dec_test_string = ''
for i in range(len(dec_t_string)):
  dec_test_string = dec_test_string + chr(dec_t_string[i])
print("Decrypted Test STring: " + dec_test_string)
test_string = 'Al Dakota buys'
t_string = [ord(test_string[i]) for i in range(len(test_string))]
print("Standardized CipherSaber-2 Test String:\n" + test_string)
dec_t_string = saber.decrypt(t_string, 20, 'Al')
dec_test_string = ''
for i in range(len(dec_t_string)):
  dec_test_string = dec_test_string + chr(dec_t_string[i])
print("mead == " + dec_test_string)
wait = input("[Enter to Contine]")
wait = None

## protocol.py
print("\n\n<<<< <<<< <<<< Testing Protocol.py >>>> >>>> >>>>")
print("From: Sender\nTo: Reciever\nMessage: This is a protocol test")
print("v0.1")
message = protocol.write_message(("Reciever", '255.255.255.255'), ("Sender", '1.1.1.1'), "This is a protocol test", '0.1')
print("Composed Message:\n" + message)
read_message = protocol.read_message(message)
print("Decomposed Message:")
print(read_message)

print("v0.2")
message = protocol.write_message(("Reciever", '255.255.255.255'), ("Sender", '1.1.1.1'), "This is a protocol test", '0.2')
print("Composed Message:\n" + message)
read_message = protocol.read_message(message)
print("Decomposed Message:")
print(read_message)
wait = input("[Enter to Contine]")
wait = None

## messages.py
print("\n\n<<<< <<<< <<<< Testing messages.py >>>> >>>> >>>>")
mess_list = messages.message_list()
print("Print_n on an empty list: (Print None)")
mess_list.print_n(4)
print("Adding 15 messages to the message list in revers order.\nSender: Sender\nReciever: Reciever, Message: str(i) | for i = 30 to 15")
for i in range(30,15,-1):
  mess_list.add_message("Sender", "Reciever", str(i))
print("Print -1 messages: (Print None)")
mess_list.print_n(-1)
print("Print 25 messages: (Print 15 messages)")
mess_list.print_n(25)
print("Print 4 messages: (Print 4 messages)")
mess_list.print_n(4)
print("Print 'a' messages: (Print None)")
mess_list.print_n('a')
print("Adding 15 more messages to the message list in revers order.\nSender: Sender\nReciever: Reciever, Message: str(i) | for i = 15 to 0")
for i in range(15,0,-1):
  mess_list.add_message("Sender", "Reciever", str(i))
print("Print 25 messages: (Print 20 messages)")
mess_list.print_n(25)
wait = input("[Enter to Contine]")
wait = None

## user_func.py
print("\n\n<<<< <<<< <<<< user_func.py >>>> >>>> >>>>")
print("Attempting to open test_file.txt. To test opening files that do not exist, ensure that test_file.txt does not exist.")
user_list = user_func.u_list('test_file.txt') #might exist
print("setting user_list.key = '1234567890' and user_list.me = 'user0'")
user_list.key = '1234567890'
user_list.me = 'user0'
print("Adding users0 throuhg user20, all with ip '127.0.0.1'")
for i in range(0,21):
  user_list.add_user(("user"+str(i), '127.0.0.1'))
print("Printing all users in network")
user_list.print_users()
print("Searching for 'user10': Return user_info")
print(user_list.search_users('user10'))
print("Removing 'user10'")
user_list.remove_user('user10')
print("Searching for 'user10': Return None (print True)")
print(user_list.search_users('user10') == None)
print("Writing file")
user_list.write_file()
print("Reading test_file.txt in to new user_list")
user_list_2 = user_func.u_list('test_file.txt')
print("key: " + user_list_2.key + "\nme: " + user_list_2.me)
print("users in user_list_2")
user_list_2.print_users()
wait = input("[Enter to Contine]")
wait = None
print("Testing Valid User Names\nUser Name | Expected | Result")
print("Borders of charactes in range")
print("aAzZ09- | True | ", str(user_func.valid_user('aAzZ09-')))
print("User Name Lengths")
print("123456789012345678901234567890 (len = 30) | True | ", str(user_func.valid_user('123456789012345678901234567890')))
print("1234567890123456789012345678901 (len = 31 )| False | ", str(user_func.valid_user('1234567890123456789012345678901')))
print("12 | False | ", str(user_func.valid_user('12')))
print("123 | True | ", str(user_func.valid_user('123')))
print("Borders of characters out of range")
print("user/ | False | ", str(user_func.valid_user('user/')))
print("user: | False | ", str(user_func.valid_user('user:')))
print("user@ | False | ", str(user_func.valid_user('user@')))
print("user[ | False | ", str(user_func.valid_user('user[')))
print("user` | False | ", str(user_func.valid_user("user`")))
print("user{ | False | ", str(user_func.valid_user('user{')))


print("<<<< <<<< <<<< Testing main.py >>>> >>>> >>>>")
print("Testing of main.py shall be done manually be entering the following commands in order to the prompts:\n(it should be noted that the messages sent will be recieved by the user on the same system)")
print("Test 1:")
print("Prompt:        | Input                  | Expected operation\n" +
      "Enter TauNet filename:  | test_file.txt | Load test_file.txt as u_list\n" +
      "TauNet v0.2>>  | @user0 hello1          | Sends 'hello1' to user0\n" +
      "TauNet v0.2>>  | @user20 hello2         | Sends 'hello2' to user20\n" +
      "TauNet v0.2>>  | @ hello3               | Sends 'hello3' to user20\n" +
      "TauNet v0.2>>  | @user10 hello4         | prints invalid command message\n" +
      "TauNet v0.2>>  | +userr 192.168.1.254   | add userr to user_list with \n" +
      "               |                        | address 192.168.1.254\n" +
      "TauNet v0.2>>  | +aAzZ09- 127.0.0.1     | add aAzZ01- to user_list with\n" +
      "               |                        | address 127.0.0.1\n" +
      "TauNet v0.2>>  | +user! 1.1.1.1         | print user name error message\n" +
      "TauNet v0.2>>  | +usr 1.1.1.1           | print user name error message\n" +
      "TauNet v0.2>>  | 1234567890123456789012345678901 | print user name error message\n"+
      "TauNet v0.2>>  | @userr hello5          | Unable to send message error\n" +
      "Attempt to resend message? (y/n) | y    | Unable to send message error\n" +
      "Attempt to resend message? (y/n) | n    | Discard message return to prompt\n" +
      "TauNet v0.2>>  | -userr                 | Remove uerrr from the user_list\n" +
      "TauNet v0.2>>  | @ hello6               | Prints invaild command message\n" +
      "TauNet v0.2>>  | @userr hello7          | Prints invalid command message\n" +
      "TauNet v0.2>>  | #21                    | Prints command error message\n" +
      "TauNet v0.2>>  | #-1                    | Prints command erorr message\n" +
      "TauNet v0.2>>  | #a                     | Prints command error message\n" +
      "TauNet v0.2>>  | #                      | Prints command error message\n" +
      "TauNet v0.2>>  | #1                     | Prints message 'hello3' message info\n"+
      "TauNet v0.2>>  | #20                    | Prints message 'hello1', 'hello2',\n"+
      "               |                        | 'hello3' in that order.\n"
      "TauNet v0.2>>  | ~                      | Prints a list of all users.\n" +
      "               |                        | user20 -> user0, but no user10\n" +
      "TauNet v0.2>>  | ?                      | Prints help menu\n" +
      "TauNet v0.2>>  | !CLEAR                 | Screen is cleard\n" +
      "TauNet v0.2>>  | !EXIT                  | Program Exits\n")

wait = input("[Enter to Contine]")
wait = None

print("Test 2:")
lmtest = True
try:
  open("test_file.txt")
except:
  lmtest = False
print("Activate Long Message test == ", lmtest)
if lmtest:
  main.main(True)
print("\nLong Message Test Complete:")
wait = input("[Enter to Contine]")
wait = None

print("Test 3:")
print("Prompt:                | Input         | Expected operation\n" +
      "Enter TauNet filename: | test2         | File does not exist prompt\n" +
      "Would you like to crate it? (y/n) | n  | Return to TauNet filename prompt\n" +
      "Enter TauNet filename: | test2         | File does not exist prompt\n" +
      "Would you like to crate it? (y/n) | y  | Enter File Creation Dialogue\n" +
      "Input TauNet key       | password      | correct? prompt\n" +
      "Is this correct? (y/n) | n             | Return to key prompt\n" +
      "Input TauNet key       | password      | correct? prompt\n" +
      "Is this correct? (y/n) | y             | TauNet Key = password\n" +
      "Input your Username:   | user0         | correct? prompt\n" +
      "Is this correct? (y/n) | n             | Return to user name prompt\n" +
      "Input your Username:   | user0         | correct? prompt\n" +
      "Is this correct? (y/n) | y             | TauNet user name = user0\n" +
      "Enter a TauNet User? (y/n) | y         | Input user name prompt\n" +
      "Input user name:       | user0         | Input user0's address prompt\n" +
      "Input user0's address  | 127.0.0.1     | correct? prompt\n" +
      "Is this correct? (y/n) | n             | Enter a TauNet user prompt\n" +
      "Enter a TauNet user? (y/n) | y         | Input user name prompt\n" +
      "Input user name:       | user0         | Input user0's address prompt\n" +
      "Input user0's address  | 127.0.0.1     | correct? prompt\n" +
      "Is this correct? (y/n) | y             | user0 is added to user list\n" +
      "                       |               | Enter a TauNet user prompt\n" +
      "Enter a TauNet user? (y/n) | y         | Input user name prompt\n" +
      "Input user name:       | user1         | Input user1's address prompt\n" +
      "Input user1's address  | 127.0.0.1     | correct? prompt\n" +
      "Is this correct? (y/n) | y             | user1 is added to user list\n" +
      "                       |               | Enter a TauNet user prompt\n" +
      "Enter a TauNet user? (y/n) | y         | Input user name prompt\n" +
      "Input user name:       | user1         | Input user1's address prompt\n" +
      "Input user1's address  | 127.0.0.1     | correct? prompt\n" +
      "Is this correct? (y/n) | y             | user already added message\n" +
      "                       |               | Enter a TauNet user prompt\n")
wait = input("[Enter to Contine]")
wait = None
print("Enter a TauNet user? (y/n) | y         | Input user name prompt\n" +      
      "Input user name:       | ua            | Input ua's address prompt\n" +
      "Input ua's address     | 127.0.0.1     | correct? prompt\n" +
      "Is this correct? (y/n) | y             | user name error message\n" +
      "                       |               | Enter a TauNet user prompt\n" +
      "Enter a TauNet user? (y/n) | y         | Input user name prompt\n" +
      "Input user name:       | 1234567890123456789012345678901 |\n" +
      "                       |               | Input address prompt\n" +
      "Input 's      address  | 127.0.0.1     | correct? prompt\n" +
      "Is this correct? (y/n) | y             | User name error message\n" +
      "                       |               | Enter a TauNet user prompt\n" +
      "Enter a TauNet user? (y/n) | y         | Input user name prompt\n" +
      "Input user name:       | user!         | Input user!'s address prompt\n" +
      "Input user!'s address  | 127.0.0.1     | correct? prompt\n" +
      "Is this correct? (y/n) | y             | User name error message\n" +
      "                       |               | Enter a TauNet user prompt\n" +
      "Enter a TauNet user? (y/n) | n         | Writes file displays TauNet prompt\n" +
      "TauNet v0.2>>          | @user1 hello1 | Sends hello1 to user1\n" +
      "TauNet v0.2>>          | @user! hello2 | Invalid Command message\n" +
      "TauNet v0.2>>          | !EXIT         | Exit program\n" +
      "<Reopen program>\n" +
      "Enter TauNet filename: | test2         | test2 taunet loaded in to user_list\n" +
      "TauNet v0.2>>          | @user1 hello3 | Sends hello3 to user1\n" +
      "TauNet v0.2>>          | !EXIT         | Exit program")
print("<<<< <<<< <<<< TESTS COMPLETE >>>> >>>> >>>>")
