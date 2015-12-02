class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def str_val(self):
        if self.type == 'array':
            str_vals = ''
            for val in self.value:
                str_vals += val.str_val()
            return str_vals
        else:
            return str(self.value)

    def debug_val(self):
        if self.type == 'array':
            str_vals = '['
            for val in self.value:
                str_vals += val.str_val() + ' '
            return str_vals[:-1] + ']'
        elif self.type == 'string':
            return '"' + self.value + '"'
        else:
            return str(self.value)

    def __str__(self):
        return str(self.value)

    def is_truthy(self):
        if self.type == 'integer':
            return self.value != 0
        else:
            return 0


class Inter:
    def __init__(self):
        self.stack = []
        self.arr_markers = []  # array markers, thx aditsu
        self.variables = {}  # TODO: add more variables

    def run_code(self, code):
        # print(self)
        # print(code)
        for command in code:
            # print(command)
            if command['token_type'] == 'integer':
                self.stack.append(Token('integer', command['token_value']))
            if command['token_type'] == 'operator':
                self.do_operator(command['token_value'])
            if command['token_type'] == 'string':
                self.stack.append(Token('string', command['token_value']))

    def do_operator(self, op):
        if op == '+':
            if len(self.stack) < 2:
                self.error('Not enough items on stack')
                return
            y = self.pop()
            x = self.pop()
            if x.type == 'integer' and y.type == 'integer':
                self.stack.append(Token('integer', x.value + y.value))
            elif x.type == 'string' or y.type == 'string':
                self.stack.append(Token('string', x.str_val() + y.str_val()))
        if op == '-':
            if len(self.stack) < 2:
                self.error('Not enough items on stack')
                return
            y = self.pop()
            x = self.pop()
            if x.type == 'integer' and y.type == 'integer':
                self.stack.append(Token('integer', x.value - y.value))
            else:
                self.error("Values not integer")
                return
        if op == '*':
            if len(self.stack) < 2:
                self.error('Not enough items on stack')
                return
            y = self.pop()
            x = self.pop()
            if x.type == 'integer' and y.type == 'integer':
                self.stack.append(Token('integer', x.value * y.value))
            else:
                self.error("Values not integer")
                return
        if op == '/':
            if len(self.stack) < 2:
                self.error('Not enough items on stack')
                return
            y = self.pop()
            x = self.pop()
            if x.type == 'integer' and y.type == 'integer':
                self.stack.append(Token('integer', x.value / y.value))
            else:
                self.error("Values not integer")
                return
        if op == '=':
            if len(self.stack) < 2:
                self.error('Not enough items on stack')
                return
            y = self.pop()
            x = self.pop()
            if x.value == y.value:
                self.stack.append(Token('integer', 1))
            else:
                self.stack.append(Token('integer', 0))
        if op == '^':
            if len(self.stack) < 2:
                self.error('Not enough items on stack')
                return
            exp = self.pop()
            base = self.pop()
            if exp.type == 'integer' and base.type == 'integer':
                self.stack.append(Token('integer', base.value ** exp.value))
            else:
                self.error('Values not integer')
                return

        if op == ';':
            if len(self.stack) < 1:
                self.error('Not enough items on stack')
                return
            self.pop()
        if op == '[':
            self.arr_markers.append(len(self.stack))
        if op == ']':
            amount_to_rem = -(len(self.stack) - self.arr_markers.pop())
            new_arr = self.stack[amount_to_rem:]
            self.stack = self.stack[:amount_to_rem]
            self.stack.append(Token('array', new_arr))
        if op == '@':
            if len(self.stack) < 2:
                self.error('Not enough items on stack')
                return
            index = self.pop()
            arr = self.pop()
            if index.type == 'integer' and arr.type == 'array':
                try:
                    self.stack.append(Token('integer', arr.value[index.value]))
                except IndexError:
                    self.error('Index out of range')
            else:
                self.error('Values not integer')
                return
        if op == '~':
            if len(self.stack) < 1:
                self.error('Not enough items on stack')
                return
            item = self.pop()

            if item.type == 'integer':
                self.stack.append(Token('ineger', -item.value))
            else:
                self.stack.append(item)
        if op == '!':
            if len(self.stack) < 1:
                self.error('Not enough items on stack')
                return
            item = self.pop()

            if item.type == 'integer':
                if item.is_truthy():
                    new = 0
                else:
                    new = 1
                self.stack.append(Token('integer', new))
        if op == 'r':
            if len(self.stack) < 1:
                self.error('Not enough items on stack')
                return
            item = self.pop()
            if item.type == 'integer':
                array = map(lambda i: Token('integer', i),
                            range(item.value))
                self.stack.append(Token('array', array))
            else:
                self.error('Values not integer')
                return
        if op == '.r':
            if len(self.stack) < 2:
                self.error('Not enough items on stack')
                return
            last_index = self.pop()
            first_index = self.pop()
            if last_index.type == 'integer' and first_index.type == 'integer':
                array = map(lambda i: Token('integer', i),
                            range(first_index.value, last_index.value))
                self.stack.append(Token('array', array))
            else:
                self.error('Values not integer')
                return
        if op == '.d':
            self.debug()
        if op == '\\':
            if len(self.stack) < 2:
                self.error('Not enough items on stack')
                return
            x = self.pop()
            y = self.pop()
            self.stack.append(x)
            self.stack.append(y)

    def output(self):
        print("".join(list(map(lambda x: x.str_val(), self.stack))))

    def error(self, message):
        print('Error: ' + message)

    def pop(self):
        if len(self.arr_markers) > 0:
            if self.arr_markers[-1] == len(self.stack):
                self.arr_markers[-1] -= 1
        return self.stack.pop()

    def debug(self):
        print('Stack: [' + ' '.
              join(list(map(lambda x: x.debug_val(), self.stack)))
              + ']')
        print('Array Markers: ' + str(self.arr_markers))
