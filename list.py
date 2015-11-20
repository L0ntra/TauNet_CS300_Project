class user_node:
  def __init__(self, data):
    self.next_node =  None
    self.data = data
    return

  def add_node(self, data):
    if not self.next_node:
      self.next_node = user_node(data)
      return
    self.next_node.add_node(data)
    return

  def print_node(self):
    print(self.data, end='')
    if self.next_node:
      self.next_node.print_node()
    return

u_node = user_node(1)
u_node.add_node(2)
u_node.add_node(3)
u_node.print_node()

