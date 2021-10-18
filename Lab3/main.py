from PDA import *

def check_int(n, bot=0, top=10000000):
    n = n.strip()
    while not n.isdigit() or int(n) > top or int(n) < bot:
        print('Неверный ввод.')
        n = input()
    return int(n)

def main():
    while True:
        print("1. Проверка строки\n2. Генерация строки\n")
        pda = PDA()
        n = check_int(input(), 1, 2)
        if n == 1:
            print("Введите строку")
            print(pda.check_string(input() + '#')+'\n')
        else:
            print("Введите длину строки")
            print(pda.generate_string(check_int(input(), 0))+'\n')

main()