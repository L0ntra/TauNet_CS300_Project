# Copyright (c) 2015 Gregory Gaston
# License: https://opensource.org/licenses/MIT
# This file contains the class and functions used to recored messages
# recieved by users.

MAX_MESSAGES = 20



# <<<< <<<< <<<< mess_list class >>>> >>>> >>>> #
# DLL of messages
class mess_list:
  def __init__(self, sender = None, reciever = None, message = None, next_node = None):
    self.next_node = next_node
    self.prev_node = None
    self.sender = sender
    self.reciever = reciever
    self.message = message

  def add_message(self, sender, reciever, message):
    new_node = mess_list(sender, reciever, message, self)
    self.prev_node = new_node
    return new_node
    

  def print_n(self, n):
    try:
      n = n-1
      if n > 0 and self.next_node:
        self.next_node.print_n(n)
      if self.sender and self.reciever and self.message:
        print("\nSender: " + self.sender + "\t Reciever: " + self.reciever +
              "\nMessage: " + self.message)
    except: None
    return


# <<<< <<<< <<<< message_list class >>>> >>>> >>>> #
# Manages the mess_list class
class message_list:
  def __init__(self, sender = None, reciever = None, message = None):
    self.head = None
    self.total = 0
    if sender and reciever and message:
      self.head = mess_list(sender, reciever, message)
      self.total = 1
    self.tail = self.head

  def add_message(self, sender, reciever, message):
    if not self.head:
      self.tail = self.head = mess_list(sender, reciever, message)
      return None
    else:
      self.head = self.head.add_message(sender, reciever, message)
      self.total = self.total + 1
    if self.total > MAX_MESSAGES-1:
      assert(self.tail) #if tail is empty something bad happend
      self.remove_tail()
    return None

  def remove_tail(self):
    if not self.tail.prev_node:
      return None
    #unlink he tail.
    temp = self.tail.prev_node
    self.tail.prev_node.next_node = None
    self.tail.prev_node = None
    self.tail = temp
    self.total = self.total - 1
    return None

  def print_n(self, n):
    try:
      if n < 1:
        return None
      if self.head:
        self.head.print_n(n)
    except: None
    return None
