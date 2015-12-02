##LLL for the users
class user_node:
  def __init__(self, u_name = None, u_ip = None, next_node = None):
    self.next_node =  None
    self.user_name = u_name
    self.ip = u_ip
    return

  #add a new node at the begining. Returns the new head
  def add_node(self, u_name, u_ip):
    new_node = user_node(u_name, u_ip)
    new_node.next_node = self
    return new_node

  def remove_node(self, u_name):
    if self.user_name == u_name:
      return self.next_node
    if self.next_node:
      self.next_node = self.next_node.remove_node(u_name)
    return self

  #prints all users and their ip addrsses
  def print_node(self):
    print(self.user_name + ' (' + self.ip + ') ', end='')
    if self.next_node:
      self.next_node.print_node()
    return

  #Searches for matching user name and returns tuple (user_name, ip address)
  def search_user(self, u_name):
    if self.user_name == u_name:
      return (self.user_name, self.ip)
    if self.next_node:
      return self.next_node.search_user(u_name)
    return None

  #Searches for matching ip and returns tuple (user_name, ip address)
  #May want to add ability to return all Users with the specified IP
  def search_ip(self, u_ip):
    if self.ip == u_ip:
      return (self.user_name, self.ip)
    if self.next_node:
      return self.next_node.search_ip(u_ip)
    return None

class u_list:
  #User list must be initialized with a filename.
  def __init__(self, filename = None):
    if filename:
      f = open(filename)
      self.key = f.readline().strip('\n') # Read in Key
      self.me = f.readline().strip('\n')  # Read in my user name
      self.user_list = self.read_file(f)
      f.close()
    else:
      self.key = None
      self.me = None
      self.user_list = None
    self.filename = filename
    return

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
      self.key = input("Input TauNet ket: ")
      if input("Key = " + self.key + "\nIs this correct? (y/n): ") == 'y':
        break
    while True:
      self.me = input("Input your user name: ")
      if input("user name = " + self.me + "\nIs this correct? (y/n): ") == 'y':
        break
    print("Creating the list of other users on your TauNetwork:")
    while True:
      while True:
        user = input("Input user name: ")
        ip = input("Input " + user + "'s IP address: ")
        print("Username = " + user + " IP = " + ip)
        if input("Is this correct? (y/n): ") == 'y':
          if self.user_list:
            if self.add_user((user, ip)):
              print(user + " has already been added to the user list.")
          else:
            self.user_list = user_node(user, ip, self.user_list)
          break
      if not (input("Enter another user? (y/n): ") == 'y'):
        break
    self.filename = filename
    self.write_file()
    return

  def write_file(self):
    assert self.filename
    f = open(self.filename, 'w')
    assert f
    f.write(self.key + '\n')
    f.write(self.me + '\n')
    current = self.user_list
    while current:
      if current.user_name and current.ip:
        f.write(current.user_name + '\n')
        f.write(current.ip +'\n')
      current = current.next_node
    return

  #Reads in the users from the file
  def read_file(self, f):
    user_name = f.readline().strip('\n')
    user_ip = f.readline().strip('\n')
    if not user_name or not user_ip: #End Of File
      return None
    user_list = user_node(user_name, user_ip) 
    user_list.next_node = self.read_file(f)
    return user_list

  #Seach the userlist for a user name and return (user_name, IP)
  #if found or None if not found
  def search_users(self, user_name):
    if self.user_list:
      return self.user_list.search_user(user_name)
    return None

  #Search the userlist for an IP address and return (user name, IP)
  #if found or None if not found
  def search_ip(self, user_ip):
    if self.user_list:
      return self.user_list.search_ip(user_ip)
    return None
  
  #prints all usernames and their ip addresses
  def print_users(self):
    if self.user_list:
      return self.user_list.print_node()
    return None

  #Adds a user to the list of users
  #user_info == (user_name, user_ip)
  def add_user(self, user_info):
    if not self.search_users(user_info[0]): ## make sure the user name isn't already taken
      self.user_list = self.user_list.add_node(user_info[0], user_info[1])
      return True
    return False

  #Removes a user from the list of user
  def remove_user(self, user_name):
    if(self.user_list and self.search_users(user_name)):
      self.user_list = self.user_list.remove_node(user_name)
      return True
    return False

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
