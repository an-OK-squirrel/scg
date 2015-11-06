class Inter:
  def __init__(self):
    self.stack = []
    self.variables = {}  # TODO: add more variables

  def run_code(self, code):
    print(self)
    print(code)
    for command in code:
      print(command)
      if command['token_type'] == 'integer':
        self.stack.append({'type': 'integer', 'value': command['token_value']})
      if command['token_type'] == 'operator':
        self.do_operator(command['token_value'])
        print(command['token_value'])

  def do_operator(self, op):
    if op == '+':
      x = self.stack.pop()['value']
      y = self.stack.pop()['value']
      self.stack.append({'type': 'integer', 'value': x + y})