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
      if len(self.stack) < 2:
        self.error('Not enough items on stack')
        return
      x = self.stack.pop()
      y = self.stack.pop()
      if x['type'] == 'integer' and y['type'] == 'integer':
        self.stack.append({'type': 'integer', 'value': x['value'] + y['value']})
      else:
        self.error("Values not integer")
        return

  def error(self, message):
    print('Error: ' + message)