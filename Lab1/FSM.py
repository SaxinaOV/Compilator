from random import choice

count_digits = 0

def err1():
    print('строка не соответствует\n')

def check(char):
    if char in ['0', '1']:
        return True
    print('символ не из алфавита\n')
    return False

class State:
    def __init__(self, next = {}):
        self.next = next 

class FSM:
    def __init__(self):
        self.q0 = State()
        self.q1 = State()
        self.q2 = State()
        self.err = State()
        self.q0.next = {'0': self.q0, '1': self.q1}
        self.q1.next = {'0': self.q2, '1': self.q1}
        self.q2.next = {'0': self.q0, '1': self.err}

    def check_string(self, line):
        cur_state = self.q0
        for char in line:
            if check(char):
                cur_state = cur_state.next[char]
                if cur_state == self.err:
                    print('строка не соответствует\n')
                    return False
            else:
                return False
        return True
        
    def random_string(self, n):
        my_string = ''
        cur_state = self.q0
        for i in range(n):
            if cur_state != self.q2:
                cur_input = choice(list(cur_state.next.keys()))
            else:
                cur_input = '0'
            my_string += cur_input
            cur_state = cur_state.next[cur_input]
        return my_string
    






