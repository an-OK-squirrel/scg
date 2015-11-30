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

    def __str__(self):
        return str(self.value)


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
            val = self.pop()

            if val.type == 'integer':
                self.stack.append(Token('ineger', -val.value))

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
        print('Stack: ' + str(list(map(str, self.stack))))
        print('Array Markers: ' + str(self.arr_markers))
