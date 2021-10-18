from random import choice

S, B, a, b = 'S', 'B', 'a', 'b'
count_a = 0
count_b = 0
y1 = 0
y2 = 0
prod = {S: {a: "aB"}, B: {a: "aBB", b: "b"}}

def y1():
    global count_a
    count_a += 1
    print("a: " + str(count_a))

def y2():
    global count_b
    count_b += 1
    print("b: " + str(count_b))

lookup_table = {S: {a: [B, a, y1]}, B: {a: [B, B, a, y1], b: [b, y2]}}

def analyzer(s):
    chain = []
    str_chain = ''
    c = ''
    string = s
    stack = ['#', S]
    while stack:
        if stack[-1] == y1 or stack[-1] == y2:
            chain.append(str_chain + ''.join(list(reversed(stack))[1:-1]))
            str_chain += stack[-2]
        stack_top = stack[-1]
        if string: 
            if string[0] not in [a,b]:
                return "\nсимвол не из алфавита\n"
            if stack_top in [a, b]:
                if stack_top == string[0]:
                    stack.pop()
                    string = string[1:]
                else:
                    return "\nцепочка не принадлежит грамматике\n"
            elif stack_top in [S, B]:
                if string[0] in lookup_table[stack_top].keys():
                    stack.pop()
                    for el in lookup_table[stack_top][string[0]]:
                        stack.append(el)
                        if el != y1 and el != y2:
                            c += el
                    #chain.append(c)
                    c = ''
                else:
                    return "\nцепочка не принадлежит грамматике\n"
            elif stack_top == y1 or stack_top == y2:
                stack_top()
                stack.pop() 
            else:
                return "\nцепочка не принадлежит грамматике\n"
            if stack[-1] == '#' and string == '':
                print('\nS', end='')
                for j in chain:
                    print(' -> ' + j, end='')
                return "\nцепочка принадлежит грамматике\n"
        else:
            return "\nцепочка не принадлежит грамматике\n"
    
def generator(m):
    s = "S"
    i = 0
    while True:
        if s == S:
            s = prod[S][a]
            print("S -> {}".format(s), end = '')
            i += 1
        elif s[i] == B:
            if len(s) == m:
                s = s[:i] + prod[B][b] + s[i+1:]
                print(" -> {}".format(s), end = '')
                i += 1
            else:
                if i == len(s)-1:
                    s = s[:i] + prod[B][a] + s[i+1:]
                    print(" -> {}".format(s), end = '')
                    i += 1
                else:
                    char = choice([a,b])
                    s = s[:i] + prod[B][char] + s[i+1:]
                    print(" -> {}".format(s), end = '')
                    i += 1
        if i == m:
            print('')
            return s              

def main():
    while(1):
        print("1) Сгенерировать строку")
        print("2) Проверить строку")
        n = input()
        if n == "2":
            print("Введите строку")
            string = input()
            print()
            print(analyzer(string))
            global count_a, count_b
            count_a = count_b = 0
        if n == "1":
            print("Введите длину строки")
            l = int(input())
            while (l<2 or l%2!=0):
                print("Невозможно сгенерировать строку указаной длины. Укажите верное значение.")
                l = int(input())
            print(generator(l))       

if __name__ == '__main__':
    main()
    