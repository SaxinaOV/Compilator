import random

class PDA:
    def __init__(self):
        self.stack = ['!']
        self.delta_dic = {(0, 'a', '!'): (0, '!A'),
                        (0, 'a', 'A'): (0, 'AA'),
                        (0, 'b', '!'): (1, '!A'),
                        (0, 'b', 'A'): (1, 'AA'),
                        (0, '#', '!'): (3, '!'),
                        (0, '#', 'A'): (3, '!'),
                        (0, 'c', '!'): (4, '!'),
                        (0, 'c', 'A'): (2, ''),
                        (1, 'b', 'A'): (1, 'AA'),
                        (1, 'c', 'A'): (2, ''),
                        (1, '#', 'A'): (3, '!'),
                        (2, 'c', 'A'): (2, ''),
                        (2, 'c', '!'): (4, '!'),
                        (2, '#', '!'): (4, '!'),
                        (2, '#', 'A'): (3, '!')}

    def check_string(self, s):
        state = 0
        for c in s:
            try:
                new_state, push_s = self.delta_dic[(state, c, self.stack[-1])]
            except KeyError:
                new_state = 5
                push_s = ''
            self.stack.pop()
            if push_s:
                for i in push_s:
                    self.stack.append(i)
            if new_state == 5 or (c == '#' and s.index(c) != len(s)-1):
                return("символ не из алфавита")
            elif new_state == 3:
                return("строка принадлежит языку")
            elif new_state == 4:
                return("строка не принадлежит языку")
            state = new_state
        return("строка не принадлежит языку")
        
    def generate_string(self, n):
        state = 0
        s = ''
        while len(s) < n:
            if len(s) <= n-len(s):
                choice = random.choice(list(filter(lambda x: x[0] == state and x[1] != 'c' 
                                            and x[1] != '#' and x[2] == self.stack[-1], list(self.delta_dic.keys()))))
            else:
                choice = random.choice(list(filter(lambda x: x[0] == state and 
                                        x[1] != '#' and x[2] == self.stack[-1], list(self.delta_dic.keys()))))
            state, push_s = self.delta_dic[choice]
            self.stack.pop()
            if push_s:
                for i in push_s:
                    self.stack.append(i)
            s += choice[1]
        return s

