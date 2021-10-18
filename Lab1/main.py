from FSM import FSM

def check_int(n, bot=0, top=10000000):
    n = n.strip()
    while not n.isdigit() or int(n) > top or int(n) < bot:
        print('Неверный ввод.')
        print('\n')
        n = input()
    return int(n)

def main(): 
    my_FSM = FSM()
    index = 9
    while index != 0:
        print('1. Проверить строку')
        print('2. Сгенерировать строку')
        print('0. Выйти\n')
        index = check_int(input(), 0, 2)
        if index == 1:
            line = input()
            if my_FSM.check_string(line):
                print('строка соответствует\n')
        if index == 2:
            n = check_int(input('Количество символов: '), 0)
            print(my_FSM.random_string(n)+'\n')
        else:
            pass

if __name__ == '__main__':
    main()