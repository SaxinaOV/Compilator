from random import choice

def check(char):
    if char in ['a', 'b', 'c']:
        return True
    return False

class State:
    def __init__(self, next = {}):
        self.next = next 

class FSM:
    def __init__(self):
        self.q0 = State()
        self.q1 = State()
        self.q2 = State()
        self.q0.next = {'b': self.q0, 'a': self.q1}
        self.q1.next = {'a': self.q1, 'c': self.q2}

    def check_string(self, line):
        cur_state = self.q0
        for char in line:
            if check(char):
                try:
                    cur_state = cur_state.next[char]
                except KeyError:
                    return 0
            else:
                return 2
        if cur_state == self.q2:
            return 1
        return 0
        
    def random_string(self, n):
        my_string = ''
        cur_state = self.q0
        for i in range(n):
            if cur_state == self.q0:
                if len(my_string) < n-2:
                    cur_input = choice(('a', 'b'))
                else:
                    cur_input = 'a'
            elif cur_state == self.q1:
                if len(my_string) < n-1:
                    cur_input = 'a'
                else:
                    cur_input = 'c'
            my_string += cur_input
            cur_state = cur_state.next[cur_input]
        return my_string
    






