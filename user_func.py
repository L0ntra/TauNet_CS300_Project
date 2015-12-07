# Copyright (c) 2015 Gregory Gaston
# License: https://opensource.org/licenses/MIT
# This file containes the functions needed to impliment the list of
# nodes on the TauNetwork. Each user_node stores the user_name, 
# address, and next_node in the list. u_list manages the nodes in
# the user list.


# <<<< <<<< <<<< User_node Class >>>> >>>> >>>> #
# Linearl linked list for the users
class user_node:
  def __init__(self, u_name = None, u_ip = None, next_node = None):
    self.next_node =  None
    self.user_name = u_name
    self.ip = u_ip
    return

  # Add a new node at the begining. Returns the new head
  def add_node(self, u_name, u_ip):
    new_node = user_node(u_name, u_ip)
    new_node.next_node = self
    return new_node

  # Searches for the user_name, u_name, and removes it.
  def remove_node(self, u_name):
    if self.user_name == u_name:
      return self.next_node
    if self.next_node:
      self.next_node = self.next_node.remove_node(u_name)
    return self

  # Prints all users and their ip addrsses
  def print_node(self):
    print(self.user_name + ' (' + self.ip + ')', end='   ')
    if self.next_node:
      self.next_node.print_node()
    return

  # Searches for matching user name and returns tuple (user_name, ip address)
  def search_user(self, u_name):
    if self.user_name == u_name:
      return (self.user_name, self.ip)
    if self.next_node:
      return self.next_node.search_user(u_name)
    return None

  # Searches for matching ip and returns tuple (user_name, ip address)
  # May want to add ability to return all Users with the specified IP
  def search_ip(self, u_ip):
    if self.ip == u_ip:
      return (self.user_name, self.ip)
    if self.next_node:
      return self.next_node.search_ip(u_ip)
    return None



# <<<< <<<< <<<< u_list class >>>> >>>> >>>> #
# Manages the list of TauNet users
class u_list:
  def __init__(self, filename = None):
    exists = True
    try:
      open(filename)
    except:
      exists = False
    if filename and exists:
      f = open(filename)
      self.key = f.readline().strip('\n') # Read in Key
      self.me = f.readline().strip('\n')  # Read in my user name
      if self.key == '' or self.me == '':
        sefl.key = self.me = None
      self.user_list = self.read_file(f)
      f.close()
    else:
      self.key = None
      self.me = None
      self.user_list = None
    self.filename = filename
    return

  # Genorates the file that represents the TauNetowrk
  def input_u_list(self, filename = None):
    if not filename:
      while True:
        filename = input("Input file name to create: ")
        try:
          open(filename)
        except IOError:
          break
        else:
          if input("WARNING: File alredy exists. Overwrite? (y/n): ") == 'y':
            break
    while True:
      self.key = input("Input TauNet key: ")
      if input("Key = " + self.key + "\nIs this correct? (y/n): ") == 'y':
        break
    while True:
      self.me = input("Input your user name: ")
      if not valid_user(self.me):
        print("Error: Invalid user name.\nUsers names may only contain uppercase and lowercase letters from a-z, the numbers from 0-9, and the - symbol.")
      elif input("user name = " + self.me + "\nIs this correct? (y/n): ") == 'y':
        break
    print("Creating the list of other users on your TauNetwork:")
    while input("Enter a tauNet user? (y/n): ") == 'y':
      while True:
        user = input("Input user name: ")
        ip = input("Input " + user + "'s address: ")
        print("Username = " + user + " IP = " + ip)
        if input("Is this correct? (y/n): ") == 'y':
          if not valid_user(user):
            print("Error: Invalid user name.\nUsers names may only contain uppercase and lowercase letters a-z, the numbers 0-9, and the - symbol.")
          elif self.add_user((user, ip)):
            print(user + " has already been added to the user list.")
          break
        break
    self.filename = filename
    self.write_file()
    return


  # Write the u_list (user_list) to file.
  #XXX Future update: Encrypt the file with RC4
  def write_file(self):
    assert self.filename
    f = open(self.filename, 'w+')
    assert f
    f.write(self.key + '\n')
    f.write(self.me + '\n')
    current = self.user_list
    while current:
      assert current
      if current.user_name and current.ip:
        f.write(current.user_name + '\n')
        f.write(current.ip +'\n')
      current = current.next_node
    return


  # Recursively reads in the users from the file
  #XXX Future update: Decrypth the file with RC4
  #XXX This will require a complete rework of this function
  def read_file(self, f):
    user_name = f.readline().strip('\n')
    user_ip = f.readline().strip('\n')
    if not user_name or not user_ip: #End Of File
      return None
    user_list = user_node(user_name, user_ip) 
    user_list.next_node = self.read_file(f)
    return user_list


  # Seach the userlist for a user name and return (user_name, IP)
  # if found or 'None' if not found
  def search_users(self, user_name):
    if self.user_list:
      return self.user_list.search_user(user_name)
    return None


  # Search the userlist for an IP address and return (user name, IP)
  # if found or 'None' if not found
  def search_ip(self, user_ip):
    if self.user_list:
      return self.user_list.search_ip(user_ip)
    return None


  # Prints all usernames and their ip addresses
  def print_users(self):
    if self.user_list:
      return self.user_list.print_node()
    return None


  # Adds a user to the list of users. user_info == (user_name, user_ip)
  def add_user(self, user_info):
    # Make sure the user name isn't taken
    if not self.user_list:
      self.user_list = user_node(user_info[0], user_info[1], self.user_list)
      return True
    if not self.search_users(user_info[0]):
      self.user_list = self.user_list.add_node(user_info[0], user_info[1])
      return True
    return False


  # Removes a user from the list of user
  def remove_user(self, user_name):
    if(self.user_list and self.search_users(user_name)):
      self.user_list = self.user_list.remove_node(user_name)
      return True
    return False


# <<<< <<<< <<<< General functions for users >>>> >>>> >>>> #

# checks to see if a username is valid. Returns ture or false
def valid_user(user_name):
  # Must check for duplicates
  # Valid Characters a-z, A-Z, 0-9, '-'
  length = len(user_name)
  if length > 30 or length < 3:
    return False
  for i in range(0, length):
    if not ((user_name[i] >= 'a' and user_name[i] <= 'z') or (user_name[i] >= 'A' and user_name[i] <= 'Z') or (user_name[i] >= '0' and user_name[i] <= '9') or user_name[i] == '-'):
      return False
  return True


# Checks for a properly formattd ip address. returns True or False
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


# main for Testing
def main():
  filename = "users"
  users = u_list(filename)
  print(users.key)
  print(users.me)

  print('\n\n')
  print(users.search_users('user3'))
  print(users.search_ip('127.0.0.1'))
  users.print_users()
#  print('\n\n')

if __name__ == "__main__":
  main()
