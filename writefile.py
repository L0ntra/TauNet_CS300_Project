##Instead of directly writing the file create the user_list object and
##Write a method for writing that method to a file.

##writes the file for the TauNet user list
def write_file():
  while 1:
    network_name = input("Network Name: ")
    if 'Y' == input("<<WARNING: If a Network with that name already exists it will be destroyed>> Continue? (Y/N): "):
      break

  f = open(network_name, 'w+')

  f.write(input("Network Key: ") + '\n')
  f.write(input("Your User Name: ") + '\n')
  user_name = ''
  ##write passkey
  while 1:
    user_name = input("User name: ")
    ip = input(user_name + "'s IP Address: ")
    if 'Y' == input("User name: " + user_name + "\nIP Address: " + ip + "\nIs this correct? (Y/N)"):
      f.write(user_name +'\n' + ip + '\n')
    if 'N' == input("Enter another User? (Y/N): "):
      break
  f.close()
  return

def add_users():
  network_name = input("Network Name: ")
  f = open(network_name, 'a+')
  f.seek(0,0)
  if f.readline() == '':  #file is empty report error
    return 
  f.seek(0,2)
  while 1:
    user_name = input("User name: ")
    ip = input(user_name + "'s IP Address: ")
    if 'Y' == input("User name: " + user_name + "\nIP Address: " + ip + "\nIs this correct? (Y/N)"):
      f.write(user_name +'\n' + ip + '\n')
    if 'N' == input("Enter another User? (Y/N): "):
      break
  f.close()
  return


#checks to see if a username is valid. Returns ture or false
def valid_user(user_name):
  # Must check for duplicates
  # Valid Characters a-z, A-Z, 0-9, '-'
  length = len(user_name)
  if length > 12 or length < 3:
    return False
  for i in range(0, length):
    if not ((user_name[i] >= 'a' and user_name[i] <= 'z') or (user_name[i] >= 'A' and user_name[i] <= 'Z') or (user_name[i] >= '0' and user_name[i] <= '9') or user_name[i] == '-'):
      return False
  return True

#checks to see if an ip address is valid. returns true or false
def valid_ip(ip):
  length = len(ip) #length of ip
  temp_char = ''
  temp_int = 0 #value of each ip section
  last = -1 # location of the last '.'
  total = 0 #total number of sections found
  for i in range(0, length+1):
    if i == length or ip[i] == '.':
      temp_char = int(ip[(last+1):(i)]) #1 after last '.'
      temp_int = int(temp_char)
      if temp_int > 255 or temp_int < 0: 
        return False  #IP not in a valid range
      total = total + 1
      last = i

  if total == 4:  #there must be exactly 4 blocks in an ip address
    return True
  return False

def main():
#  print(valid_ip('128.0.0.1'))       #true
#  print(valid_ip('1.1.1.256'))       #false
#  print(valid_ip('1.1.1.-1'))        #false
#  print(valid_ip('256.1.1.255'))     #false
#  print(valid_ip('-1.1.1.1'))        #false
#  print(valid_ip('255.255.255.255')) #true
#  print(valid_ip('1.1.1.1'))         #true
#  print(valid_ip('1.1.1.1.1'))       #false
#  print(valid_ip('1.1.1'))           #false
#  print(valid_ip('128'))             #false
#  print(valid_ip('1234567890'))      #false

  print(valid_user('aAzZ01-'))        #true   - All chars in range
  print(valid_user('aaa!'))           #false  - one char not in range
  print(valid_user('aa'))             #false  - too short
  print(valid_user('aaaaaaaaaaaaa'))  #false  - too long

  #write_file()
  #add_users()
  return

if __name__ == '__main__':
  main()
